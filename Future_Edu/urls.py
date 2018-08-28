# coding: utf-8
"""Future_Edu URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url, include

import xadmin


from users.views import IndexView

from django.views.static import serve

from settings import MEDIA_ROOT, STATIC_ROOT    # 生产环境打开，开发环境注释
# from settings import MEDIA_ROOT   # 开发环境打开，产环境注释

urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^captcha/', include('captcha.urls')),
    url(r'^media/(?P<path>.*)', serve, {'document_root': MEDIA_ROOT}),
    url(r'^static/(?P<path>.*)', serve, {'document_root': STATIC_ROOT}),     # 生产环境打开，开发环境注释
    url(r'^users/', include('users.urls', namespace="users")),
    url(r'^org/', include('organization.urls',namespace="org")),
    url(r'^course/', include('courses.urls',namespace="courses")),
    url(r'^teacher/', include('organization.urls',namespace="teacher")),
]



handler404 = "operation.views.page_not_found"
handler500 = "operation.views.server_error"
