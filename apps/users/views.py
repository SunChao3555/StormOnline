# _*_ coding: utf-8 _*_

# --------django包-----------------------------------
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.views.generic.base import View
from django.contrib.auth.hashers import make_password
# ----------------------------------------------------

# -----------自定义模块--------------------------
from .models import UserProfile, EmailVerifyRecord
from .forms import LoginForm, RegisterForm, ForgetpwdForm, Reset_pwdForm
from utils.email_send import send_register_email
# -------------------------------------------------------
# Create your views here.


# ----------------------------重定义登陆方式-------------------------------
class CustomBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None
# -----------------------------end---------------------------------------------------


# --------------------使用类继承django/static.view实现登陆业务逻辑--------------------------
# 最长用的继承view对象是get和post


# ------------------------邮箱验证业务逻辑----------------------------------
class ActiveUserView(View):
    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
        else:
            return render(request, "active_fail.html")
        return render(request, "login.html")


# --------------------邮箱注册业务逻辑---------------------
class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm()
        return render(request, "register.html", {'register_form': register_form})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_name = request.POST.get("email", "")
            if UserProfile.objects.filter(email=user_name):
                return render(request, "login.html", {"register_form": register_form, "msg": "用户已经存在,请登陆"})
            pass_word = request.POST.get("password", "")
            user_profile = UserProfile()
            user_profile.username = user_name
            user_profile.email = user_name
            user_profile.is_active = False
            user_profile.password = make_password(pass_word)
            user_profile.save()
            send_register_email(user_name, "register")
            # return render(request, "send_success.html")
            return render(request, "login.html", {"msg": "激活链接已发至注册邮箱，请激活后登陆"})
        else:
            return render(request, "register.html", {"register_form": register_form})


# ----------------------登陆业务逻辑---------------------------------
class LoginView(View):
    def get(self, request):
        return render(request, "login.html", {})

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_name = request.POST.get("username", "")
            pass_word = request.POST.get("password", "")
            user = authenticate(username=user_name, password=pass_word)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return render(request, "index.html")
                else:
                    return render(request, "login.html", {"msg": "用户未激活！"})
            else:
                return render(request, "login.html", {"msg": "用户名或密码错误！"})
        else:
                return render(request, "login.html", {"msg": "用户名或密码错误！", "login_form": login_form})
# -----------------------------end--------------------------------------------


# ----------------------------使用函数实现登陆业务逻辑----------------------------------
# 调用login出于安全django在request内有安全设计，后面cookie中在做原理了解
# def user_login(request):
#     if request.method == 'POST':
#         user_name = request.POST.get("username", "")
#         pass_word = request.POST.get("password", "")
#         user = authenticate(username=user_name, password=pass_word)
#         if user is not None:
#             login(request, user)
#             return render(request, "index.html")
#         else:
#             return render(request, "login.html", {"msg": "用户名或密码错误"})
#     elif request.method == 'GET':
#         return render(request, "login.html", {})
# --------------------------------------------------------------------------------


# -------------------------忘记密码业务逻辑---------------------------------------
class ForgetPwdView(View):
    def get(self, request):
        forget_form = ForgetpwdForm()
        return render(request, "forgetpwd.html", {"forget_form": forget_form})

    def post(self, request):
        forget_form = ForgetpwdForm(request.POST)
        if forget_form.is_valid():
            email = request.POST.get("email", "")
            send_register_email(email, "forget")
            return render(request, "send_success.html")
        else:
            return render(request, "forgetpwd.html", {"forget_form": forget_form})


# ---------------------使用邮箱重置密码业务逻辑------------------------------------------
class ResetView(View):
    def get(self, request, reset_code):
        all_records = EmailVerifyRecord.objects.filter(code=reset_code)
        if all_records:
            for record in all_records:
                email = record.email
                return render(request, "password_reset.html", {"email": email})
        else:
            return render(request, "active_fail.html")
        return render(request, "login.html")


# ---------------------修改密码业务逻辑------------------------------
'''
        这里post为什么又重新写了一个class而没有放在resetpwd业务逻辑内
        主要是因为，form post在网页上时需要一个action活动url，但是reset继承的view
        内有一个reset_code参数在action活动url中需要带上参数
'''


class ModifyPwdView(View):
    def post(self, request):
        modify_form = Reset_pwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get("password1", "")
            pwd2 = request.POST.get("password2", "")
            email = request.POST.get("email", "")
            if pwd1 != pwd2:
                return render(request, "password_reset.html", {"email": email, "msg": "密码不一致！"})
            user = UserProfile.objects.get(email=email)
            user.password = make_password(pwd2)
            user.save()

            return render(request, "login.html")
        else:
            email = request.POST.get("email", "")
            return render(request, "password_reset.html", {"email": email, "reset_pwd": modify_form})


