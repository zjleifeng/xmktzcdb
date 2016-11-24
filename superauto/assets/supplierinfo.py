#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2016/11/12 14:41
# @Author  : eric
# @Site    : 
# @File    : supplierinfo.py
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
from forms import AddSupplierForm
from assets.models import AssetDetails,AssetType,AssetBrands,AssetStatus,EmployeeUser,UserRecord,SupplierInfo

@login_required
def SupplierView(request):
    supplier_list = SupplierInfo.objects.all()

    obj_list = []
    if supplier_list:
        for obj in supplier_list:
            if obj.delstatus == 0:
                obj_list.append(obj)

    allcount = len(obj_list)


    paginate_by = settings.PAGE_NUM
    paginator = Paginator(obj_list, paginate_by)
    page = request.GET.get('page')
    try:
        obj_list = paginator.page(page)
    except PageNotAnInteger:
        obj_list = paginator.page(1)
    except EmptyPage:
        obj_list = paginator.page(paginator.num_pages)
    return render(request, 'include/supplierinfo/supplierinfo.html',
                  {'obj_list': obj_list, 'allcount': allcount})


@login_required
def AddSupplierView(request):
    if request.method=='GET':

        form = AddSupplierForm
        return render_to_response('include/supplierinfo/addsupplierinfo.html', RequestContext(request, {'form': form}))
    else:
        form = AddSupplierForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/supplier/')
        else:
            form = AddSupplierForm
            return render(request, 'include/supplierinfo/addsupplierinfo.html', {'form': form})

@login_required
def EditSupplierView(request,sup_id):
    try:
        obj_list = SupplierInfo.objects.get(id=sup_id)
        if request.method == 'POST':
            form = AddSupplierForm(request.POST, instance=obj_list)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/supplier/')
        else:
            form = AddSupplierForm(instance=obj_list)
            return render(request, 'include/supplierinfo/editsupplierinfo.html', {'form': form})
    except UserRecord.DoesNotExist:
        raise PermissionDenied

@login_required
def DelSupplierView(request,sup_id):
    try:
        obj_list = SupplierInfo.objects.get(id=sup_id)
        if request.method == 'POST':
            obj_list.delstatus = 1
            obj_list.save()
            return HttpResponseRedirect('/supplier/')
        else:
            HttpResponse('请正确处理请求')
    except UserRecord.DoesNotExist:
        raise PermissionDenied



@login_required
def SupplierSearch(request):
    S = request.GET.get('word', '')
    obj_list = SupplierInfo.objects.filter(Q(corporate_name__icontains=S)|Q(contect_name__icontains=S))
    if 'S' in request.GET and request.GET['S']:
        S = request.GET['S']
    count=obj_list.count()
    if count==0:
        count='零'
    allcount = SupplierInfo.objects.all().count()
    paginate_by = settings.PAGE_NUM
    paginator = Paginator(obj_list, paginate_by)
    page = request.GET.get('page')
    try:
        obj_list = paginator.page(page)  # 返回用户请求的页码对象
    except PageNotAnInteger:  # 如果请求中的page不是数字,也就是为空的情况下
        obj_list = paginator.page(1)
    except EmptyPage:
        # 如果请求的页码数超出paginator.page_range(),则返回paginator页码对象的最后一页
        obj_list = paginator.page(paginator.num_pages)
    return render(request, 'include/supplierinfo/supplierinfo.html', {'obj_list': obj_list,'S':S,'allcount':allcount,'count':count})

@login_required
def LoadSupplierView(request):
    obj_list = SupplierInfo.objects.all()
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
        sheet = ws.add_sheet(u'供应商信息', cell_overwrite_ok=True)
        col_1 = sheet.col(0)  # xlwt中是行和列都是从0开始计算的
        col_2 = sheet.col(1)
        col_3 = sheet.col(2)
        col_4 = sheet.col(3)
        col_5 = sheet.col(4)
        col_6 = sheet.col(5)
        col_7 = sheet.col(6)

        col_1.width = 256 * 40
        col_2.width = 256 * 50
        col_3.width = 256 * 30
        col_4.width = 256 * 40
        col_5.width = 256 * 30
        col_6.width = 256 * 30
        col_7.width = 256 * 40

        sheet.write(0, 0, u'公司名称(必填项)', style_heading)
        sheet.write(0, 1, u'公司地址(必填项)', style_heading)
        sheet.write(0, 2, u'公司电话', style_heading)
        sheet.write(0, 3, u'公司网站', style_heading)
        sheet.write(0, 4, u'联系人(必填项)', style_heading)
        sheet.write(0, 5, u'联系人电话(必填项)', style_heading)
        sheet.write(0, 6, u'联系人邮箱', style_heading)

        excel_row = 1
        for obj in obj_list:
            corporate_name = obj.corporate_name

            corporate_adress=obj.corporate_adress



            if not obj.corporate_phone:
                corporate_phone = ""
            else:
                corporate_phone = obj.corporate_phone

            if not obj.corporate_site:
                corporate_site = ''
            else:
                corporate_site = obj.corporate_site

            contect_name=obj.contect_name
            contect_phone=obj.contect_phone
            if not obj.contect_email:
                contect_email = ""
            else:
                contect_email = obj.contect_email

            sheet.write(excel_row, 0, corporate_name, style_body)
            sheet.write(excel_row, 1, corporate_adress, style_body)
            sheet.write(excel_row, 2, corporate_phone, style_body)
            sheet.write(excel_row, 3, corporate_site, style_body)
            sheet.write(excel_row, 4, contect_name, style_body)
            sheet.write(excel_row, 5, contect_phone, style_body)
            sheet.write(excel_row, 6, contect_email, style_body)

            excel_row += 1
        fname = 'supplier.xls'
        output = StringIO.StringIO()
        ws.save(output)
        output.seek(0)
        response = HttpResponse(output.getvalue(), content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename=%s' % fname
        response.write(output.getvalue())
        return response

@login_required
def UpSupplierView(request):
    username = request.user.username
    if request.method == 'POST':
        form = UpForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                xlsfiles = request.FILES.get('upform', '')
                filename = xlsfiles.name
                fname = os.path.join(settings.MEDIA_ROOT, 'uploads/supplier/%s' % strftime('%Y/%m/%d', localtime()),
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
                        corporate_name = record[0].strip()

                        corporate_adress = record[1].strip()

                        if record[2]:
                            corporate_phone = str(record[2]).strip().rstrip('.0')
                        else:
                            corporate_phone=None

                        if record[3]:
                            corporate_site = record[3].strip()
                        else:
                            corporate_site=None


                        contect_name=record[4].strip()

                        contect_phone = str(record[5]).strip().rstrip('.0')

                        if record[6]:


                            contect_email = record[6].strip()
                        else:
                            contect_email=None

                        asset = SupplierInfo(corporate_name=corporate_name, corporate_adress=corporate_adress, corporate_phone=corporate_phone, corporate_site=corporate_site,
                                             contect_name=contect_name, contect_phone=contect_phone, contect_email=contect_email)
                        asset.save()

                    except AssetDetails.DoesNotExist, e:
                        traceback.print_stack()
                        traceback.print_exc()
                        print e
                successinfo = "上传"
                success = True
                return render_to_response('include/supplierinfo/upsupplierinfo.html', {
                    "title": '导入供应商信息',
                    'form': form,
                    'successinfo': successinfo,
                    'success': success,
                    'username': username}, context_instance=RequestContext(request))
            except Exception, e:
                traceback.print_stack()
                traceback.print_exc()
                print e
        else:
            return render_to_response('include/supplierinfo/upsupplierinfo.html', {
                "title": '导入供应商信息',
                'form': form,
                'username': username}, context_instance=RequestContext(request))
    return render_to_response('include/supplierinfo/upsupplierinfo.html', RequestContext(request))


