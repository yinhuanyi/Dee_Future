#!usr/bin/env python  
#-*- coding:utf-8 _*-  
""" 
@作者: yhy
@模块名: mixin_utils.py 
@创建时间: 2018-04-12 
@模块功能：实现用户登入认证的view, 这是一个工具
"""


from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# TODO： 这个mixin装饰器需要好好总结下
class LoginRequiredMixin(object):

    @method_decorator(login_required(login_url='/users/login/'))
    def dispatch(self, request, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)
