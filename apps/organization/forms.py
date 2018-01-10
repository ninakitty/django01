#!/usr/bin/python
# -*- coding: utf-8 -*-
import re

from django import forms

from operation.models import UserAsk


class UserAskForm(forms.ModelForm):
    '''
    定义ModelForm    
    '''

    class Meta:
        model = UserAsk
        fields = ['name', 'mobile', 'course_name']
        error_messages = {
            '__all__': {

            },
            'name': {
                'required': '名字不能为空',
                'invalid': '名字格式错误..',
            },
            'mobile': {
                'required': '手机不能为空',
            },
            'course_name': {
                'required': '课程名不能为空',
            }
        }

    def clean_mobile(self):
        '''
        添加手机号码验证
        :return: 
        '''
        mobile = self.cleaned_data['mobile']
        REGEX_MOBILE = '^(13\d|14[57]|15[^4\D]|17[13678]|18\d)\d{8}|170[^346\D]\d{7}$'
        p = re.compile(REGEX_MOBILE)
        if p.match(mobile):
            return mobile
        else:
            raise forms.ValidationError(code='mobile_invalidata', message='手机验证失败！')
