#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2016/11/14 12:09
# @Author  : eric
# @Site    : 
# @File    : repairinfo.py
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
from forms import AddRepairForm
from assets.models import AssetDetails,AssetType,AssetBrands,AssetStatus,EmployeeUser,AssetInfo,AssetCdrom,UserStatus,UserRecord,RecordStatus,AssetChang,RepairInfo

@login_required
def RepairInfoView(request):
    repair_list=RepairInfo.objects.all().order_by('-create_time')
    assetdetail_list=AssetDetails.objects.all()

    obj_list=[]
    if repair_list:
        for obj in repair_list:
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
    return render(request, 'include/repairinfo/repairinfo.html',
                  {'obj_list': obj_list, 'allcount': allcount, 'assetdetail_list': assetdetail_list})


@login_required
def AddRepairInfoView(request):
    if request.method=='GET':

        form = AddRepairForm
        return render_to_response('include/repairinfo/addrepairinfo.html', RequestContext(request, {'form': form}))
    else:
        form = AddRepairForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/repairinfo/')
        else:
            form = AddRepairForm
            return render(request, 'include/repairinfo/addrepairinfo.html', {'form': form})


@login_required
def EditRepairInfoView(request,repair_id):
    try:
        obj_list = RepairInfo.objects.get(id=repair_id)
        if request.method == 'POST':
            form = AddRepairForm(request.POST, instance=obj_list)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/repairinfo/')
        else:
            form = AddRepairForm(instance=obj_list)
            return render(request, 'include/repairinfo/editrepairinfo.html', {'form': form})
    except UserRecord.DoesNotExist:
        raise PermissionDenied

@login_required
def DelRepairInfoView(request,repair_id):
    try:
        obj_list = RepairInfo.objects.get(id=repair_id)
        if request.method == 'POST':
            obj_list.delstatus = 1
            obj_list.save()
            return HttpResponseRedirect('/repairinfo/')
        else:
            HttpResponse('请正确处理请求')
    except UserRecord.DoesNotExist:
        raise PermissionDenied


@login_required
def RepairInfoSearch(request):
    S = request.GET.get('word', '')
    WT = request.GET.get('wordtype', '')
    WB = request.GET.get('wordbrand', '')

    if 'S' in request.GET and request.GET['S']:
        S = request.GET['S']
    if 'WT' in request.GET and request.GET['WT']:
        WT = request.GET['WT']
    if 'WB' in request.GET and request.GET['WB']:
        WB = request.GET['WB']
    assetdetail_list = AssetDetails.objects.all()
    if not WT and not WB:
        repair_list = RepairInfo.objects.filter(
            (Q(itno__itno__icontains=S) | Q(repinfo__icontains=S)| Q(whorep__icontains=S)))
    elif not WT:
        repair_list=RepairInfo.objects.filter((Q(itno__itno__icontains=S)| Q(repinfo__icontains=S)| Q(whorep__icontains=S)) &Q(issure=WB))
    elif not WB:
        repair_list = RepairInfo.objects.filter(
            (Q(repinfo__icontains=S) | Q(whorep__icontains=S)) & Q(itno__itno__icontains=WT))
    else:
        repair_list = RepairInfo.objects.filter(
            (Q(repinfo__icontains=S) | Q(whorep__icontains=S)) & Q(itno__itno__icontains=WT) & Q(
                issure__iexact=WB))

    allcount = EmployeeUser.objects.all().count()

    obj_list = []
    if repair_list:
        for obj in repair_list:
            if obj.delstatus == 0:
                obj_list.append(obj)
    count = len(obj_list)

    paginate_by = settings.PAGE_NUM
    paginator = Paginator(obj_list, paginate_by)
    page = request.GET.get('page')
    try:
        obj_list = paginator.page(page)
    except PageNotAnInteger:
        obj_list = paginator.page(1)
    except EmptyPage:
        obj_list = paginator.page(paginator.num_pages)
    return render(request, 'include/repairinfo/repairinfo.html',
                  {'obj_list': obj_list, 'S': S, 'WT': WT, 'WB': WB, 'assetdetail_list': assetdetail_list,
                    'count': count, 'allcount': allcount})


@login_required
def LoadRepairInfoView(request):
    obj_list =  RepairInfo.objects.all().order_by('itno')
    style_heading = easyxf("""
                            font:
                                name SimSun,
                                colour_index black,
                                bold on,
                                height 300;
                            align:
                                wrap off,
                                vert center,
                                horiz center;

                            pattern:
                                pattern solid,
                                fore-colour 0x34;
                            borders:
                                left THIN,
                                right THIN,
                                top THIN,
                                bottom THIN;
                                """
                           )
    style_body = easyxf("""
                            font:
                                name Arial,
                                bold off,
                                height 250;
                            align:
                                wrap on,
                                vert center,
                                horiz left;
                            borders:
                                left THIN,
                                right THIN,
                                top THIN,
                                bottom THIN;
                            """
                        )
    style_green = easyxf(" pattern: pattern solid,fore-colour 0x11;")
    style_red = easyxf(" pattern: pattern solid,fore-colour 0x0A;")
    fmts = [
        'M/D/YY',
        'D-MMM-YY',
        'D-MMM',
        'MMM-YY',
        'h:mm AM/PM',
        'h:mm:ss AM/PM',
        'h:mm',
        'h:mm:ss',
        'M/D/YY h:mm',
        'mm:ss',
        '[h]:mm:ss',
        'mm:ss.0',
    ]
    style = XFStyle()
    style.num_format_str = 'M/D/YY'

    if obj_list:
        ws = Workbook(encoding='utf-8')
        sheet = ws.add_sheet(u'资产维护记录', cell_overwrite_ok=True)
        col_1 = sheet.col(0)  # xlwt中是行和列都是从0开始计算的
        col_2 = sheet.col(1)
        col_3 = sheet.col(2)
        col_4 = sheet.col(3)
        col_5 = sheet.col(4)
        col_6 = sheet.col(5)
        col_7 = sheet.col(6)



        col_1.width = 256 * 40
        col_2.width = 256 * 20
        col_3.width = 256 * 20
        col_4.width = 256 * 50
        col_5.width = 256 * 20
        col_6.width = 256 * 20
        col_7.width = 256 * 20


        sheet.write(0, 0, u'资产编号', style_heading)
        sheet.write(0, 1, u'维护开始时间', style_heading)
        sheet.write(0, 2, u'维护结束时间', style_heading)
        sheet.write(0, 3, u'维护内容', style_heading)
        sheet.write(0, 4, u'是否完成', style_heading)
        sheet.write(0, 5, u'维护人员', style_heading)
        sheet.write(0, 6, u'维护人电话', style_heading)



        excel_row = 1
        for obj in obj_list:
            itno = obj.itno.itno


            if not obj.start_time:
                start_time = ""
            else:
                start_time = obj.start_time.strftime("%Y/%m/%d")

            if not obj.end_time:
                end_time = ""
            else:
                end_time = obj.end_time.strftime("%Y/%m/%d")






            if not obj.repinfo:
                repinfo = ""
            else:
                repinfo = obj.repinfo


            if obj.issure==True:
                issure='完成'
            else:
                issure='未完成'
            if not obj.whorep:
                whorep = ""
            else:
                whorep = obj.whorep
            if not obj.whophone:
                whophone = ""
            else:
                whophone = obj.whophone

            sheet.write(excel_row, 0, itno, style_body)
            sheet.write(excel_row, 1, start_time, style)
            sheet.write(excel_row, 2, end_time, style)
            sheet.write(excel_row, 3, repinfo, style_body)
            sheet.write(excel_row, 4, issure, style_body)
            sheet.write(excel_row, 5, whorep, style_body)
            sheet.write(excel_row, 6, whophone, style_body)


            excel_row += 1
        fname = 'repairinfo.xls'
        output = StringIO.StringIO()
        ws.save(output)
        output.seek(0)
        response = HttpResponse(output.getvalue(), content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename=%s' % fname
        response.write(output.getvalue())
        return response



@login_required
def UpRepairInfoView(request):
    pass
