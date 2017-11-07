# -*- coding: utf-8 -*-
from django.shortcuts import render
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.
from django.views.generic import View
from .models import Course, CourseResource, Video
from operation.models import UserFavorite, CourseComments, UserCourse
from django.http import HttpResponse
import json
from utils.mixin_utils import LoginRequiredMixin
from django.db.models import Q


class CourseListView(View):
    def get(self, request):
        all_courses = Course.objects.all().order_by("-add_time")
        hot_courses = Course.objects.all().order_by("-click_nums")[:3]

        # 课程全局搜索
        search_keywords = request.GET.get('keywords', "")
        if search_keywords:
            all_courses = all_courses.filter(Q(name__icontains=search_keywords) | Q(desc__icontains=search_keywords) | Q(detail__icontains=search_keywords))

        # 课程排序
        sort = request.GET.get('sort', "")
        if sort:
            if sort == "students":
                all_courses = all_courses.order_by("-students")
            elif sort == "hot":
                all_courses = all_courses.order_by("-click_nums")

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # Provide Paginator with the request object for complete querystring generation
        # 第二个参数代表每一页显示的个数
        p = Paginator(all_courses, 3, request=request)
        courses = p.page(page)

        return render(request, 'course-list.html', {
            "all_courses": courses,
            "sort": sort,
            "hot_courses": hot_courses,
        })


class CourseDetailView(View):
    """
    课程详情页
    """
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        # 增加课程点击数
        course.click_nums += 1
        course.save()

        has_fav_course = False
        has_fav_org = False

        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course.id, fav_type=1):
                has_fav_course = True

            elif UserFavorite.objects.filter(user=request.user, fav_id=course.course_org.id, fav_type=2):
                has_fav_org = True

        tag = course.tag
        if tag:
            relate_courses = Course.objects.filter(tag=tag)[:1]
        else:
            relate_courses = []

        return render(request, 'course-detail.html', {
            "course": course,
            "relate_courses": relate_courses,
            "has_fav_course": has_fav_course,
            "has_fav_org": has_fav_org,
        })


class CourseInfoView(LoginRequiredMixin, View):
    """
    课程章节信息
    """
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        course.students += 1
        course.save()

        user_courses_has_bind = UserCourse.objects.filter(user=request.user, course=course)
        if not user_courses_has_bind:
            user_course = UserCourse(user=request.user, course=course)
            user_course.save()

        # 学过该课程的同学还学过其他课程推荐功能

        # UserCourse 定义为一条学生学习某个课程的数据，包含学生，课程
        # 通过一门课程搜索出所有在该课程下学习的UserCourse信息
        user_courses_filter_by_course = UserCourse.objects.filter(course=course)

        # 利用python列表表达式获取所有这些学生的id
        user_ids = [user_courses.user.id for user_courses in user_courses_filter_by_course]

        # 再根据这些学生的id找到这部分学生学过的所有课程(通过列表过滤)
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)

        # 利用python列表表达式获取所有这些课程的id
        course_ids = [user_courses.course.id for user_courses in all_user_courses]

        # 最后根据这些课程id找到这部分课程实例集合
        relate_courses = Course.objects.filter(id__in=course_ids).order_by("-click_nums")[:5]

        all_resource = CourseResource.objects.filter(course=course)
        return render(request, 'course-video.html', {
            "course": course,
            "all_resource": all_resource,
            "relate_courses": relate_courses,
        })


class CourseCommentView(LoginRequiredMixin, View):
    """
    课程评论信息
    """
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        all_resource = CourseResource.objects.filter(course=course)
        all_comments = CourseComments.objects.all()
        return render(request, 'course-comment.html', {
            "course": course,
            "all_comments": all_comments,
            "all_resource": all_resource,
        })


class AddCommentsView(View):
    def post(self, request):
        not_login = {'status': 'fail', 'msg': u'用户未登录'}
        success_comment = {'status': 'success', 'msg': u'添加成功'}
        fail_comment = {'status': 'fail', 'msg': u'评论失败'}
        if not request.user.is_authenticated():
            # 判断用户登录状态
            return HttpResponse(json.dumps(not_login), content_type="application/json")

        course_id = request.POST.get("course_id", 0)
        comments = request.POST.get("comments", "")

        if int(course_id) > 0 and comments:
            course_comments = CourseComments()
            course = Course.objects.get(id=int(course_id))
            course_comments.course = course
            course_comments.comments = comments
            course_comments.user = request.user
            course_comments.save()
            return HttpResponse(json.dumps(success_comment), content_type="application/json")
        else:
            return HttpResponse(json.dumps(fail_comment), content_type="application/json")


class VideoPlayView(View):
    """
    视频播放页面
    """
    def get(self, request, video_id):
        video = Video.objects.get(id=int(video_id))
        course = video.lesson.course
        course.students += 1
        course.save()

        user_courses_has_bind = UserCourse.objects.filter(user=request.user, course=course)
        if not user_courses_has_bind:
            user_course = UserCourse(user=request.user, course=course)
            user_course.save()

        # 学过该课程的同学还学过其他课程推荐功能

        # UserCourse 定义为一条学生学习某个课程的数据，包含学生，课程
        # 通过一门课程搜索出所有在该课程下学习的UserCourse信息
        user_courses_filter_by_course = UserCourse.objects.filter(course=course)

        # 利用python列表表达式获取所有这些学生的id
        user_ids = [user_courses.user.id for user_courses in user_courses_filter_by_course]

        # 再根据这些学生的id找到这部分学生学过的所有课程(通过列表过滤)
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)

        # 利用python列表表达式获取所有这些课程的id
        course_ids = [user_courses.course.id for user_courses in all_user_courses]

        # 最后根据这些课程id找到这部分课程实例集合
        relate_courses = Course.objects.filter(id__in=course_ids).order_by("-click_nums")[:5]

        all_resource = CourseResource.objects.filter(course=course)
        return render(request, 'course-play.html', {
            "course": course,
            "all_resource": all_resource,
            "relate_courses": relate_courses,
            "video": video,
        })
