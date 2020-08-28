from django.shortcuts import render, redirect, HttpResponse, reverse, HttpResponseRedirect
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from utils.pyqrcode import *
from utils.enhance import get_object
from portal.models import UserProfile
import logging

# Create your views here.

logger = logging.getLogger('webKeepass')


def bad_request(requests, exception):
    return render(requests, 'portal/500.html')

def page_not_found(requests, exception):
    print("page_not_found")
    return render(requests, 'portal/404.html')

class DefaultMixin(LoginRequiredMixin):
    """
    定义 认证类 、 分页 ， 重定向
    """
    login_url = "/login/"


class LoginView(View):
    def get(self, request):
        return render(request, 'portal/login.html')

    def post(self, request):

        username = request.POST.get('username')
        password = request.POST.get('password')
        verfiy = request.POST.get('verfiy')
        user = authenticate(username=username, password=password)
        user_profile = get_object(UserProfile, user=user)
        message = {}
        if user is not None:
            if QrCode.verify(user_profile.secret_key, verfiy):
                login(request, user)
                logger.info(f"{request.user.username} login")
                return redirect('/group/')
            else:
                message = {'msg':'MFA错误'}
                return JsonResponse(message, status=400)
        else:
            # 返回一个非法登录的错误页面
            message = {'msg':'用户名或者密码错误'}
            logger.error(f"{username} login failed")
            # return render(request, 'portal/login.html', locals())
            return JsonResponse(message, status=400)

class LogoutView(DefaultMixin, View):
    def get(self, request):
        logout(request)
        logger.info(f"{request.user.username} logout")
        return HttpResponseRedirect(reverse('dashboard:group'))
