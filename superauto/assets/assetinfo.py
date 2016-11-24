#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2016/11/17 16:46
# @Author  : eric
# @Site    : 
# @File    : assetinfo.py
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
from forms import AddAssetinfoForm
from assets.models import AssetDetails,AssetType,AssetBrands,AssetStatus,EmployeeUser,AssetInfo,AssetCdrom

@login_required
def AssetinfoView(request):
    assetinfo_list=AssetInfo.objects.all()
    obj_list=[]
    if assetinfo_list:
        for obj in assetinfo_list:
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
    return render(request, 'include/assetinfo/assetinfo.html',
                  {'obj_list': obj_list, 'allcount': allcount,'sel_list':assetinfo_list})


@login_required
def AssetinfoSearchView(request):
    S = request.GET.get('word', '')
    WT=request.GET.get('wordname','')

    if 'S' in request.GET and request.GET['S']:
        S = request.GET['S']
    if 'WT' in request.GET and request.GET['WT']:
        WT = request.GET['WT']

    allcount=AssetInfo.objects.all().count()
    sel_list=AssetInfo.objects.all()

    if not S and not WT:
        assetinfo_list=AssetInfo.objects.filter(Q(infoname__icontains=S))
    elif not S:
        assetinfo_list=AssetInfo.objects.filter(Q(infoname__icontains=WT))
    elif not WT:
        assetinfo_list = AssetInfo.objects.filter(Q(infoname__icontains=S))
    else:
        assetinfo_list = AssetInfo.objects.filter(Q(infoname__icontains=WT))
    obj_list=[]
    for obj in assetinfo_list:
        if obj.delstatus==0:
            obj_list.append(obj)
    count=len(obj_list)

    paginate_by = settings.PAGE_NUM
    paginator = Paginator(obj_list, paginate_by)
    page = request.GET.get('page')
    try:
        obj_list = paginator.page(page)
    except PageNotAnInteger:
        obj_list = paginator.page(1)
    except EmptyPage:
        obj_list = paginator.page(paginator.num_pages)
    return render(request, 'include/assetinfo/assetinfo.html',
                  {'obj_list': obj_list,'S':S,'WT':WT, 'count': count, 'allcount': allcount,'sel_list':sel_list})


@login_required
def AddAssetinfoView(request):
    if request.method=='GET':

        form = AddAssetinfoForm
        return render_to_response('include/assetinfo/addassetinfo.html', RequestContext(request, {'form': form}))
    else:
        form = AddAssetinfoForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/assetinfo/')
        else:
            form = AddAssetinfoForm
            return render(request, 'include/assetinfo/addassetinfo.html', {'form': form})

@login_required
def EditAssetinfoView(request,info_id):

        try:
            obj_list=AssetInfo.objects.get(id=info_id)
            if request.method == 'POST':
                form=AddAssetinfoForm(request.POST,instance=obj_list)
                if form.is_valid():
                    form.save()
                    return HttpResponseRedirect('/assetinfo/')
            else:
                form=AddAssetinfoForm(instance=obj_list)
                return render(request,'include/assetinfo/editassetinfo.html',{'form':form})
        except AssetInfo.DoesNotExist:
            raise PermissionDenied


@login_required
def DelAssetinfoView(request,info_id):
    try:
        obj_list=AssetInfo.objects.get(id=info_id)
        if request.method=='POST':
            obj_list.delstatus=1
            obj_list.save()
            return HttpResponseRedirect('/assetinfo/')
        else:
            HttpResponse('请正确处理请求')
    except AssetInfo.DoesNotExist:
        raise PermissionDenied


@login_required
def LoadAssetinfoView(request):
    obj_list = AssetInfo.objects.all()
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
        sheet = ws.add_sheet(u'资产配置信息', cell_overwrite_ok=True)

        col_1 = sheet.col(0)  # xlwt中是行和列都是从0开始计算的
        col_2 = sheet.col(1)
        col_3 = sheet.col(2)
        col_4 = sheet.col(3)
        col_5 = sheet.col(4)
        col_6 = sheet.col(5)
        col_7 = sheet.col(6)
        col_8 = sheet.col(7)
        col_9 = sheet.col(8)
        col_10 = sheet.col(9)
        col_11 = sheet.col(10)
        col_12 = sheet.col(11)
        col_13 = sheet.col(12)

        col_1.width = 256 * 20
        col_2.width = 256 * 20
        col_3.width = 256 * 20
        col_4.width = 256 * 20
        col_5.width = 256 * 20
        col_6.width = 256 * 20
        col_7.width = 256 * 20
        col_8.width = 256 * 20
        col_9.width = 256 * 20
        col_10.width = 256 * 20
        col_11.width = 256 * 20
        col_12.width = 256 * 20
        col_13.width = 256 * 20

        sheet.write(0, 0, u'配置名称', style_heading)
        sheet.write(0, 1, u'机器名', style_heading)
        sheet.write(0, 2, u'硬盘容量', style_heading)
        sheet.write(0, 3, u'内存大小', style_heading)
        sheet.write(0, 4, u'是否有光驱', style_heading)
        sheet.write(0, 5, u'显卡', style_heading)
        sheet.write(0, 6, u'CPU', style_heading)
        sheet.write(0, 7, u'显示器', style_heading)
        sheet.write(0, 8, u'IP地址', style_heading)
        sheet.write(0, 9, u'MAC地址', style_heading)
        sheet.write(0, 10, u'Wifi地址', style_heading)
        sheet.write(0, 11, u'WifiMAC地址', style_heading)
        sheet.write(0, 12, u'购买时间', style_heading)

        excel_row = 1
        for obj in obj_list:
            infoname = obj.infoname.strip()
            if not obj.cpname:
                cpname = ""
            else:
                cpname = obj.cpname.strip()
            disktp = obj.disktb.strip()
            memory = obj.memory.strip()
            if not obj.cdrom:
                cdrom = ""
            else:
                cdrom = obj.cdrom.assetcdrom
            if not obj.videocard:
                videocard = ""
            else:
                videocard = obj.videocard
            if not obj.cpu:
                cpu = ""
            else:
                cpu = obj.cpu
            if not obj.displaycard:
                displaycard = ""
            else:
                displaycard = obj.displaycard
            if not obj.ipadress:
                ipadress = ""
            else:
                ipadress = obj.ipadress
            if not obj.mac:
                mac = ""
            else:
                mac = obj.mac
            if not obj.wifi_mac:
                wifi_mac = ""
            else:
                wifi_mac = obj.wifi_mac
            if not obj.wifi_ip:
                wifi_ip = ""
            else:
                wifi_ip = obj.wifi_ip
            if not obj.buy_time:
                buy_time = ""
            else:
                buy_time = obj.buy_time.strftime("%Y/%m/%d")

            sheet.write(excel_row, 0, infoname, style_body)
            sheet.write(excel_row, 1, cpname, style_body)
            sheet.write(excel_row, 2, disktp, style_body)
            sheet.write(excel_row, 3, memory, style_body)
            sheet.write(excel_row, 4, cdrom, style_body)
            sheet.write(excel_row, 5, videocard, style_body)
            sheet.write(excel_row, 6, cpu, style_body)
            sheet.write(excel_row, 7, displaycard, style_body)
            sheet.write(excel_row, 8, ipadress, style_body)
            sheet.write(excel_row, 9, mac, style_body)
            sheet.write(excel_row, 10, wifi_ip, style_body)
            sheet.write(excel_row, 11, wifi_mac, style_body)
            sheet.write(excel_row, 12, buy_time, style)

            excel_row += 1

        fname = 'assetinfofile.xls'

        output = StringIO.StringIO()
        ws.save(output)
        output.seek(0)
        response = HttpResponse(output.getvalue(), content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename=%s' % fname
        response.write(output.getvalue())
        return response

@login_required
def UpAssetinfoView(request):
    username=request.user.username
    if request.method=='POST':
        form=UpForm(request.POST,request.FILES)
        if form.is_valid():
            try:
                xlsfiles = request.FILES.get('upform', '')
                filename = xlsfiles.name
                fname = os.path.join(settings.MEDIA_ROOT, 'uploads/assetinfo/%s' % strftime('%Y/%m/%d', localtime()),
                                     filename)
                if os.path.exists(fname):
                    os.remove(fname)
                dirs = os.path.dirname(fname)
                if not os.path.exists(dirs):
                    os.makedirs(dirs)

                if os.path.isfile(fname):
                    os.remove(fname)
                content = xlsfiles.read()
                fp = open(fname, 'wb')
                fp.write(content)
                fp.close()

                book=xlrd.open_workbook(fname)
                sheet=book.sheet_by_index(0)
                for row_index in range(1,sheet.nrows):
                    record = sheet.row_values(row_index, 0)
                    try:
                        infoname = str(record[0]).strip().rstrip('.0')
                        cpname=record[1].strip()
                        disktp = str(record[2]).strip().rstrip('.0')
                        memory = str(record[3]).strip().rstrip('.0')
                        cdrom = record[4].strip()
                        if cdrom:
                            try:
                                cdrom_id=AssetCdrom.objects.get(assetcdrom=cdrom)
                            except AssetBrands.DoesNotExist:
                                pass
                        videocard = record[5].strip()
                        cpu = str(record[6]).strip()
                        displaycard = record[7].strip()
                        ipadress = record[8].strip()

                        mac = record[9].strip()

                        wifi_ip = record[10].strip()
                        wifi_mac = record[11].strip()
                        buy_time = record[12]
                        if buy_time:
                            tp=type(buy_time)
                            if tp==float:
                                buy_date = xlrd.xldate.xldate_as_datetime(record[12], 0)
                            elif tp == unicode:
                                buy_date = datetime.datetime.strptime(buy_time, '%Y/%m/%d')
                        else:
                            buy_date=None

                        assetinfo=AssetInfo(infoname=infoname,cpname=cpname,disktb=disktp,memory=memory,cdrom=cdrom_id,videocard=videocard,cpu=cpu,displaycard=displaycard,ipadress=ipadress,mac=mac,wifi_ip=wifi_ip,wifi_mac=wifi_mac,buy_time=buy_date)
                        assetinfo.save()

                    except AssetDetails.DoesNotExist, e:
                        traceback.print_stack()
                        traceback.print_exc()
                        print e
                successinfo = "上传"
                success = True
                return render_to_response('include/assetinfo/upassetinfo.html', {
                    "title": '导入资产详情',
                    'form': form,
                    'successinfo': successinfo,
                    'success': success,
                    'username': username}, context_instance=RequestContext(request))
            except Exception, e:
                traceback.print_stack()
                traceback.print_exc()
                print e
        else:
            return render_to_response('include/assetinfo/upassetinfo.html', {
                "title": '导入资产详情',
                'form': form,
                'username': username}, context_instance=RequestContext(request))
    return render_to_response('include/assetinfo/upassetinfo.html', RequestContext(request))

