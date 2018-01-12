#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.conf.urls import url

from organization.views import OrgView, AddUserAskView, OrgHomeView

urlpatterns = [
    url(r'^list/$', OrgView.as_view(), name='orglist'),
    url(r'^add/$', AddUserAskView.as_view(), name='adduserask'),
    url(r'^home/(?P<org_id>\d+)/$', OrgHomeView.as_view(), name='org_home'),
]
