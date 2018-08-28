# coding: utf-8
from django.shortcuts import render
from django.views.generic import View
from .models import Course, Video
from django.db.models import Q
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from operation.models import UserFavorite, UserCourse, CourseConments
from django.http import HttpResponse
import json
from utils.mixin_utils import LoginRequiredMixin

class CourseListView(View):
    def get(self, request):
        all_courses = Course.objects.all()
        hot_courses = Course.objects.all().order_by("-click_nums")[:3]
        # todo：实现课程基于关键字搜索的功能（需求掌握ES的搜索）
        search_keywords = request.GET.get("keywords", "")
        if search_keywords:
            all_courses = all_courses.filter(Q(name__icontains=search_keywords)|Q(desc__icontains=search_keywords)|Q(detail__icontains=search_keywords))
        sort = request.GET.get('sort', "new")
        if sort == 'hot':
            all_courses = all_courses.order_by("-click_nums")
        elif sort == 'students':
            all_courses = all_courses.order_by("-students")
        else:
            all_courses = all_courses.order_by("-add_time")
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_courses, per_page=9, request=request)
        courses = p.page(page)
        return render(request, 'courses/course-list.html', {
            "all_courses": courses,
            "sort": sort,
            "hot_courses": hot_courses,
        })



class CourseDetailView(View):
    def get(self, request, course_id):
        course = Course.objects.get(id = int(course_id))
        course.click_nums += 1
        course.save()
        tag = course.tag
        if tag:
            relate_course = Course.objects.filter(tag=tag).exclude(name=course.name).order_by("-click_nums")[:1]
        else:
            relate_course = None
        has_fav_course = False
        has_fav_org = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=int(course_id), fav_type=1):  # 如果已经被这个用户收藏
                has_fav_course = True
            if UserFavorite.objects.filter(user=request.user, fav_id=int(course.course_org.id), fav_type=2):  # 如果已经被这个用户收藏
                has_fav_org = True
        return  render(request, 'courses/course-detail.html', {
            "course": course,
            "relate_course": relate_course,
            "has_fav_course": has_fav_course,
            "has_fav_org": has_fav_org,
        })



# 处理开始学习按钮的逻辑，也就是课程info
class CourseInfoView(LoginRequiredMixin,View):

    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        '''
        小总结：这里获取 章节和资源 都有两种方式
        第一种：因为章节的外键指向课程，因此，可以在课程里面通过Django提供的方法名lesson_set来获取
        第二种：因为章节的外键指向课程，可以通过Lession过滤出课程，例如: Lession.objects.filter(course=course_id)
        '''
        lessions = course.get_course_lession()
        all_resourses = course.get_course_resource()
        # 用户点击之后课程之后，直接将学生加一
        course.students += 1
        course.save()
        # 每次用户点击了这个课程开始学习的时候，让UserCourse这个model保存用户和课程
        # 首先看看是否在UserCourse里面已经将用户和课程关联起来了，如果关联起来，就不要继续保存了
        user_course = UserCourse.objects.filter(user=request.user, course=course)
        if not user_course:
            user_course = UserCourse()
            user_course.user = request.user
            user_course.course = course
            user_course.save()

        # 处理"学过这些课程的同学还学习过哪些课程",
        user_courses = UserCourse.objects.filter(course=course) # 取出这个课程相关的所有的记录
        user_ids = [user_course.user.id for user_course in user_courses] # 获取学个这个课程的所有用户的id
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids) # 通过所有学过这么课程的用户的id，来获取不同的用户学习过的不同的课程记录
        course_ids = [user_course.course.id for user_course in all_user_courses] # 获取用户学到其他课程的所有的课程ID
        relate_courses = Course.objects.filter(id__in=course_ids).exclude(name=course.name).order_by('-click_nums')[:1] # 通过课程ID找出相关的课程， 且排除当前课程，考虑到页面长度，所以随机返回一个课程
        return  render(request, 'courses/course-video.html', {
            "course_id": course_id,
            "lessions": lessions,
            "all_resourses": all_resourses,
            "course": course,
            "relate_courses":relate_courses,
        })



# 处理课程评论的逻辑
class CourseCommentView(LoginRequiredMixin,View):
    def get(self, request, course_id):

        course = Course.objects.get(id=int(course_id))
        all_resourses = course.get_course_resource()
        all_comments = CourseConments.objects.filter(course=course)

        # 处理"学过这些课程的同学还学习过哪些课程",
        user_courses = UserCourse.objects.filter(course=course)  # 取出这个课程相关的所有的记录
        user_ids = [user_course.user.id for user_course in user_courses]  # 获取学个这个课程的所有用户的id
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)  # 通过所有学过这么课程的用户的id，来获取不同的用户学习过的不同的课程记录
        course_ids = [user_course.course.id for user_course in all_user_courses]  # 获取用户学到其他课程的所有的课程ID
        relate_courses = Course.objects.filter(id__in=course_ids).exclude(name=course.name).order_by('-click_nums')[:1]  # 通过课程ID找出相关的课程， 且排除当前课程，考虑到页面长度，所以随机返回一个课程

        return render(request, 'courses/course-comment.html', {
            "course_id": course_id,
            "course": course,
            "all_comments": all_comments,
            "all_resourses": all_resourses,
            "relate_courses": relate_courses,
        })



# 处理用户添加课程的评论, ajax， ajax请求一般是保存到库中
class AddCommentView(View):
    def post(self, request, ):

        # 判断用户是否已经登入
        if not request.user.is_authenticated():
            error = {'status': 'fail', 'msg': '您还未登入，请先登录'}
            # 这里将用户跳转到登录页面是在ajax中处理的，我们这只返回json对象, 如果状态是fail的，那么ajax将会跳转到导入页面
            return HttpResponse(json.dumps(error), content_type="application/json")

        # 将评论存储到数据库之前，课程和内容
        course_id = request.POST.get("course_id", 0)
        comment = request.POST.get('comment', "")

        if course_id > 0 and comment:
            course_comments = CourseConments()
            course = Course.objects.get(id=int(course_id))
            # TODO：这里需要注意下，由于在CourseConments里面course是一个外键的约束，在存储这外键的时候，必须存储的是course实例，不能是ID，
            # TODO：但是从CourseConments取值，可以通过filter函数指定course=course_id来取到CourseConments实例记录
            course_comments.course = course
            course_comments.comments = comment
            course_comments.user = request.user
            course_comments.save()
            success = {'status': 'success', 'msg': '添加成功'}
            # 这里将用户跳转到登录页面是在ajax中处理的，我们这只返回json对象, 如果状态是fail的，那么ajax将会跳转到导入页面
            return HttpResponse(json.dumps(success), content_type="application/json")
        else:
            error = {'status': 'fail', 'msg': '添加失败'}
            # 这里将用户跳转到登录页面是在ajax中处理的，我们这只返回json对象, 如果状态是fail的，那么ajax将会跳转到导入页面
            return HttpResponse(json.dumps(error), content_type="application/json")



# 处理点击视频之后播放的请求
class VideoPlayView(LoginRequiredMixin,View):
    def get(self, request, video_id):
        video = Video.objects.get(id=int(video_id)) # 获取video记录
        course = video.lession.course # 获取这个视频的课程记录
        lessions = course.get_course_lession()
        all_resourses = course.get_course_resource()


        # 每次用户点击了这个课程开始学习的时候，让UserCourse这个model保存用户和课程
        # 首先看看是否在UserCourse里面已经将用户和课程关联起来了，如果关联起来，就不要继续保存了
        user_course = UserCourse.objects.filter(user=request.user, course=course)
        if not user_course:
            user_course = UserCourse()
            user_course.user = request.user
            user_course.course = course
            user_course.save()



        # 处理"学过这些课程的同学还学习过哪些课程",
        user_courses = UserCourse.objects.filter(course=course) # 取出这个课程相关的所有的记录
        user_ids = [user_course.user.id for user_course in user_courses] # 获取学个这个课程的所有用户的id
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids) # 通过所有学过这么课程的用户的id，来获取不同的用户学习过的不同的课程记录
        course_ids = [user_course.course.id for user_course in all_user_courses] # 获取用户学到其他课程的所有的课程ID
        relate_courses = Course.objects.filter(id__in=course_ids).order_by("-click_nums")[:5]  # 通过课程ID找出相关的课程



        return  render(request, 'courses/course-play.html', {

            "lessions": lessions,
            "all_resourses": all_resourses,
            "course": course,
            "relate_courses":relate_courses,
            "video": video,

        })