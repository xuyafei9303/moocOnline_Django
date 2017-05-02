# _*_ encoding:utf-8 _*_
from django.shortcuts import render
from django.views.generic import View
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.db.models import Q
import json

from .models import Course, CourseResource, Video
from operation.models import UserFavorate, CourceComment, UserCourse
from utils.mixin_utils import LoginRequiredMixin

# Create your views here.


class CourseListView(View):
    def get(self, request):
        all_courses = Course.objects.all().order_by("-add_time")

        hot_courses = Course.objects.all().order_by("-click_nums")[:3]

        # 课程搜索
        search_keywords = request.GET.get('keywords', "")
        if search_keywords:
            all_courses = all_courses.filter(Q(name__icontains=search_keywords)|Q(desc__icontains=search_keywords)|Q(detail__icontains=search_keywords))

        # 课程排序
        sort = request.GET.get('sort', '')
        if sort:
            if sort == "students":
                all_courses = all_courses.order_by("-students")
            elif sort == "hot":
                all_courses = all_courses.order_by("-click_nums")

        # 对课程进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_courses, 3, request=request)

        courses = p.page(page)
        return render(request, 'course-list.html', {
            'all_courses': courses,
            'sort': sort,
            'hot_courses': hot_courses,

        })


class CourseDetailView(View):
    '''
    课程详情页
    '''
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        course.click_nums += 1
        course.save()

        has_fav_course = False
        has_fav_org = False

        if request.user.is_authenticated():
            if UserFavorate.objects.filter(user=request.user, fav_id=course.id, fav_type=1):
                has_fav_course = True

            if UserFavorate.objects.filter(user=request.user, fav_id=course.course_org.id, fav_type=2):
                has_fav_org = True


        tag = course.tag
        if tag:
            relate_courses = Course.objects.filter(tag=tag)[:1]
        else:
            relate_courses = []
        return render(request, 'course-detail.html', {
            'course': course,
            'relate_courses': relate_courses,
            'has_fav_course': has_fav_course,
            'has_fav_org': has_fav_org,
        })


class CourseInfoView(LoginRequiredMixin, View):
    '''
    课程章节信息
    '''
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        course.students += 1
        course.save()
        # 查询用户是否关联了该课程
        user_courses = UserCourse.objects.filter(user=request.user, course=course)
        if not  user_courses:
            user_course = UserCourse(user=request.user, course=course)
            user_course.save()

        user_coursers = UserCourse.objects.filter(course=course)
        user_ids = [user_courser.user.id for user_courser in user_coursers]
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)

        # 取出所以课程id
        course_ids = [user_courser.course.id for user_courser in all_user_courses]
        # 获取学过该用户学过其他的所以课程
        relate_courses = Course.objects.filter(id__in=course_ids).order_by("-click_nums")[:5]
        all_resource = CourseResource.objects.filter(course=course)
        return render(request, 'course-video.html', {
            'course': course,
            'course_resources': all_resource,
            'relate_courses': relate_courses,
        })


class CommentsView(LoginRequiredMixin ,View):
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        all_resource = CourseResource.objects.filter(course=course)
        all_comments = CourceComment.objects.all()
        return render(request, 'course-comment.html', {
            'course': course,
            'course_resources': all_resource,
            'all_comments': all_comments,
        })


class VideoPlayView(View):
    '''
    视频播放页面
    '''
    def get(self, request, video_id):
        video = Video.objects.get(id=int(video_id))
        course = video.lesson.course
        # 查询用户是否关联了该课程
        user_courses = UserCourse.objects.filter(user=request.user, course=course)
        if not  user_courses:
            user_course = UserCourse(user=request.user, course=course)
            user_course.save()

        user_coursers = UserCourse.objects.filter(course=course)
        user_ids = [user_courser.user.id for user_courser in user_coursers]
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)

        # 取出所以课程id
        course_ids = [user_courser.course.id for user_courser in all_user_courses]
        # 获取学过该用户学过其他的所以课程
        relate_courses = Course.objects.filter(id__in=course_ids).order_by("-click_nums")[:5]
        all_resource = CourseResource.objects.filter(course=course)
        return render(request, 'course-play.html', {
            'course': course,
            'course_resources': all_resource,
            'relate_courses': relate_courses,
            'video': video,
        })



class AddCommentsView(View):
    '''
    用户提交课程评论
    '''
    def post(self, request):
        # 判断用户登录状态
        if not request.user.is_authenticated():
            return HttpResponse(json.dumps({'status': 'fail', 'msg': '用户未登录'}), content_type='application/json')

        course_id = request.POST.get("course_id", 0)
        comments = request.POST.get("comments", "")
        if course_id > 0 and comments:
            course_comments = CourceComment()
            course = Course.objects.get(id=int(course_id))
            course_comments.course = course
            course_comments.comments = comments
            course_comments.user = request.user
            course_comments.save()
            return HttpResponse(json.dumps({'status': 'success', 'msg': '添加成功'}), content_type='application/json')
        else:
            return HttpResponse(json.dumps({'status': 'fail', 'msg': '添加失败'}), content_type='application/json')



