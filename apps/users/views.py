from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.views.generic import View

from .models import UserProfile
from .forms import UserForm, EmailForm


class RegistView(View):
    def get(self, request):
        return render(request, )


# 自定义认证类
class CustomBackends(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class LoginView(View):
    def get(self, request):
        return render(request, 'login.html', {})

    def post(self, request):
        user_form = UserForm(request.POST)
        user_name = request.POST.get('username', '')
        pass_word = request.POST.get('password', '')
        # form认证
        if user_form.is_valid():
            # 认证用户
            user = authenticate(username=user_name, password=pass_word)
            # 判断是否认证成功
            if user is not None:
                login(request, user)
                return render(request, 'index.html')
            else:
                return render(request, 'login.html',
                              {'msg': '用户名或密码错误！', 'user_name': user_name, 'pass_word': pass_word})
        else:
            return render(request, 'login.html',
                          {'user_form': user_form, 'user_name': user_name, 'pass_word': pass_word})
