#!/usr/bin/env python  
#-*- coding:utf-8 _*-  
""" 
@作者: yhy
@模块名: forms.py 
@创建时间: 2018-08-07 
@模块功能：
"""


from django import forms


from captcha.fields import CaptchaField

from .models import UserProfile


class LoginForm(forms.Form):
    username = forms.CharField(required=True, min_length=6)
    password = forms.CharField(required=True, min_length=6)



class RegisterForm(forms.Form):
    email = forms.EmailField(required=True, )
    password = forms.CharField(required=True, min_length=6, )
    captcha = CaptchaField(error_messages={"invalid": u"验证码错误, 请重新输入"})



class ForgetForm(forms.Form):
    email = forms.EmailField(required=True, )
    captcha = CaptchaField(error_messages={"invalid": u"验证码错误, 请重新输入"})



class ModifyPwdForm(forms.Form):
    password1 = forms.CharField(required=True, min_length=6)
    password2 = forms.CharField(required=True, min_length=6)




# # 引入form做处理用户上传的头像文件
#  TODO：这里再次引入了model form, 可以把任何一个model form认为是一个model类，且具有form验证的功能
class UploadImageForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ["image", ]

# # 引入form验证用户的信息上传
# # TODO：这里再次引入了model form, 可以把任何一个model form认为是一个model类，且具有form验证的功能
class UserInfoForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ["nick_name", "birthday", "gender", "address", "mobile"]




