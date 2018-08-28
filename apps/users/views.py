# coding: utf-8

from django.shortcuts import render
from django.contrib.auth import authenticate,login, logout
from django.contrib.auth.backends import ModelBackend
from users.models import UserProfile
from operation.models import UserCourse, UserFavorite, UserMessage
from courses.models import Course
from organization.models import CourseOrg, Teacher
from django.db.models import Q
from django.views.generic.base import View
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
import logging
from .forms import LoginForm, RegisterForm, ForgetForm, ModifyPwdForm, UploadImageForm, UserInfoForm
from django.contrib.auth.hashers import make_password    # 使用Django自带的对称加密函数，对用户上传的数据进行加密
from utils.email_send import send_register_email
from .models import EmailVerifyRecord, Banner
from utils.mixin_utils import LoginRequiredMixin
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
import json

logger = logging.getLogger('django_debug_error')



# todo:重写认证方法
class CustomBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):
                return user
            return None
        except Exception as e:
            logger.error("username={} message={}".format(username, e))
            return None



class IndexView(View):
    def get(self, request):

        # 取出轮播图页面
        all_banners = Banner.objects.all().order_by("-index")

        # 取出所有的课程，显示在轮播图的课程，不显示在轮播图的课程
        all_courses = Course.objects.all()
        unbanner_courses = all_courses.filter(is_banner=False)[:6]
        banner_courses = all_courses.filter(is_banner=True)[:4]

        # 取出所有的机构
        all_orgs = CourseOrg.objects.all()[:15]



        return render(request, 'users/index.html', {

            "all_banners": all_banners,
            "all_courses": all_courses,
            "unbanner_courses": unbanner_courses,
            "banner_courses": banner_courses,
            "all_orgs": all_orgs,

        })



class LoginView(View):
    def get(self, request):
        return render(request, "users/login.html", {})

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_name = request.POST.get('username', "")
            pass_word = request.POST.get('password', "")
            user = authenticate(username=user_name, password=pass_word)
            if user:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse('index'))
                else:
                    return render(request, "users/login.html", {"msg": "您还没有激活邮箱链接，请激活邮箱链接再登入"})
            return render(request, "users/login.html", {"msg": "用户名或密码错误!"})
        return render(request, "users/login.html", {"login_form": login_form})



# todo:这一块逻辑需要需改下, 将前端页面设置注册的时候，必须填写邮箱、用户名、密码, 不能将邮箱和用户名混着使用
class RegisterView(View):
    def get(self,request):
        register_form = RegisterForm()
        return render(request, template_name='users/register.html', context={'register_form':register_form})

    def post(self,request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_name = request.POST.get('email', "")
            if UserProfile.objects.filter(email=user_name):
                return render(request, "users/register.html", {"msg": u"用户已经存在，请直接登录"})
            pass_word = request.POST.get('password', "")
            user_profile = UserProfile()
            user_profile.is_active = False
            user_profile.username = user_name
            user_profile.email = user_name
            user_profile.password = make_password(pass_word)
            user_profile.save()  # 保存到数据库

            # 如果注册成功，给用户发送一条消息
            user_message = UserMessage()
            user_message.user = user_profile.id
            user_message.message = "欢迎来到Dee Future教学平台"
            user_message.save()

            send_register_email(user_name, 'register')
            return render(request, "users/login.html", context={})
        else:
            return render(request, "users/register.html", {'register_form': register_form})



# todo: 其实这里需要将EmailVerifyRecord这个model添加一个字段，设置这个字段的过期时间，最好是这个model不用MySQL关系数据库，使用redis缓存数据库保存验证码
class ActiveUserView(View):
    def get(self, request, active_code):
        all_code_set = EmailVerifyRecord.objects.filter(code=active_code)
        if all_code_set:
            for record in all_code_set:
                email = record.email
                try:
                    user = UserProfile.objects.get(email=email)
                    user.is_active = True
                    user.save()
                except Exception as e:
                    logger.error("email={} message={}".format(email, e))
            return HttpResponseRedirect(reverse("users:login"))
        else:
            return render(request, 'users/active_fail.html')




class ForgetPwdView(View):
    def get(self, request):
        forget_form = ForgetForm()
        return render(request, "users/forgetpwd.html", {"forget_form": forget_form})

    def post(self, request):
        forget_form = ForgetForm(request.POST)
        if forget_form.is_valid():
            email = request.POST.get("email", "")
            if send_register_email(email, 'forget'):
                return render(request, 'users/send_success.html', {'email': email})
            else:
                return render(request, 'users/send_failed.html', {'email': email})
        else:
            return render(request, 'users/forgetpwd.html', {"forget_form": forget_form})



class ResetView(View):
    def get(self, request, active_code):
        all_code_set = EmailVerifyRecord.objects.filter(code=active_code)
        if all_code_set:
            for record in all_code_set:
                email = record.email
                user = UserProfile.objects.get(email=email)
                return render(request, "users/password_reset.html", {"email": email})
        else:
            return render(request, 'users/active_fail.html', {})



class ModifyPwdView(View):
    def post(self, request):
        modify_pwd_form = ModifyPwdForm(request.POST)
        if modify_pwd_form.is_valid():
            pwd1 = request.POST.get('password1', "")
            pwd2 = request.POST.get('password2', "")
            email = request.POST.get('email', "")
            if pwd1 != pwd2:
                return render(request, 'users/password_reset.html', {"email": email, "msg": "请确保两次输入的密码相同"})
            user = UserProfile.objects.get(email=email)
            user.password = make_password(pwd1)
            user.save()
            # todo: 这里还可以判断，此链接是否已经被点击过。可以在EmailVerifyRecord表中添加一个字段is_alive，然后根据获取email或code从表中过滤出这条记录，然后把is_alive设置为True， 每次进来先查询这个is_alive字段，如果为true，直接返回一个链接失效的HTML
            return render(request, 'users/login.html')
        else:
            email = request.POST.get('email', "")
            return render(request, 'users/password_reset.html', {"email": email, "modify_pwd_form": modify_pwd_form})



# TODO：处理用户个人信息的请求， 最后以及个人信息的post表单提交的修改
class UserinfoView(LoginRequiredMixin,View):
    # 处理用户个人信息的请求
    def get(self, request):
        return render(request, 'users/usercenter-info.html', {

        })

    # 处理用户个人信息的修改
    def post(self, request): # 使用model form对用户的表单提交进行判断

        # todo : 这里传递了一个instance参数，目的是将这个user实例，绑定到这个model form之上, 如果数据验证通过，可以直接保存
        user_info_form = UserInfoForm(request.POST, instance=request.user)
        if user_info_form.is_valid():
            user_info_form.save()

            msg = {"status": "success"}
            return HttpResponse(json.dumps(msg), content_type="application/json")
        else:
            msg = user_info_form.errors
            return HttpResponse(json.dumps(msg), content_type="application/json")



# 处理个人用户信息的头像上传逻辑
class UploadImageView(LoginRequiredMixin,View):
    def post(self, request):
        image_form = UploadImageForm(request.POST, request.FILES, instance=request.user)
        if image_form.is_valid():
            image_form.save()
            msg = {'status': 'success',}
            return HttpResponse(json.dumps(msg), content_type="application/json")
        else:
            msg = {'status': 'fail', }
            return HttpResponse(json.dumps(msg), content_type="application/json")



# 用户在个人中心修改密码
class UpdatePwdView(View):
    def post(self, request):
        modify_pwd_form = ModifyPwdForm(request.POST)
        if modify_pwd_form.is_valid():
            pwd1 = request.POST.get('password1', "")
            pwd2 = request.POST.get('password2', "")
            if pwd1 != pwd2:
                msg = {'status': 'fail', "msg": "请确保两次输入的密码相同",}
                return HttpResponse(json.dumps(msg), content_type="application/json")
            user = request.user
            user.password = make_password(pwd1)
            user.save()

            msg = {'status': 'success', }
            return HttpResponse(json.dumps(msg), content_type="application/json")

        else:
            msg = {"msg": "请按照要求填写新密码"}
            return HttpResponse(json.dumps(msg), content_type="application/json")




# 用户点击获取验证码的逻辑， 用户必须是登入才能发送验证码
class SendEmailCodeView(LoginRequiredMixin,View):
    def get(self, request):
        email = request.GET.get("email", "")
        if UserProfile.objects.filter(email=email):
            msg = {'status': 'fail','msg': '此邮箱已经被注册'}
            return HttpResponse(json.dumps(msg), content_type='application/json')
        else:
            send_register_email(email, "update_email")
            msg = {"status": "success", 'msg': '认证邮件已发送到您的邮箱，请查收'}
            return HttpResponse(json.dumps(msg), content_type='application/json')



# 获取验证码，修改邮箱
class UpdateEmailView(LoginRequiredMixin,View):
    def post(self, request):
        email = request.POST.get('email', '')
        email_code = request.POST.get('email_code', '')

        existed_records = EmailVerifyRecord.objects.filter(email=email,code=email_code, send_type='update_email')
        if existed_records:
            user = request.user
            user.email = email
            user.save()

            msg = {"status": "success", 'msg': '邮箱修改成功'}
            return HttpResponse(json.dumps(msg), content_type='application/json')
        else:
            msg = {"status": "fail", 'msg': '验证码错误，请重新获取验证码'}
            return HttpResponse(json.dumps(msg), content_type='application/json')




# 我的课程页面处理逻辑
class MyCourseView(LoginRequiredMixin,View):
    def get(self, request):
        user_courses = UserCourse.objects.filter(user=request.user)
        courses = [user_course.course for user_course in user_courses]

        return  render(request, 'users/usercenter-mycourse.html', {
            "user_course": user_courses,
            "courses": courses,
        })




# 我的收藏---课程机构
class MyFavOrgView(LoginRequiredMixin,View):
    def get(self, request):
        user_favs = UserFavorite.objects.filter(user=request.user, fav_type=2) # 返回一个收藏机构
        org_ids = [user_fav.fav_id for user_fav in user_favs]
        orgs = [CourseOrg.objects.get(id=org_id) for org_id in org_ids]

        return render(request, 'users/usercenter-fav-org.html', {
            "orgs": orgs,
        })



# 我的收藏---授课老师
class MyFavTeacherView(LoginRequiredMixin,View):
    def get(self, request):
        user_favs = UserFavorite.objects.filter(user=request.user, fav_type=3)
        teacher_ids = [user_fav.fav_id for user_fav in user_favs]
        teachers = [Teacher.objects.get(id=org_id) for org_id in teacher_ids]

        return render(request, 'users/usercenter-fav-teacher.html', {
            "teachers": teachers,
        })




# 我的收藏---公开课程
class MyFavCourseView(LoginRequiredMixin,View):
    def get(self, request):
        user_favs = UserFavorite.objects.filter(user=request.user, fav_type=1)
        course_ids = [user_fav.fav_id for user_fav in user_favs]
        courses = [Course.objects.get(id=org_id) for org_id in course_ids]

        return render(request, 'users/usercenter-fav-course.html', {
            "courses": courses,
        })



# 我的消息
class MyMessageView(LoginRequiredMixin,View):
    def get(self, request):

        all_messages = UserMessage.objects.filter(user=request.user.id)

        # 只要访问了这个链接， 会将所有的消息设置为已读
        all_unread_messages = UserMessage.objects.filter(user=request.user.id, has_read=False)
        for unread_messages in all_unread_messages:
            unread_messages.has_read = True
            unread_messages.save()

        # 对消息进行分页
        try:  # 默认是第一页，如果有page参数，那么page就是传递进来的参数
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_messages, per_page=1, request=request)  # 通过所有机构的记录创建分页器

        messages = p.page(page)  # 翻页器默认从第一页显示

        return render(request, 'users/usercenter-message.html', {
            "all_messages": messages,
        })



class LogoutView(View):
    def get(self, request):
        logout(request)
        from django.core.urlresolvers import reverse
        return HttpResponseRedirect(reverse('index'))








