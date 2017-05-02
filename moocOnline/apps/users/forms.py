# _*_ encoding:utf-8 _*_
__author__ = 'xuyafei'
__date__ = '17/3/27 上午11:11'


from django import forms
from captcha.fields import CaptchaField

from .models import UserProfile


class LoginFrom(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, min_length=5)


class RegisterForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True, min_length=5)
    captcha = CaptchaField(error_messages={"invalid": u"验证码错误"})


class ForgetForm(forms.Form):
    email = forms.EmailField(required=True)
    captcha = CaptchaField(error_messages={"invalid": u"验证码错误"})


class ModifyPwdForm(forms.Form):
    password1 = forms.CharField(required=True, min_length=5)
    password2 = forms.CharField(required=True, min_length=5)


# 这里一定要继承ModelForm！！
class UploadImageForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['image']


# 这里一定要继承ModelForm！！
class UserInfoForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['nick_name', 'gender', 'birday', 'address', 'mobile']
