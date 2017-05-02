# _*_ encoding:utf-8 _*_
__author__ = 'xuyafei'
__date__ = '2017/4/6 上午11:51'


from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class LoginRequiredMixin(object):

    @method_decorator(login_required(login_url="/login/"))
    def dispatch(self, requeat, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(requeat, *args, **kwargs)