"""django01 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.views.generic import TemplateView
from django.views.static import serve

import xadmin

from django01.settings import MEDIA_ROOT

xadmin.autodiscover()
from xadmin.plugins import xversion
from users.views import LoginView, RegisterView, ActUserView, LogoutView, ForgetPwdView, ResetView, ModifyView

xversion.register_models()
urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    url(r'^xadmin/', include(xadmin.site.urls)),
    url(r'^$', TemplateView.as_view(template_name='index.html'), name='index'),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^register/$', RegisterView.as_view(), name='register'),
    url(r'^activate/(?P<act_code>.*)/$', ActUserView.as_view(), name='activate'),
    url(r'^captcha/', include('captcha.urls')),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    url(r'^forget_pwd/$', ForgetPwdView.as_view(), name='forgetpwd'),
    url(r'^reset/(?P<res_code>.*)/$', ResetView.as_view(), name='reset'),
    url(r'^modify/$', ModifyView.as_view(), name='modify'),
    url(r'^org/', include('organization.urls',namespace='org')),
    url(r'^media/(?P<path>.*)$', serve, {'document_root': MEDIA_ROOT}),

]
