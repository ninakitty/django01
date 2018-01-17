# coding:utf-8
from courses.views import CourseListView

__author__ = 'nina'
__date__ = '2018/1/17 14:14'

from django.conf.urls import url

urlpatterns = [
    url(r'^list/$', CourseListView.as_view(), name='courselist'),
]
