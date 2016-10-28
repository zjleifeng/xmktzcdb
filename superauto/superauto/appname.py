#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2016/10/26 13:44
# @Author  : eric
# @Site    : 
# @File    : appname.py
# @Software: PyCharm

from django.contrib.admin.apps import AdminConfig as _AdminConfig
from django.apps import AppConfig

class assetsConfig(AppConfig):
    name=u'assets'
    verbose_name=u'资产管理'