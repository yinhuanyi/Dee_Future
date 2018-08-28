#!/usr/bin/env python  
#-*- coding:utf-8 _*-  
""" 
@作者: yhy
@模块名: adminx.py 
@创建时间: 2018-08-03 
@模块功能：
"""

import xadmin

from .models import UserAsk, CourseConments, UserFavorite, UserMessage, UserCourse

class UserAskAdmin(object):
    list_display = ['name', 'mobile', 'course_name', 'add_time']
    search_fields = ['name', 'mobile', 'course_name',]
    list_filter = ['name', 'mobile', 'course_name', 'add_time']
    model_icon = 'fa fa-volume-off'

class CourseConmentsAdmin(object):
    list_display = ['user', 'course', 'comments', 'add_time',]
    search_fields = ['user', 'course', 'comments',]
    list_filter = ['user', 'course', 'comments', 'add_time',]
    model_icon = 'fa fa-wrench'

class UserFavoriteAdmin(object):
    list_display = ['user', 'fav_id', 'fav_type', 'add_time']
    search_fields = ['user', 'fav_id', 'fav_type',]
    list_filter = ['user', 'fav_id', 'fav_type', 'add_time']
    model_icon = 'fa fa-thumbs-up'

class UserMessageAdmin(object):
    list_display = ['user', 'message', 'has_read', 'add_time',]
    search_fields = ['user', 'message', 'has_read',]
    list_filter = ['user', 'message', 'has_read', 'add_time',]
    model_icon = 'fa fa-tablet'

class UserCourseAdmin(object):
    list_display = ['user', 'course', 'add_time', ]
    search_fields = ['user', 'course',]
    list_filter = ['user', 'course', 'add_time', ]
    model_icon = 'fa fa-users'


xadmin.site.register(UserAsk, UserAskAdmin)
xadmin.site.register(CourseConments, CourseConmentsAdmin)
xadmin.site.register(UserFavorite, UserFavoriteAdmin)
xadmin.site.register(UserMessage, UserMessageAdmin)
xadmin.site.register(UserCourse, UserCourseAdmin)
