#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2016/10/27 13:40
# @Author  : eric
# @Site    : 
# @File    : urls.py
# @Software: PyCharm

from django.conf.urls import *
from django.contrib import admin
from assets import views
from assets.views import index,DeptSearchView
from assets.dept import EditDept_detail
from django.views.generic.base import RedirectView



urlpatterns = [

    url(r'^$',index),
    url(r'^accounts/login/$', 'assets.account.userlogin', name="userlogin"),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout',
        {'next_page': '/accounts/login/'}, name="userlogout"),

    url(r'^dept/$','assets.dept.DeptView',name='dept-view'),
    url(r'^adddept/$','assets.dept.AddDept',name='adddept-view'),
    url(r'^editdept/$','assets.dept.EditDept',name='editdept-view'),
    url(r'^dept/(\d+)/$', EditDept_detail),
    url(r'^deldept/(\d+)/$', 'assets.dept.DelDept_detail', name='deldept-view'),
    url(r'^search/$', DeptSearchView),
    url(r'^xlwtdept/$', 'assets.upxlwt.dept_xlwt'),
    url(r'^xlrddept/$', 'assets.upxlwt.dept_xlrd'),




]
