#!/usr/bin/python
# -*- coding: utf-8 -*-
from captcha.fields import CaptchaField
from django import forms


class UserForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, min_length=5)


class EmailForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True, min_length=5)
    captcha = CaptchaField(error_messages={'invalid':'验证码错误！'})
