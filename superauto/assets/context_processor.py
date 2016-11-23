#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2016/11/18 17:20
# @Author  : eric
# @Site    : 
# @File    : context_processor.py
# @Software: PyCharm

from assets.models import SiteInfo
import datetime

def siteinfo(request):
    sitename=SiteInfo.objects.all()[0]
    if request.META.has_key('HTTP_X_FORWARDED_FOR'):
        ip = request.META['HTTP_X_FORWARDED_FOR']
    else:
        ip = request.META['REMOTE_ADDR']

    if request.META.has_key('HTTP_USER_AGENT'):

        agent = request.META['HTTP_USER_AGENT']
    else:
        agent='unknown'

    now_time = datetime.datetime.now()

    return {'sitename':sitename,'ip_address': ip,'agent':agent,'now_time':now_time}

#def ip_address(request):
  #  return {'ip_address': request.META['REMOTE_ADDR']}