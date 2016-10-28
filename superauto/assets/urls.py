#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2016/10/27 13:40
# @Author  : eric
# @Site    : 
# @File    : urls.py
# @Software: PyCharm

from django.conf.urls import include, url
from django.contrib import admin
from assets import views
from assets.views import IndexView,AssetDetailsView,DeptView,EmployeeUserView
from assets.views import login,logout

urlpatterns = [

    url(r'^$',IndexView.as_view(), name='index-view'),
    url(r'^assetdetail/(?P<slug>\w+).html$',
        AssetDetailsView.as_view(), name='assetdetails-view'),
    url(r'^dept/$',DeptView.as_view(), name='dept-view'),
    url(r'^user/$',EmployeeUserView.as_view(), name='user-view'),
    url(r'^logout/$',logout),
    url(r'^login/$', login),

]
