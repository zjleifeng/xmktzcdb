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
from assets.models import AssetDetails,AssetType,AssetBrands,AssetStatus,EmployeeUser,AssetInfo,AssetCdrom,UserStatus,UserRecord,RecordStatus,AssetChang

@login_required
def UseRecordView(request):
    record_list=UserRecord.objects.all().order_by('-creare_time')
    assetdetail_list=AssetDetails.objects.all()
    users_list=EmployeeUser.objects.all()
    recordtype_list=RecordStatus.objects.all()
    obj_list=[]

    if record_list:
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
    S = request.GET.get('word', '')
    WT = request.GET.get('wordtype', '')
    WB = request.GET.get('wordbrand', '')
    WS = request.GET.get('wordstatus', '')

    if 'S' in request.GET and request.GET['S']:
        S = request.GET['S']
    if 'WT' in request.GET and request.GET['WT']:
        WT = request.GET['WT']
    if 'WB' in request.GET and request.GET['WB']:
        WB = request.GET['WB']
    if 'WS' in request.GET and request.GET['WS']:
        WS = request.GET['WS']

    sS = (Q(itno__itno__icontains=S) | Q(chang__assetchang__icontains=S))
    sWT = Q(itno__itno__iexact=WT)
    sWB = Q(user__engname__iexact=WB)
    sWS = Q(secordtatus__recordstatus__iexact=WS)

    if not WT and not WB and not WS:
        sql = sS


    elif not WT:
        if not WB:
            sql = sS & sWS

        elif not WS:
            sql = sS & sWB

        else:
            sql = sS & sWS & sWB

    elif not WB:
        if not WS:
            sql = sS & sWT

        else:
            sql = sS & sWS & sWT

    elif not WS:
        sql = sS & sWB & sWT


    else:
        sql = sS & sWS & sWB & sWT

    obj_list = UserRecord.objects.filter(sql)



    count = obj_list.count()
    allcount = UserRecord.objects.all().count()

    assetdetail_list = AssetDetails.objects.all()
    users_list = EmployeeUser.objects.all()
    recordtype_list = RecordStatus.objects.all()
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
                  {'obj_list': obj_list, 'S': S, 'WT': WT, 'WB': WB, 'WS': WS, 'assetdetail_list': assetdetail_list,
                   'users_list': users_list, 'recordtype_list': recordtype_list, 'count': count,
                   'allcount': allcount})


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
    obj_list = UserRecord.objects.all().order_by('itno')
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
        sheet = ws.add_sheet(u'资产使用记录', cell_overwrite_ok=True)
        col_1 = sheet.col(0)  # xlwt中是行和列都是从0开始计算的
        col_2 = sheet.col(1)
        col_3 = sheet.col(2)
        col_4 = sheet.col(3)
        col_5 = sheet.col(4)
        col_6 = sheet.col(5)
        col_7 = sheet.col(6)
        col_8 = sheet.col(7)


        col_1.width = 256 * 40
        col_2.width = 256 * 20
        col_3.width = 256 * 20
        col_4.width = 256 * 20
        col_5.width = 256 * 20
        col_6.width = 256 * 20
        col_7.width = 256 * 20
        col_8.width = 256 * 20

        sheet.write(0, 0, u'资产编号', style_heading)
        sheet.write(0, 1, u'使用者', style_heading)
        sheet.write(0, 2, u'使用类型', style_heading)
        sheet.write(0, 3, u'领用日期', style_heading)
        sheet.write(0, 4, u'预计归还日期', style_heading)
        sheet.write(0, 5, u'实际归还时间', style_heading)
        sheet.write(0, 6, u'归还状态', style_heading)
        sheet.write(0, 7, u'备注', style_heading)


        excel_row = 1
        for obj in obj_list:
            itno = obj.itno.itno
            if not obj.user:
                user = ""
            else:
                user = obj.user.engname

            if not obj.chang:
                chang = ""
            else:
                chang = obj.chang.assetchang

            if not obj.start_time:
                start_time = ""
            else:
                start_time = obj.start_time.strftime("%Y/%m/%d")

            if not obj.yend_time:
                yend_time = ""
            else:
                yend_time = obj.yend_time.strftime("%Y/%m/%d")

            if not obj.send_time:
                send_time = ""
            else:
                send_time = obj.send_time.strftime("%Y/%m/%d")




            if not obj.secordtatus:
                secordtatus = ""
            else:
                secordtatus = obj.secordtatus.recordstatus

            if not obj.recordtype:
                recordtype = ""
            else:
                recordtype = obj.recordtype

            sheet.write(excel_row, 0, itno, style_body)
            sheet.write(excel_row, 1, user, style_body)
            sheet.write(excel_row, 2, chang, style_body)
            sheet.write(excel_row, 3, start_time, style)
            sheet.write(excel_row, 4, yend_time, style)
            sheet.write(excel_row, 5, send_time, style)
            sheet.write(excel_row, 6, secordtatus, style_body)
            sheet.write(excel_row, 7, recordtype, style_body)

            excel_row += 1
        fname = 'userrecord.xls'
        output = StringIO.StringIO()
        ws.save(output)
        output.seek(0)
        response = HttpResponse(output.getvalue(), content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename=%s' % fname
        response.write(output.getvalue())
        return response

def UpUseRecordView(request):
    username = request.user.username
    if request.method == 'POST':
        form = UpForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                xlsfiles = request.FILES.get('upform', '')
                filename = xlsfiles.name
                fname = os.path.join(settings.MEDIA_ROOT, 'uploads/userrecord/%s' % strftime('%Y/%m/%d', localtime()),
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

                book = xlrd.open_workbook(fname)
                sheet = book.sheet_by_index(0)
                for row_index in range(1, sheet.nrows):
                    record = sheet.row_values(row_index, 0)
                    try:
                        itno = record[0].strip().rstrip(".0")
                        if itno:
                            try:
                                itnoid=AssetDetails.objects.get(itno=itno)
                            except AssetDetails.DoesNotExist:
                                pass
                        else:
                            pass


                        user = record[1].strip()
                        if user:
                            try:
                                userid=EmployeeUser.objects.get(engname=user)
                            except EmployeeUser.DoesNotExist:
                                pass
                        else:
                            userid=None

                        chang = record[2].strip()
                        if chang:
                            try:
                                changid = AssetChang.objects.get(assetchang=chang)
                            except AssetChang.DoesNotExist:
                                pass
                        else:
                            changid = None

                        start_time_r = record[3]
                        if start_time_r:
                            tp = type(start_time_r)
                            if tp == float:

                                start_time = xlrd.xldate.xldate_as_datetime(record[3], 0)

                            elif tp == unicode:

                                start_time = datetime.datetime.strptime(start_time_r, '%Y/%m/%d')

                        else:
                            start_time = None

                        yend_time_r = record[4]
                        if yend_time_r:
                            tp = type(yend_time_r)
                            if tp == float:

                                yend_time = xlrd.xldate.xldate_as_datetime(record[4], 0)

                            elif tp == unicode:

                                yend_time = datetime.datetime.strptime(yend_time_r, '%Y/%m/%d')

                        else:
                            yend_time = None

                        send_time_r = record[5]
                        if send_time_r:
                            tp = type(send_time_r)
                            if tp == float:

                                send_time = xlrd.xldate.xldate_as_datetime(record[4], 0)

                            elif tp == unicode:

                                send_time = datetime.datetime.strptime(send_time_r, '%Y/%m/%d')

                        else:
                            send_time = None

                        secordtatus = record[6].strip()
                        if secordtatus:
                            try:
                                secordtatusid = RecordStatus.objects.get(recordstatus=secordtatus)
                            except RecordStatus.DoesNotExist:
                                pass
                        else:
                            secordtatusid = None

                        recordtype = record[7].strip()


                        asset = UserRecord(itno=itnoid, user=userid, chang=changid, start_time=start_time,
                                           yend_time=yend_time, send_time=send_time, secordtatus=secordtatusid,recordtype=recordtype)
                        asset.save()

                    except AssetDetails.DoesNotExist, e:
                        traceback.print_stack()
                        traceback.print_exc()
                        print e
                successinfo = "上传"
                success = True
                return render_to_response('include/userecord/upuserecord.html', {
                    "title": '导入使用记录',
                    'form': form,
                    'successinfo': successinfo,
                    'success': success,
                    'username': username}, context_instance=RequestContext(request))
            except Exception, e:
                traceback.print_stack()
                traceback.print_exc()
                print e
        else:
            return render_to_response('include/userecord/upuserecord.html', {
                "title": '导入使用',
                'form': form,
                'username': username}, context_instance=RequestContext(request))
    return render_to_response('include/userecord/upuserecord.html', RequestContext(request))
