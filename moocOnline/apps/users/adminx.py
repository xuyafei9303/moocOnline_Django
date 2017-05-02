# _*_ encoding:utf-8 _*_
__author__ = 'xuyafei'
__date__ = '17/3/24 上午9:47'

import xadmin
from xadmin import views
# from xadmin.plugins.auth import UserAdmin

from .models import EmailVerifyRecord, Banner


# class UserProfileAdmin(UserAdmin):
#     pass


class BaseSetting(object):
    enable_themes = True #主题功能
    use_bootswatch = True # 后台模板样式


class GlobalSettings(object):
    site_title = "慕课在线网后台管理系统" # 左上角title
    site_footer = "copy-right 慕课网" # 下面footertitle
    menu_style = "accordion" # 后台中右侧的app字段折叠起来


class EmailVerifyRecordAdmin(object):
    list_display = ['code', 'email', 'send_type', 'send_time']
    search_fields = ['code', 'email', 'send_type']
    list_filter = ['code', 'email', 'send_type', 'send_time']
    model_icon = 'fa fa-address-book-o'


class BannerAdmin(object):
    list_display = ['title', 'image', 'url', 'index', 'add_time']
    search_fields = ['title', 'image', 'url', 'index']
    list_filter = ['title', 'image', 'url', 'index', 'add_time']


# from django.contrib.auth.models import User
# xadmin.site.unregister(User)
xadmin.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin)
xadmin.site.register(Banner, BannerAdmin)
# xadmin.site.register(UserProfile, UserProfileAdmin)

xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSettings)