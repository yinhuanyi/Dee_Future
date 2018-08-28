#!/usr/bin/env python  
#-*- coding:utf-8 _*-  
""" 
@作者: yhy
@模块名: adminx.py 
@创建时间: 2018-08-02 
@模块功能：
"""

import xadmin

from .models import Course, Lesson, Video, CourseResource, BannerCourse



class LessonInline(object):
    model = Lesson
    extra = 0



class CourseResourceInline(object):
    model = CourseResource
    extra = 0



class BannerCourseAdmin(object):
    list_display = ['name', 'desc', 'degree', 'learn_times', 'students', 'fav_num', 'image', 'click_nums', "course_org",
                    'add_time']
    search_fields = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students', 'fav_num', 'image', 'click_nums',
                     'add_time']
    list_filter = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students', 'fav_num', 'image', 'click_nums',
                   'course_org', 'add_time']
    ordering = ["-click_nums"]
    readonly_fields = ['students', 'fav_num']
    exclude = ['click_nums']
    inlines = [LessonInline, CourseResourceInline]
    model_icon = 'fa fa-magic'

    # TODO： 重载父类的方法， 完成对is_banner字段的过滤
    def queryset(self):
        qs = super(BannerCourseAdmin, self).queryset()
        qs = qs.filter(is_banner=True)
        return qs



class CourseAdmin(object):
    list_display = ['name', 'desc', 'degree', 'learn_times', 'students', 'fav_num', 'image', 'click_nums', "course_org"]
    search_fields = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students', 'fav_num', 'image', 'click_nums',
                     'add_time']
    list_filter = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students', 'fav_num', 'image', 'click_nums',
                   'course_org', 'add_time']
    ordering = ["-click_nums"]
    readonly_fields = ['students', 'fav_num']
    list_editable = ['degree', 'desc']
    exclude = ['click_nums']
    inlines = [LessonInline, CourseResourceInline]
    refresh_times = [3, 5]
    style_fields = {"detail": "ueditor"}
    import_excel = True
    model_icon = 'fa fa-book'

    # TODO： 重载父类的方法， 完成对is_banner字段的过滤
    def queryset(self):
        qs = super(CourseAdmin, self).queryset()
        qs = qs.filter(is_banner=False)
        return qs


class LessonAdmin(object):
    list_display = ['course', 'name', 'add_time', ]
    search_fields = ['course', 'name', ]
    list_filter = ['course__name', 'name', 'add_time', ]
    model_icon = 'fa fa-folder-open-o'



class VideoAdmin(object):
    list_display = ['lession', 'name', 'add_time', ]
    search_fields = ['lession', 'name', ]
    list_filter = ['lession', 'name', 'add_time', ]
    model_icon = 'fa fa-play-circle'



class CourseResourceAdmin(object):
    list_display = ['course', 'name', 'download', 'add_time']
    search_fields = ['course', 'name', 'download']
    list_filter = ['course', 'name', 'download', 'add_time']
    model_icon = 'fa fa-suitcase'


xadmin.site.register(Course, CourseAdmin)
xadmin.site.register(BannerCourse, BannerCourseAdmin)
xadmin.site.register(Lesson, LessonAdmin)
xadmin.site.register(Video, VideoAdmin)
xadmin.site.register(CourseResource, CourseResourceAdmin)
