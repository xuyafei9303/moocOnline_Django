# _*_ encoding:utf-8 _*_
__author__ = 'xuyafei'
__date__ = '17/3/24 上午11:09'

import xadmin

from .models import Course, Lesson, Video, CourseResource, BannerCourse
from organization.models import CourseOrg


class LessonInLine(object):
    model = Lesson
    extra = 0


class CourseResourceInLine(object):
    model = CourseResource
    extra = 0

class CourseAdmin(object):
    list_display = ['name', 'desc', 'detail', 'degree', 'learn_time', 'students', 'fav_nums', 'image', 'click_nums', 'add_time', 'get_zj_nums', 'go_to']
    search_fields = ['name', 'desc', 'detail', 'degree', 'students']
    list_filter = ['name', 'desc', 'detail', 'degree', 'learn_time', 'students', 'fav_nums', 'image', 'click_nums', 'add_time']
    ordering = ['-click_nums'] # 根据点击数倒叙排列
    readonly_fields = ['click_nums'] # 设置某些字段在显示的时候是只读的
    exclude = ['fav_nums'] # 让某些字段不显示出来 与上面字段同时存在会导致冲突
    inlines = [LessonInLine, CourseResourceInLine]
    list_editable= ['name' , 'degree']# 在列表页的字段设置直接修改
    style_fields = {"detail":"ueditor"}

    # refresh_time= [3, 5] 按时刷新

    def queryset(self):
        qs = super(CourseAdmin, self).queryset()
        qs = qs.filter(is_banner=False)
        return qs

    def save_models(self):
        # 在保存课程的时候统计课程机构的课程数
        obj = self.new_obj
        obj.save()
        if obj.course_org is not None:
            course_org = obj.course_org
            course_org.course_nums = Course.objects.filter(course_org=course_org).count()
            course_org.save()


class BannerCourseAdmin(object):
    list_display = ['name', 'desc', 'detail', 'degree', 'learn_time', 'students', 'fav_nums', 'image', 'click_nums', 'add_time']
    search_fields = ['name', 'desc', 'detail', 'degree', 'students']
    list_filter = ['name', 'desc', 'detail', 'degree', 'learn_time', 'students', 'fav_nums', 'image', 'click_nums', 'add_time']
    ordering = ['-click_nums'] # 根据点击数倒叙排列
    readonly_fields = ['click_nums'] # 设置某些字段在显示的时候是只读的
    exclude = ['fav_nums'] # 让某些字段不显示出来 与上面字段同时存在会导致冲突
    inlines = [LessonInLine, CourseResourceInLine]

    def queryset(self):
        qs = super(BannerCourseAdmin, self).queryset()
        qs = qs.filter(is_banner=True)
        return qs


class LessonAdmin(object):
    list_display = ['course', 'name', 'add_time']
    search_fields = ['course', 'name']
    list_filter = ['course__name', 'name', 'add_time']


class VideoAdmin(object):
    list_display = ['lesson', 'name', 'add_time']
    search_fields = ['lesson', 'name']
    list_filter = ['lesson', 'name', 'add_time']


class CourseResourceAdmin(object):
    list_display = ['course', 'name', 'download', 'add_time']
    search_fields = ['lesson', 'name', 'download']
    list_filter = ['course', 'name', 'download', 'add_time']

xadmin.site.register(Course, CourseAdmin)
xadmin.site.register(BannerCourse, BannerCourseAdmin)
xadmin.site.register(Lesson, LessonAdmin)
xadmin.site.register(Video, VideoAdmin)
xadmin.site.register(CourseResource, CourseResourceAdmin)

