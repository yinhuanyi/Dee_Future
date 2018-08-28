# coding: utf-8
from __future__ import unicode_literals

from datetime import datetime

from django.db import models

# Create your models here.



class CityDict(models.Model):
    name = models.CharField(max_length=20, verbose_name="城市")
    desc = models.CharField(max_length=200, verbose_name="描述")
    add_time = models.DateTimeField(default=datetime.now)


    class Meta:
        verbose_name = "城市"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name



class CourseOrg(models.Model):
    name = models.CharField(max_length=50, verbose_name="机构名称")
    tag = models.CharField(max_length=20, verbose_name="机构标签", default="全国知名")
    category = models.CharField(max_length=10,
                                choices=(('pxjg', '培训机构'), ('gx', '高校'), ('gr', '个人')),
                                default="pxjg",
                                verbose_name="机构类别")
    desc = models.TextField(verbose_name="机构描述")
    click_nums = models.IntegerField(default=0, verbose_name="点击数")
    fav_nums = models.IntegerField(default=0, verbose_name="收藏数")
    image = models.ImageField(upload_to="org/%Y/%m", verbose_name="机构logo图片")
    address = models.CharField(max_length=50, verbose_name="机构地址")
    city = models.ForeignKey(CityDict, verbose_name='所在城市')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')
    students = models.IntegerField(default=0, verbose_name="学习人数")
    course_numbers = models.IntegerField(default=0, verbose_name="课程数")
    phone = models.CharField(default="", verbose_name='机构电话', max_length=100)


    class Meta:
        verbose_name = "课程机构"
        verbose_name_plural = verbose_name


    def __str__(self):
        return self.name

    def get_teacher_number(self):
        return self.teacher_set.all().count()

    def get_course_number(self):
        return self.course_set.all().count()


class Teacher(models.Model):
    org = models.ForeignKey(CourseOrg, verbose_name="所属机构")
    name = models.CharField(max_length=50, verbose_name="教师名")
    work_years = models.IntegerField(default=0, verbose_name="工作年限")
    work_company = models.CharField(max_length=50, verbose_name="就职公司")
    work_position = models.CharField(max_length=50, verbose_name="公司职位")
    points = models.CharField(max_length=50, verbose_name="教学特点")
    click_nums = models.IntegerField(default=0, verbose_name="点击数")
    fav_nums = models.IntegerField(default=0, verbose_name="收藏数")
    add_time = models.DateTimeField(default=datetime.now)
    image = models.ImageField(upload_to="teacher/%Y/%m", verbose_name="头像", max_length=100, default="")
    desc = models.CharField(max_length=1000, default="", verbose_name="自我介绍")
    class_num = models.IntegerField(default=1, verbose_name="课程数")
    age = models.IntegerField(default=24, verbose_name="年龄", )


    class Meta:
        verbose_name = "教师"
        verbose_name_plural = verbose_name


    def __str__(self):
        return self.name

    def get_courses(self):
        return self.course_set.all().count()


