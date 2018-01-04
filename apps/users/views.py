from django.contrib.auth.hashers import make_password
from django.shortcuts import render
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.views.generic import View

from utils.email_send import send_register_email
from .models import UserProfile, EmailVerifyRecord
from .forms import UserForm, EmailForm


class ActUserView(View):
    def get(self, request, act_code):
        all_record = EmailVerifyRecord.objects.filter(code=act_code)
        if all_record:
            for record in all_record:
                email = record.email
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
                return render(request, 'login.html', {'msg': '激活成功！请登录！'})


class RegisterView(View):
    def get(self, request):
        reg_form = EmailForm()
        return render(request, 'register.html', {'reg_form': reg_form})

    def post(self, request):
        reg_form = EmailForm(request.POST)
        if reg_form.is_valid():
            user_name = request.POST.get('email', '')
            pass_word = request.POST.get('password', '')
            userProfile = UserProfile()
            userProfile.username = user_name
            userProfile.email = user_name
            userProfile.password = make_password(pass_word)
            userProfile.is_active = False

            # 查询是否已存在
            if UserProfile.objects.filter(Q(username=user_name) | Q(email=user_name)):

                return render(request, 'register.html', {'msg': '邮箱已存在！', 'reg_form': reg_form})
            else:
                userProfile.save()
                # 发送验证邮件
                send_register_email(userProfile.email, 'register')
                return render(request, 'login.html', {'msg': '注册成功！请进入邮箱激活帐号！'})
        else:
            return render(request, 'register.html', {'reg_form': reg_form})


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
                if user.is_active:
                    login(request, user)
                    return render(request, 'index.html')
                else:
                    return render(request, 'login.html',
                                  {'msg': '用户未激活！'})
            else:
                return render(request, 'login.html',
                              {'msg': '用户名或密码错误！', 'user_name': user_name, 'pass_word': pass_word})
        else:
            return render(request, 'login.html',
                          {'user_form': user_form, 'user_name': user_name, 'pass_word': pass_word})


class LogoutView(View):
    def get(self, request):
        logout(request)
        return render(request, 'login.html', {})
