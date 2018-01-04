#!/usr/bin/python
# -*- coding: utf-8 -*-
from captcha.fields import CaptchaField
from django import forms


class UserForm(forms.Form):
    username = forms.CharField(required=True, error_messages={'required': '用户名不能为空！'})
    password = forms.CharField(required=True, min_length=5, error_messages={'required': '密码不能为空！'})


class EmailForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True, min_length=5)
    captcha = CaptchaField(error_messages={'invalid': '验证码错误！', 'required': '验证码不能为空！'})


class ForgetForm(forms.Form):
    email = forms.EmailField(required=True,error_messages={'required':'邮箱不能为空！'})
    captcha = CaptchaField(error_messages={'invalid': '验证码错误！', 'required': '验证码不能为空！'})
