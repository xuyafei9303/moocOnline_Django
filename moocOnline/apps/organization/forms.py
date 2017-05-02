# _*_ encoding:utf-8 _*_
__author__ = 'xuyafei'
__date__ = '17/3/31 下午3:44'

import re
from django import forms


from operation.models import UserAsk


class UserAskForm(forms.ModelForm):

    class Meta:
        model = UserAsk
        fields = ['name', 'mobile', 'course_name']

    def clean_mobile(self):
        '''
        验证手机号码是否合法
        '''
        mobile = self.cleaned_data['mobile']
        REGEX_MOBILE = "^1(3[0-9]|4[57]|5[0-35-9]|7[01678]|8[0-9])\d{8}$"
        p = re.compile(REGEX_MOBILE)
        if p.match(mobile):
            return mobile
        else:
            return forms.ValidationError(u"手机号码非法", code="mobile_invalid")