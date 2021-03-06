#!/usr/bin/env python  
#-*- coding:utf-8 _*-  
""" 
@作者: yhy
@模块名: adminx.py 
@创建时间: 2018-08-03 
@模块功能：
"""

import xadmin

from .models import CityDict, CourseOrg, Teacher

class CityDictAdmin(object):
    list_display = ['name', 'desc', 'add_time',]
    search_fields = ['name', 'desc',]
    list_filter = ['name', 'desc', 'add_time',]
    model_icon = 'fa fa-laptop'

class CourseOrgAdmin(object):
    list_display = ['name', 'desc', 'click_nums', 'fav_nums', 'image', 'address', 'city', 'add_time']
    search_fields = ['name', 'desc', 'click_nums', 'fav_nums', 'image', 'address', 'city']
    list_filter = ['name', 'desc', 'click_nums', 'fav_nums', 'image', 'address', 'city', 'add_time']
    model_icon = 'fa fa-camera-retro'




class TeacherAdmin(object):
    list_display = ['org', 'name', 'work_years', 'work_company', 'work_position', 'points', 'click_nums', 'fav_nums', 'add_time']
    search_fields = ['org', 'name', 'work_years', 'work_company', 'work_position', 'points', 'click_nums', 'fav_nums',]
    list_filter = ['org', 'name', 'work_years', 'work_company', 'work_position', 'points', 'click_nums', 'fav_nums', 'add_time']
    model_icon = 'fa fa-square'

xadmin.site.register(CityDict, CityDictAdmin)
xadmin.site.register(CourseOrg, CourseOrgAdmin)
xadmin.site.register(Teacher, TeacherAdmin)