#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.conf.urls import url

from organization.views import OrgView, AddUserAskView

urlpatterns = [
    url(r'^list/$', OrgView.as_view(), name='orglist'),
    url(r'^add/$', AddUserAskView.as_view(), name='adduserask'),
]
