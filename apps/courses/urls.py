#!/usr/bin/env python  
#-*- coding:utf-8 _*-  
""" 
@作者: yhy
@模块名: urls.py 
@创建时间: 2018-08-17 
@模块功能：
"""
from django.conf.urls import url
from .views import CourseListView, CourseDetailView, CourseInfoView, CourseCommentView, AddCommentView, VideoPlayView


urlpatterns = [
    url(r'^list/', CourseListView.as_view(), name="course_list"),
    # 课程的详情页，这里的course_id要与get()方法的关键字参数名称一一对应
    url(r'^detail/(?P<course_id>\d+)/', CourseDetailView.as_view(), name="course_detail"),
    # 课程详情页中的开始学习处理
    url(r'^info/(?P<course_id>\d+)/', CourseInfoView.as_view(), name="course_info"),
    # 课程详情页中的课程评论
    url(r'^comment/(?P<course_id>\d+)/', CourseCommentView.as_view(), name="course_comment"),
    # 添加课程评论的ajax请求处理
    url(r'^add_comment/', AddCommentView.as_view(), name="add_comment"),
    # 视频播放
    url(r'^video/(?P<video_id>\d+)/', VideoPlayView.as_view(), name="video_play"),
]
