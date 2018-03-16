# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-03-11 14:54
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_emailverifyrecord'),
    ]

    operations = [
        migrations.CreateModel(
            name='Banner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='\u6807\u9898')),
                ('image', models.ImageField(upload_to='banner/%Y/%m', verbose_name='\u8f6e\u64ad\u56fe')),
                ('url', models.URLField(verbose_name='\u8bbf\u95ee\u5730\u5740')),
                ('index', models.IntegerField(default=100, verbose_name='\u987a\u5e8f')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='\u6dfb\u52a0\u65f6\u95f4')),
            ],
            options={
                'verbose_name': '\u8f6e\u64ad\u56fe',
                'verbose_name_plural': '\u8f6e\u64ad\u56fe',
            },
        ),
        migrations.AlterModelOptions(
            name='emailverifyrecord',
            options={'verbose_name': '\u90ae\u7bb1\u9a8c\u8bc1\u7801', 'verbose_name_plural': '\u90ae\u7bb1\u9a8c\u8bc1\u7801'},
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='image',
            field=models.ImageField(default='image/default.png', upload_to='image/%Y/%m'),
        ),
    ]
