# coding: utf-8
from __future__ import unicode_literals

from datetime import datetime


from django.db import models

from organization.models import CourseOrg, Teacher



# Create your models here.
class Course(models.Model):
    name = models.CharField(max_length=50, verbose_name="课程名")
    desc = models.CharField(max_length=300, verbose_name="课程描述")
    # detail = UEditorField(verbose_name=u"课程详情",width=600, height=300, imagePath="courses/ueditor/", filePath="courses/ueditor/", default="")
    detail = models.TextField(verbose_name='课程详情', max_length=100000, default='')
    # todo: 这里需要注意：因为degree是choice类型，如果前端直接在HTML中取degree的值，那么会显示数据库中保存的值，那么在取值的时候应该这样写：{{ course.get_degree_display }} ， 这样取到的值就是choice映射的值
    degree = models.CharField(choices=(("cj", '初级'), ("zj","中级"), ("gj", "高级")), max_length=3, verbose_name='难易程度')
    is_banner = models.BooleanField(default=False, verbose_name="是否此课程显示到轮播图")
    learn_times = models.IntegerField(default=0, verbose_name="学习时长(分钟数)")
    students = models.IntegerField(default=0, verbose_name="学习人数")
    fav_num = models.IntegerField(default=0, verbose_name="收藏人数")
    image = models.ImageField(upload_to="courses/%Y/%m", verbose_name="封面图", max_length=100)
    click_nums = models.IntegerField(default=0, verbose_name="点击数")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")
    course_org = models.ForeignKey(CourseOrg, verbose_name='课程机构', null=True, blank=True)
    teacher = models.ForeignKey(Teacher, verbose_name=u"授课老师", null=True, blank=True)
    course_category = models.CharField(max_length=100, verbose_name=u"课程类别", choices=(("before", "前端技术"),("after", "后端技术")), default="after")
    tag = models.CharField(verbose_name=u"课程标签", max_length=10, default="")
    what_you_need_know = models.TextField(max_length=400, verbose_name=u"课程须知", default="")
    what_you_can_learn = models.TextField(max_length=400, verbose_name=u"课程可以学到什么", default="")


    class Meta:
        verbose_name = "课程"
        verbose_name_plural = verbose_name


    def __str__(self):
        return self.name

    def get_lession_number(self):
        return self.lesson_set.all().count()


    def get_learn_users(self):
        return self.usercourse_set.all()[:5]

    def get_course_lession(self):
        return self.lesson_set.all()

    def get_course_resource(self):
        return self.courseresource_set.all()


# 这个BannerCourse有一个proxy，表示只是映射到Course的数据，并不会创建一张表
class BannerCourse(Course):


    class Meta:
        verbose_name = u"轮播课程"
        verbose_name_plural = verbose_name
        proxy = True



class Lesson(models.Model):


    course = models.ForeignKey(Course, verbose_name="课程")
    name = models.CharField(max_length=100, verbose_name="章节名")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")



    class Meta:
        verbose_name = "章节"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def get_lession_video(self):
        return self.video_set.all()



class Video(models.Model):


    lession = models.ForeignKey(Lesson, verbose_name="章节")
    name = models.CharField(max_length=100, verbose_name="视频名")
    url = models.CharField(max_length=200, verbose_name="视频访问地址", default="")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")
    learn_times = models.IntegerField(default=0, verbose_name="学习时长(分钟数)")


    class Meta:
        verbose_name = "视频"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name



class CourseResource(models.Model):


    course = models.ForeignKey(Course, verbose_name="课程")
    name = models.CharField(max_length=100, verbose_name="名称")
    download = models.FileField(upload_to="course/resource/%Y/%m", verbose_name="资源文件", max_length=100)
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")


    class Meta:
        verbose_name = "Dee Future学习资源"
        verbose_name_plural = verbose_name



    def __str__(self):
        return self.name