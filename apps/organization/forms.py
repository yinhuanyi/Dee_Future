#!/usr/bin/env python  
#-*- coding:utf-8 _*-  
""" 
@作者: yhy
@模块名: forms.py 
@创建时间: 2018-08-15 
@模块功能：
"""

from django import forms
from operation.models import UserAsk
import re



class UserAskForm(forms.ModelForm):


    class Meta:
        model = UserAsk
        fields = ['name', 'mobile', 'course_name']

    def clean_mobile(self):
        mobile = self.cleaned_data['mobile']
        REGEX_MOBILE = "^(13[0-9]|14[579]|15[0-3,5-9]|16[6]|17[0135678]|18[0-9]|19[89])\d{8}$"
        p = re.compile(REGEX_MOBILE)
        if p.match(mobile):
            return mobile
        else:
            raise forms.ValidationError(message='手机号码不正确', code="mobile_invalid")


