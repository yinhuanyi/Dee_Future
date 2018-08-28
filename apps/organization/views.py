# coding: utf-8
from django.shortcuts import render
from django.views.generic import View
from .models import CourseOrg, CityDict, Teacher
from operation.models import UserFavorite
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from .forms import UserAskForm
from django.http import HttpResponse
from courses.models import Course
from django.db.models import Q
import json



class OrgView(View):
    def get(self, request):
        all_orgs = CourseOrg.objects.all()
        hot_orgs = all_orgs.order_by("-click_nums")[:3]
        category = request.GET.get('ct', "")
        if category:
            all_orgs = all_orgs.filter(category=category)
        city_id = request.GET.get('city', "")
        if city_id:
            all_orgs = all_orgs.filter(city_id=city_id)
        sort = request.GET.get('sort', '')
        if sort:
            all_orgs = all_orgs.order_by('-students') if sort == 'students' else all_orgs.order_by('-course_numbers')
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(object_list=all_orgs, per_page=5 ,request=request)
        orgs = p.page(page)
        all_citys = CityDict.objects.all()
        org_nums = all_orgs.count()
        return render(request, 'organization/org-list.html', {
            'all_orgs': orgs,
            'all_citys': all_citys,
            'org_nums': org_nums,
            'city_view_id': city_id,
            'category': category,
            'hot_orgs': hot_orgs,
            'sort': sort,
        })



class AddUserAskView(View):
    def post(self, request):
        user_ask_form = UserAskForm(request.POST)
        if user_ask_form.is_valid():
            user_ask_form.save(commit=True)
            success = {'status': 'success'}
            return HttpResponse(json.dumps(success), content_type="application/json")
        else:
            error = {'status': 'fail', 'msg': '提交出错!!!'}
            return HttpResponse(json.dumps(error), content_type="application/json")



class OrgHomeView(View):
    def get(self,request, org_id):
        current_page = 'home'
        course_org = CourseOrg.objects.get(id=int(org_id))
        all_courses = course_org.course_set.all()
        all_teachers = course_org.teacher_set.all()
        course_org.click_nums += 1
        course_org.save()
        fav_status = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=int(org_id), fav_type=2):
                fav_status = True
        return render(request, 'organization/org-detail-homepage.html', {
            "all_courses": all_courses,
            "all_teachers": all_teachers,
            "course_org": course_org,
            "current_page": current_page,
            "fav_status": fav_status,
        })



class OrgCourseView(View):
    def get(self,request, org_id):
        current_page = 'course'
        course_org = CourseOrg.objects.get(id=int(org_id))
        all_courses = course_org.course_set.all()
        fav_status = False
        if request.user.is_authenticated():
            print('用户登录')
            if UserFavorite.objects.filter(user=request.user, fav_id=int(org_id), fav_type=2):
                fav_status = True
        return render(request, 'organization/org-detail-course.html', {
            "all_courses": all_courses,
            "course_org": course_org,
            "current_page": current_page,
            "fav_status": fav_status,
        })



class OrgDescView(View):
    def get(self,request, org_id):
        current_page = 'desc'
        course_org = CourseOrg.objects.get(id=int(org_id))
        fav_status = False
        if request.user.is_authenticated():
            print('用户登录')
            if UserFavorite.objects.filter(user=request.user, fav_id=int(org_id), fav_type=2):
                fav_status = True
        return render(request, 'organization/org-detail-desc.html', {
            "course_org": course_org,
            "current_page": current_page,
            "fav_status": fav_status,
        })



class OrgTeacherView(View):
    def get(self,request, org_id):
        current_page = 'teacher'
        course_org = CourseOrg.objects.get(id=int(org_id))
        all_teachers = course_org.teacher_set.all()
        fav_status = False
        if request.user.is_authenticated():
            print('用户登录')
            if UserFavorite.objects.filter(user=request.user, fav_id=int(org_id), fav_type=2):
                fav_status = True
        return render(request, 'organization/org-detail-teachers.html', {
            "all_teachers": all_teachers,
            "course_org": course_org,
            "current_page": current_page,
            "fav_status": fav_status,
        })



class AddFavView(View):
    def post(self, request):
        fav_id = request.POST.get('fav_id', 0)
        fav_type = request.POST.get('fav_type', 0)
        if not request.user.is_authenticated():
            error = {'status': 'fail', 'msg': '您还未登入，请先登录'}
            return HttpResponse(json.dumps(error), content_type="application/json")
        else:
            exist_records = UserFavorite.objects.filter(user=request.user, fav_id=int(fav_id), fav_type=int(fav_type))
            if exist_records:
                exist_records.delete()
                if int(fav_type) == 1:
                    course = Course.objects.get(id=int(fav_id))
                    course.fav_num -= 1
                    course.save()
                elif int(fav_type) == 2:
                    org = CourseOrg.objects.get(id=int(fav_id))
                    org.fav_nums -= 1
                    org.save()
                elif int(fav_type) == 3:
                    teacher = Teacher.objects.get(id=int(fav_id))
                    teacher.fav_nums -= 1
                    teacher.save()
                error = {'status': 'fail', 'msg': '收藏'}
                return HttpResponse(json.dumps(error), content_type="application/json")
            else:
                user_fav = UserFavorite()
                if int(fav_id) > 0 and int(fav_type) >0:
                    user_fav.user = request.user
                    user_fav.fav_id = int(fav_id)
                    user_fav.fav_type = int(fav_type)
                    user_fav.save()
                    if int(fav_type) == 1:
                        course = Course.objects.get(id=int(fav_id))
                        course.fav_num += 1
                        course.save()
                    elif int(fav_type) == 2:
                        org = CourseOrg.objects.get(id=int(fav_id))
                        org.fav_nums += 1
                        org.save()
                    elif int(fav_type) == 3:
                        teacher = Teacher.objects.get(id=int(fav_id))
                        teacher.fav_nums += 1
                        teacher.save()
                    success = {'status': 'success', 'msg': '已收藏'}
                    return HttpResponse(json.dumps(success), content_type="application/json")
                else:
                    error = {'status': 'fail', 'msg': '收藏失败'}
                    return HttpResponse(json.dumps(error), content_type="application/json")



class TeacherListView(View):
    def get(self, request):
        all_teachers = Teacher.objects.all()

        # todo：实现讲师基于关键字搜索的功能（需求掌握ES的搜索）
        search_keywords = request.GET.get("keywords", "")
        if search_keywords:
            all_teachers = all_teachers.filter(
                Q(name__icontains=search_keywords) | Q(desc__icontains=search_keywords) | Q(
                    work_position__icontains=search_keywords))

        # 解决人气排序
        sort = request.GET.get('sort', '')
        all_teachers = all_teachers.order_by("-click_nums") if sort == "hot" else all_teachers.order_by("add_time")

        # 解决讲师排行榜
        sorted_teachers = all_teachers.order_by("-work_years")[:3]

        # 对课程机构进行分页
        try:  # 默认是第一页
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_teachers, per_page=2, request=request)  # 通过所有机构的记录创建分页器

        teachers = p.page(page)  # 翻页器默认从第一页显示

        # 获取机构的数量
        org_nums = all_teachers.count()

        nav = 'teacher'

        return  render(request, 'organization/teachers-list.html', {
            "all_teachers":teachers,
            "org_nums": org_nums,
            "sort": sort,
            "sorted_teachers": sorted_teachers,
        })



# 处理老师详情页的请求
class TeacherDetailView(View):
    def get(self, request, teacher_id):

        teacher = Teacher.objects.get(id=int(teacher_id))
        all_teachers = Teacher.objects.all().order_by("-click_nums")[:3]
        all_courses = Course.objects.filter(teacher=teacher)

        # 每次点击了老师详情页，点击数加一
        teacher.click_nums += 1
        teacher.save()

        # 显示页面重新刷新后的收藏和已收藏逻辑， 这里其实就是点击刷新
        has_teacher_faved = False
        has_org_faved = False
        if UserFavorite.objects.filter(fav_id=teacher.id, fav_type=3):
            has_teacher_faved = True
        if UserFavorite.objects.filter(fav_id=teacher.org.id, fav_type=2):
            has_org_faved = True


        return  render(request, 'organization/teacher-detail.html', {
            "teacher": teacher,
            "teacher_id": teacher_id,
            "all_teachers": all_teachers,
            "all_courses": all_courses,
            "has_teacher_faved": has_teacher_faved,
            "has_org_faved": has_org_faved,
        })
