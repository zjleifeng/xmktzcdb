#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2016/11/14 13:51
# @Author  : eric
# @Site    : 
# @File    : assetdetails.py
# @Software: PyCharm

from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
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
from forms import AddAssetDetailsForm
from assets.models import AssetDetails,AssetType,AssetBrands,AssetStatus,EmployeeUser,UserRecord,RecordStatus,AssetInfo
from django.views.generic import View, TemplateView, ListView, DetailView
from django import template
from django.template import Context, loader
import json


from functools import wraps
from flask import Flask
from assets.page_paginator import XmktPaginator


def get_pageinatior(func):
    def page_pageinatior(*args, **kwargs):
        reg = func(*args, **kwargs)
        paginate_by = settings.PAGE_NUM
        paginator = Paginator(reg[1], paginate_by)
        page = reg[0].request.GET.get('page')

        try:
            reg = paginator.page(page)
        except PageNotAnInteger:
            reg = paginator.page(1)
        except EmptyPage:
            reg = paginator.page(paginator.num_pages)

        return reg

    return page_pageinatior


class BaseMixin(object):


    def get_context_data(self,*args,**kwargs):
        context=super(BaseMixin,self).get_context_data(*args,**kwargs)
        try:
            if self.request.META.has_key('HTTP_X_FORWARDED_FOR'):
                ip = self.request.META['HTTP_X_FORWARDED_FOR']
            else:
                ip = self.request.META['REMOTE_ADDR']
            context['ip_adress'] = ip

        except Exception as e:
            pass

        return context

class AssetDetailsView(BaseMixin,ListView):
    template_name = 'include/assetdetails/assetdetails.html'
    context_object_name = 'obj_list'

    #@method_decorator(login_required)
    def get_context_data(self,*args,**kwargs):
        kwargs['assettype_list']=AssetType.objects.all()
        kwargs['assetbrand_list']=AssetBrands.objects.all()
        kwargs['assetstatus_list']=AssetStatus.objects.all()

        return super(AssetDetailsView,self).get_context_data( *args,**kwargs)

    @get_pageinatior
    def get_queryset(self):
        obj_list=AssetDetails.objects.filter(delstatus=0)

        return self,obj_list

    """
    def post(self, request, *args, **kwargs):
        obj_list = AssetDetails.objects.filter(delstatus=0)

        html = ''
        for asset in obj_list:
            html += template.loader.get_template(
                'include/assetdetails/all_details'
            ).render(template.Context({'post': asset}))

        mydict = {"html": html}
        return HttpResponse(
            json.dumps(mydict),
            content_type="application/json"
        )

@login_required
def AssetDetailsView1(request):

    assetdetails_list=AssetDetails.objects.all().order_by('itno')

    type(assetdetails_list)
    obj_list=[]
    count_list=[]
    if assetdetails_list:
        for obj in assetdetails_list:
            if obj.delstatus==0:
                count_list.append(UserRecord.objects.filter(Q(itno__itno__iexact=obj.itno)).count())
                b = AssetDetails.objects.get(itno=obj.itno)
                xx=b.userrecord_set.all().count()

                obj_list.append(obj)


    allcount=len(obj_list)
    assettype_list=AssetType.objects.all()
    assetbrand_list=AssetBrands.objects.all()
    assetstatus_list=AssetStatus.objects.all()

    xxx=UserRecord.itno.itno_set.all()

    paginate_by=settings.PAGE_NUM
    paginator=Paginator(obj_list,paginate_by)
    page=request.GET.get('page')
    try:
        obj_list=paginator.page(page)
    except PageNotAnInteger:
        obj_list=paginator.page(1)
    except EmptyPage:
        obj_list=paginator.page(paginator.num_pages)
    return render(request,'include/assetdetails/assetdetails.html',{'obj_list':obj_list,'allcount':allcount,'assettype_list':assettype_list,'assetbrand_list':assetbrand_list,'assetstatus_list':assetstatus_list})
"""
#使用记录查询
@login_required
def Record_search(request,itno_id):
    assetid=AssetDetails.objects.get(id=itno_id)
    itno=assetid.itno
    record_list=UserRecord.objects.filter(Q(itno__itno__iexact=itno))

    assetdetail_list = AssetDetails.objects.all()
    users_list = EmployeeUser.objects.all()
    recordtype_list = RecordStatus.objects.all()
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

    return render(request,'include/userecord/userecord.html',{'obj_list':obj_list,'allcount':allcount, 'assetdetail_list': assetdetail_list,'users_list':users_list,'recordtype_list':recordtype_list})


#配置信息查询
def Asset_Search(request,info_id):
    try:
        obj_list=AssetInfo.objects.filter(id=info_id)
    except AssetInfo.DoesNotExist:
        pass
    allcount=AssetInfo.objects.all().count()
    sel_list = AssetInfo.objects.all()
    return render(request,'include/assetinfo/assetinfo.html',{'obj_list': obj_list, 'allcount': allcount,'sel_list':sel_list})

@login_required
def AssetDetailsSearchView(request):

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

    sS=(Q(itno__contains=S)|Q(version__contains=S)|Q(where__engname__contains=S))
    sWT=Q(assettype__assettype__iexact=WT)
    sWB=Q(brands__assetbrands__iexact=WB)
    sWS=Q(status__assettatus__iexact=WS)

    if not WT and not WB and not WS:
        sql=sS

      #  obj_list=AssetDetails.objects.filter(Q(itno__contains=S)|Q(version__contains=S)|Q(where__engname__contains=S))
    elif not WT:
        if not WB:
            sql=sS & sWS
        #    obj_list = AssetDetails.objects.filter(
        #        (Q(itno__contains=S) | Q(version__contains=S) | Q(where__engname__contains=S))&Q(status__assettatus__iexact=WS))
        elif not WS:
            sql = sS & sWB
       #     obj_list = AssetDetails.objects.filter(
       #         (Q(itno__contains=S) | Q(version__contains=S) | Q(where__engname__contains=S))&Q(brands__assetbrands__iexact=WB))
        else:
            sql = sS & sWS & sWB
       #     obj_list = AssetDetails.objects.filter(
        #        (Q(itno__contains=S) | Q(version__contains=S) | Q(where__engname__contains=S)) & Q(
        #            brands__assetbrands__iexact=WB)&Q(status__assettatus__iexact=WS))

    elif not WB:
        if not WS:
            sql = sS & sWT
        #    obj_list = AssetDetails.objects.filter(
        #        (Q(itno__contains=S) | Q(version__contains=S) | Q(where__engname__contains=S)) & Q(
        #            assettype__assettype__iexact=WT))
        else:
            sql = sS & sWS &sWT
        #    obj_list = AssetDetails.objects.filter(
        #        (Q(itno__contains=S) | Q(version__contains=S) | Q(where__engname__contains=S)) & Q(
         #           assettype__assettype__iexact=WT)& Q(status__assettatus__iexact=WS))
    elif not WS:
        sql = sS & sWB & sWT
        #obj_list = AssetDetails.objects.filter(
        #    (Q(itno__contains=S) | Q(version__contains=S) | Q(where__engname__contains=S)) & Q(
         #       assettype__assettype__iexact=WT) & Q(brands__assetbrands__iexact=WB))

    else:
        sql = sS & sWS & sWB & sWT
        #obj_list = AssetDetails.objects.filter((Q(itno__contains=S) | Q(version__contains=S) | Q(where__engname__contains=S)) & (Q(assettype__assettype__iexact=WT) & Q(brands__assetbrands__iexact=WB) & Q(status__assettatus__iexact=WS)))

    obj_list=AssetDetails.objects.filter(sql)



    #obj_list=AssetDetails.objects.filter((Q(itno__contains=S)|Q(version__contains=S)|Q(where__engname__contains=S)),assettype__assettype__iexact=WT)
    #SQ=AssetDetails.objects.filter((Q(itno__contains=S)|Q(version__contains=S)|Q(where__engname__contains=S))&(Q(assettype__assettype__iexact=WT)&Q(brands__assetbrands__iexact=WB)&Q(status__assettatus__iexact=WS))).query

    count=obj_list.count()
    allcount=AssetDetails.objects.all().count()

    assettype_list=AssetType.objects.all()
    assetbrand_list=AssetBrands.objects.all()
    assetstatus_list=AssetStatus.objects.all()
    paginate_by = settings.PAGE_NUM
    paginator = Paginator(obj_list, paginate_by)
    page = request.GET.get('page')
    try:
        obj_list = paginator.page(page)
    except PageNotAnInteger:
        obj_list = paginator.page(1)
    except EmptyPage:
        obj_list = paginator.page(paginator.num_pages)
    return render(request,'include/assetdetails/assetdetails.html',{'obj_list':obj_list,'S':S,'WT':WT,'WB':WB,'WS':WS,'assettype_list':assettype_list,'assetbrand_list':assetbrand_list,'assetstatus_list':assetstatus_list,'count':count,'allcount':allcount})

@login_required
def AddAssetDetailsView(request):
    if request.method=='GET':

        form = AddAssetDetailsForm
        return render_to_response('include/assetdetails/addassetdetails.html', RequestContext(request, {'form': form}))
    else:
        form = AddAssetDetailsForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/assetdetails/')
        else:
            form = AddAssetDetailsForm
            return render(request, 'include/assetdetails/addassetdetails.html', {'form': form})
    #return render_to_response('include/assetdetails/addassetdetails.html', RequestContext(request, {'form': form}))

@login_required
def EditAssetDetailsView(request,asset_id):
    try:
        obj_list=AssetDetails.objects.get(id=asset_id)
        if request.method=='POST':
            form=AddAssetDetailsForm(request.POST,instance=obj_list)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/assetdetails/')
        else:
            form=AddAssetDetailsForm(instance=obj_list)
            return render(request,'include/assetdetails/editassetdetails.html',{'form':form})
    except AssetDetails.DoesNotExist:
        raise PermissionDenied

@login_required
def DelAssetDetailsView(request,asset_id):
    try:
        obj_list=AssetDetails.objects.get(id=asset_id)
        if request.method=='POST':
            obj_list.delstatus=1
            obj_list.save()
            return HttpResponseRedirect('/assetdetails/')
        else:
            return render(request,'include/assetdetails/editassetdetails.html',{'obj_list':obj_list})
    except AssetDetails.DoesNotExist:
        raise PermissionDenied


@login_required
def LoadAssetDetailsView(request):
    obj_list=AssetDetails.objects.all().order_by('itno')
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

    if obj_list:
        ws=Workbook(encoding='utf-8')
        sheet=ws.add_sheet(u'资产列表',cell_overwrite_ok=True)
        col_1 = sheet.col(0)  # xlwt中是行和列都是从0开始计算的
        col_2 = sheet.col(1)
        col_3 = sheet.col(2)
        col_4 = sheet.col(3)
        col_5 = sheet.col(4)
        col_6 = sheet.col(5)
        col_7 = sheet.col(6)

        col_1.width = 256 * 40
        col_2.width = 256 * 40
        col_3.width = 256 * 20
        col_4.width = 256 * 20
        col_5.width = 256 * 20
        col_6.width = 256 * 20
        col_7.width = 256 * 30


        sheet.write(0,0,u'资产编号',style_heading)
        sheet.write(0,1,u'财务资产编号',style_heading)
        sheet.write(0,2,u'资产类型',style_heading)
        sheet.write(0,3,u'品牌',style_heading)
        sheet.write(0,4,u'型号',style_heading)
        sheet.write(0,5,u'状态',style_heading)
        sheet.write(0,6,u'使用者或存放点',style_heading)

        excel_row=1
        for obj in obj_list:
            itno=obj.itno
            if not obj.financeno:
                financeno=""
            else:
                financeno=obj.financeno


            if not obj.assettype:
                assettype=""
            else:
                assettype = obj.assettype.assettype


            if not obj.brands:
                brands=""
            else:
                brands = obj.brands.assetbrands

            version=obj.version


            if not obj.status:
                status=""
            else:
                status = obj.status.assettatus


            if not obj.where:
                where="IT"
            else:
                where = obj.where.engname

            sheet.write(excel_row,0,itno,style_body)
            sheet.write(excel_row,1,financeno,style_body)
            sheet.write(excel_row,2,assettype,style_body)
            sheet.write(excel_row,3,brands,style_body)
            sheet.write(excel_row,4,version,style_body)
            sheet.write(excel_row,5,status,style_body)
            sheet.write(excel_row,6,where,style_body)

            excel_row+=1
        fname='assetdetailfile.xls'
        output=StringIO.StringIO()
        ws.save(output)
        output.seek(0)
        response = HttpResponse(output.getvalue(), content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename=%s' % fname
        response.write(output.getvalue())
        return response





@login_required
def UpAssetDetailsView(request):
    username=request.user.username
    if request.method=='POST':
        form=UpForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                xlsfiles=request.FILES.get('upform','')
                filename = xlsfiles.name
                fname=os.path.join(settings.MEDIA_ROOT,'uploads/assetdetails/%s'% strftime('%Y/%m/%d',localtime()),filename)
                if os.path.exists(fname):
                    os.remove(fname)
                dirs=os.path.dirname(fname)
                if not os.path.exists(dirs):
                    os.makedirs(dirs)

                if os.path.isfile(fname):
                        os.remove(fname)
                content=xlsfiles.read()
                fp = open(fname, 'wb')
                fp.write(content)
                fp.close()


                book=xlrd.open_workbook(fname)
                sheet=book.sheet_by_index(0)
                for row_index in range(1,sheet.nrows):
                    record=sheet.row_values(row_index,0)
                    try:
                        itno=record[0].strip().rstrip(".0")

                        financeno=str(record[1]).strip().rstrip(".0")


                        assettype=record[2].strip()
                        if assettype:
                            try:
                                assettypeid=AssetType.objects.get(assettype=assettype)
                            except AssetType.DoesNotExist:
                                pass
                        else:
                            assettypeid=None

                        brands=record[3].strip()
                        if brands:
                            try:
                                brandsid=AssetBrands.objects.get(assetbrands=brands)
                            except AssetBrands.DoesNotExist:
                                pass
                        else:
                            brandsid=None

                        version=record[4].strip()

                        status=record[5].strip()
                        if status:
                            try:
                                statusid=AssetStatus.objects.get(assettatus=status)
                            except AssetBrands.DoesNotExist:
                                pass
                        else:
                            statusid=None

                        where=record[6].strip()
                        if where and where!="IT":
                            try:
                                whereid=EmployeeUser.objects.get(engname=where)
                            except EmployeeUser.DoesNotExist:
                                pass
                        else:
                            whereid=None

                        asset=AssetDetails(itno=itno,financeno=financeno,assettype=assettypeid,brands=brandsid,version=version,status=statusid,where=whereid)
                        asset.save()

                    except AssetDetails.DoesNotExist, e:
                        traceback.print_stack()
                        traceback.print_exc()
                        print e
                successinfo = "上传"
                success = True
                return render_to_response('include/assetdetails/upassetdetails.html', {
                    "title": '导入资产列表',
                    'form': form,
                    'successinfo': successinfo,
                    'success': success,
                    'username': username}, context_instance=RequestContext(request))
            except Exception, e:
                traceback.print_stack()
                traceback.print_exc()
                print e
        else:
            return render_to_response('include/assetdetails/upassetdetails.html', {
                "title": '导入资产列表',
                'form': form,
                'username': username}, context_instance=RequestContext(request))
    return render_to_response('include/assetdetails/upassetdetails.html', RequestContext(request))





