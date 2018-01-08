from django.contrib.auth.hashers import make_password
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.views.generic import View

from utils.email_send import send_register_email
from .models import UserProfile, EmailVerifyRecord
from .forms import UserForm, EmailForm, ForgetForm, ModifyPwdForm


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
        else:
            return render(request, 'login.html', {'msg': '激活失败！请与管理员联系！'})


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
            if UserProfile.objects.filter(email=user_name):
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
        return render(request, 'index.html', {})


class ForgetPwdView(View):
    def get(self, request):
        forgetform = ForgetForm()
        return render(request, 'forgetpwd.html', {'forgetform': forgetform})

    def post(self, request):
        email = request.POST.get('email', '')
        forgetform = ForgetForm(request.POST)
        if forgetform.is_valid():
            if UserProfile.objects.filter(email=email):
                send_register_email(email, 'forget')
                return render(request, 'login.html', {'msg': '邮件已发送！请进入邮箱重置密码！'})
            else:
                return render(request, 'forgetpwd.html', {'msg': '注册邮箱不存在！'})
        else:
            return render(request, 'forgetpwd.html', {'forgetform': forgetform})


class ResetView(View):
    def get(self, request, res_code):
        all_record = EmailVerifyRecord.objects.filter(code=res_code)
        if all_record:
            for record in all_record:
                email = record.email
                return render(request, 'password_reset.html', {'email': email})
        else:
            return render(request, 'login.html', {'msg': '链接已过期或错误！请重试！'})
class ModifyView(View):
    def post(self, request):
        mod_form = ModifyPwdForm(request.POST)
        password = request.POST.get('password', '')
        password2 = request.POST.get('password2', '')
        email = request.POST.get('email', '')
        if mod_form.is_valid():
            if password == password2:
                user = UserProfile.objects.get(email=email)
                user.password = make_password(password2)
                user.save()
                EmailVerifyRecord.objects.filter(email=email).delete()
                return render(request, 'login.html', {'msg': '密码修改成功，请登录！'})
            else:
                return render(request, 'password_reset.html', {'email': email, 'mod_form': mod_form,'msg':'两次密码不一致！'})
        else:
            return render(request, 'password_reset.html', {'email': email, 'mod_form': mod_form})
