#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2016/11/18 13:23
# @Author  : eric
# @Site    : 
# @File    : userecord.py
# @Software: PyCharm


from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from superauto import settings
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.shortcuts import render,render_to_response
from django.db.models import Q
from django.http import HttpResponseRedirect,HttpResponse

from django.core.exceptions import PermissionDenied

from assets.models import Dept
from xlwt import *
import StringIO
from assets.forms import UpForm
import os
from time import strftime,localtime
import xlrd
import traceback
import time
import datetime
from forms import AddRecordForm
from assets.models import AssetDetails,AssetType,AssetBrands,AssetStatus,EmployeeUser,AssetInfo,AssetCdrom,UserStatus,UserRecord,RecordStatus

@login_required
def UseRecordView(request):
    record_list=UserRecord.objects.all().order_by('-creare_time')
    assetdetail_list=AssetDetails.objects.all()
    users_list=EmployeeUser.objects.all()
    recordtype_list=RecordStatus.objects.all()
    obj_list=[]
    for obj in record_list:
        if obj.delstatus==0:
            obj_list.append(obj)
    allcount=len(obj_list)

    paginate_by = settings.PAGE_NUM
    paginator = Paginator(obj_list, paginate_by)
    page = request.GET.get('page')
    try:
        obj_list = paginator.page(page)
    except PageNotAnInteger:
        obj_list = paginator.page(1)
    except EmptyPage:
        obj_list = paginator.page(paginator.num_pages)
    return render(request, 'include/userecord/userecord.html',
                  {'obj_list': obj_list, 'allcount': allcount, 'assetdetail_list': assetdetail_list,'users_list':users_list,'recordtype_list':recordtype_list})


def UseRecordSearch(request):
    pass

def AddUseRecordView(request):
    if request.method=='GET':

        form = AddRecordForm
        return render_to_response('include/userecord/adduserecord.html', RequestContext(request, {'form': form}))
    else:
        form = AddRecordForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/userecord/')
        else:
            form = AddRecordForm
            return render(request, 'include/userecord/adduserecord.html', {'form': form})

def EditUseRecordView(request,record_id):
    try:
        obj_list = UserRecord.objects.get(id=record_id)
        if request.method == 'POST':
            form = AddRecordForm(request.POST, instance=obj_list)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/userecord/')
        else:
            form = AddRecordForm(instance=obj_list)
            return render(request, 'include/userecord/edituserecord.html', {'form': form})
    except UserRecord.DoesNotExist:
        raise PermissionDenied

def DelUseRecordView(request,record_id):
    try:
        obj_list=UserRecord.objects.get(id=record_id)
        if request.method=='POST':
            obj_list.delstatus=1
            obj_list.save()
            return HttpResponseRedirect('/userecord/')
        else:
            HttpResponse('请正确处理请求')
    except UserRecord.DoesNotExist:
        raise PermissionDenied

def LoadUseRecordView(request):
    pass

def UpUseRecordView(request):
    pass