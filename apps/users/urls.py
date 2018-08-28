#!/usr/bin/env python  
#-*- coding:utf-8 _*-  
""" 
@作者: yhy
@模块名: urls.py 
@创建时间: 2018-08-12 
@模块功能：
"""

from django.conf.urls import url, include

from .views import LoginView, RegisterView, ActiveUserView, ForgetPwdView, ResetView, ModifyPwdView, UserinfoView, UploadImageView, UpdatePwdView, SendEmailCodeView,UpdateEmailView, MyCourseView, MyFavOrgView, MyFavTeacherView, MyFavCourseView, MyMessageView, LogoutView

urlpatterns = [
    url(r'login/$', LoginView.as_view(), name='login'),
    url(r'^logout/',LogoutView.as_view() , name='logout'),
    url(r'register/', RegisterView.as_view(), name='register'),
    url(r'^active/(?P<active_code>.*)/$', ActiveUserView.as_view(), name="user_active"),
    url(r'^forget/', ForgetPwdView.as_view(), name="forget_pwd"),
    url(r'^reset/(?P<active_code>.*)/$', ResetView.as_view(), name="reset_pwd"),
    url(r'^modify_pwd/', ModifyPwdView.as_view(), name="modify_pwd"),


    url(r'^info/', UserinfoView.as_view(), name="user_info"),
    url(r'^image/upload/', UploadImageView.as_view(), name="image_upload"),
    url(r'^update/pwd/', UpdatePwdView.as_view(), name="update_pwd"),
    url(r'^sendmail_code/', SendEmailCodeView.as_view(), name="sendmail_code"),
    url(r'^update_email/', UpdateEmailView.as_view(), name="update_email"),
    url(r'^mycourse/', MyCourseView.as_view(), name="mycourse"),
    url(r'^myfav/org/', MyFavOrgView.as_view(), name="myfav_org"),
    url(r'^myfav/teacher/', MyFavTeacherView.as_view(), name="myfav_teacher"),
    url(r'^myfav/course/', MyFavCourseView.as_view(), name="myfav_course"),
    url(r'^mymsg/', MyMessageView.as_view(), name="mymsg"),
]
