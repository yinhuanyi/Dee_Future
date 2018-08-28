#!/usr/bin/env python
#-*- coding:utf-8 _*-  
""" 
@作者: yhy
@模块名: xadmin.py 
@创建时间: 2018-08-02 
@模块功能：
"""

import xadmin

from xadmin import views

# 因为 UserProfile已经被注册了，所以不需要再次在xadmin中注册 UserProfile
from .models import EmailVerifyRecord, Banner

# 后台的样式配置
class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True

# 需改全局的样式
class GlobalSetting(object):
    site_title = "Dee Future教学管理系统"
    site_footer = "Dee Future教学管理系统"
    menu_style = "accordion"  # 让后台APP的model自行折叠


# 创建管理器
class EmailVerifyRecordAdmin(object):

    # 注明在后台显示的字段信息
    list_display = ['code', 'email', 'send_type', 'send_time']

    # 注明搜索的时候在哪些字段中进行搜索
    search_fields = ['code', 'email', 'send_type', 'send_time']

    # 给后台添加筛选功能
    list_filter = ['code', 'email', 'send_type', 'send_time']

    # 修改这个model在后台的字体图标
    model_icon = 'fa fa-tasks'

class BannerAdmin(object):
    # 注明在后台显示的字段信息
    list_display = ['title', 'image', 'url', 'index', 'add_time']

    # 注明搜索的时候在哪些字段中进行搜索
    search_fields = ['title', 'image', 'url', 'index', 'add_time']

    # 给后台添加筛选功能
    list_filter = ['title', 'image', 'url', 'index', 'add_time']

    # 修改这个model在后台的字体图标
    model_icon = 'fa fa-tags'


# 将邮箱验证表，注册到后台管理
xadmin.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin)
xadmin.site.register(Banner, BannerAdmin)



# 注册主题样式
xadmin.site.register(views.BaseAdminView, BaseSetting)

# 注册全局的设置
xadmin.site.register(views.CommAdminView, GlobalSetting)