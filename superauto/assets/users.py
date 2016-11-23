#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2016/11/8 16:42
# @Author  : eric
# @Site    : 
# @File    : users.py
# @Software: PyCharm


from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from superauto import settings
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.shortcuts import render,render_to_response
from django.db.models import Q
from django.http import HttpResponseRedirect,HttpResponse
from assets.models import EmployeeUser
from django.core.exceptions import PermissionDenied
from forms import AddUserForm
from assets.models import Dept,UserStatus
from xlwt import *
import StringIO
from assets.forms import UpForm
import os
from time import strftime,localtime
import xlrd
import traceback
import time
import datetime


@login_required
def UsersView(request):
    paginate_by=settings.PAGE_NUM
    user_list=EmployeeUser.objects.all().order_by('id')
    obj_list=[]
    for obj in user_list:
        if obj.delstatus==0:
            obj_list.append(obj)

    allcount=len(obj_list)

    paginator=Paginator(obj_list,paginate_by)
    page=request.GET.get('page')
    dept_list=Dept.objects.all()
    status_list=UserStatus.objects.all()

    try:
        obj_list=paginator.page(page)
    except PageNotAnInteger:  # 如果请求中的page不是数字,也就是为空的情况下
        obj_list = paginator.page(1)
    except EmptyPage:
        # 如果请求的页码数超出paginator.page_range(),则返回paginator页码对象的最后一页
        obj_list = paginator.page(paginator.num_pages)
    return render(request,'include/employee/users.html',{'obj_list':obj_list,'dept_list':dept_list,'status_list':status_list,'allcount':allcount})

@login_required
def UserSearchView(request):
    S=request.GET.get('word','')
    WT=request.GET.get('wordd','')
    WB=request.GET.get('words','')
    if 'S' in request.GET and request.GET['S']:
        S = request.GET['S']
    if 'WT' in request.GET and request.GET['WT']:
        WT = request.GET['WT']
    if 'WB' in request.GET and request.GET['WB']:
        WB = request.GET['WB']

    dept_list=Dept.objects.all()
    status_list=UserStatus.objects.all()
    if not WT and not WB:
        users_list = EmployeeUser.objects.filter(
            (Q(engname__icontains=S) | Q(chnname__icontains=S)))
    elif not WT:
        users_list=EmployeeUser.objects.filter((Q(engname__icontains=S)| Q(chnname__icontains=S)) &Q(status__status__iexact=WB))
    elif not WB:
        users_list = EmployeeUser.objects.filter(
            (Q(engname__icontains=S) | Q(chnname__icontains=S)) & Q(dept__deptname__iexact=WT))
    else:
        users_list = EmployeeUser.objects.filter(
            (Q(engname__icontains=S) | Q(chnname__icontains=S)) & Q(dept__deptname__iexact=WT) & Q(
                status__status__iexact=WB))


    #sqlyu = EmployeeUser.objects.filter(Q(engname__contains=S) | Q(chnname__contains=S) & Q(dept__deptname__contains=D))


    allcount=EmployeeUser.objects.all().count()

    obj_list=[]
    for obj in users_list:
        if obj.delstatus==0:
            obj_list.append(obj)
    count=len(obj_list)

    paginate_by = settings.PAGE_NUM
    paginator=Paginator(users_list,paginate_by)
    page=request.GET.get('page')
    try:
        users_list=paginator.page(page)
    except PageNotAnInteger:
        users_list=paginator.page(1)
    except EmptyPage:
        users_list=paginator.page(paginator.num_pages)
    return render(request,'include/employee/users.html',{'obj_list':users_list,'S':S,'WT':WT,'WB':WB,'dept_list':dept_list,'status_list':status_list,'count':count,'allcount':allcount})

@login_required
def AddUser(request):
    if request.method=='GET':
        form=AddUserForm
        return render_to_response('include/employee/adduser.html',RequestContext(request,{'form':form}))
    else:
        form=AddUserForm(request.POST)
        if form.is_valid():
            form.save()

            return HttpResponseRedirect('/users/')
        else:
            form=AddUserForm
            return render(request,'include/employee/adduser.html',{'form':form})


@login_required
def EditUser(request,users_id):
    try:
        obj_list=EmployeeUser.objects.get(id=users_id)
        if request.method=='POST':
            form=AddUserForm(request.POST,instance=obj_list)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/users/')
        else:
            form=AddUserForm(instance=obj_list)
            return render(request,'include/employee/edituser.html',{'form':form})
    except EmployeeUser.DoesNotExist:
        raise PermissionDenied

@login_required
def DelUser(request,users_id):
        try:
            obj_list = EmployeeUser.objects.get(id=users_id)
            if request.method == 'POST':
                obj_list.delstatus=1
                obj_list.save()

                return HttpResponseRedirect('/users/')
                #return render_to_response('/users/', RequestContext(request, {'success': success,'obj_list':obj_list}))
            else:

                return render(request,'include/employee/deluser.html',{'obj_list':obj_list})
        except EmployeeUser.DoesNotExist:
            raise PermissionDenied



@login_required
def LoadUser(request):

        obj_list=EmployeeUser.objects.all().order_by('id')
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
            ws=Workbook(encoding='utf-8')
            sheet=ws.add_sheet(u'员工表',cell_overwrite_ok=True)

            col_1 = sheet.col(0)  # xlwt中是行和列都是从0开始计算的
            col_2 = sheet.col(1)
            col_3 = sheet.col(2)
            col_4 = sheet.col(3)
            col_5 = sheet.col(4)
            col_6 = sheet.col(5)
            col_7 = sheet.col(6)
            col_8 = sheet.col(7)

            col_1.width = 256 * 20
            col_2.width = 256 * 20
            col_3.width = 256 * 20
            col_4.width = 256 * 20
            col_5.width = 256 * 40
            col_6.width = 256 * 20
            col_7.width = 256 * 20
            col_8.width = 256 * 20



            sheet.write(0, 0, u'英文名',style_heading)
            sheet.write(0, 1, u'中文名',style_heading)
            sheet.write(0, 2, u'分机号',style_heading)
            sheet.write(0, 3, u'部门',style_heading)
            sheet.write(0, 4, u'邮箱',style_heading)
            sheet.write(0, 5, u'手机',style_heading)
            sheet.write(0, 6, u'状态',style_heading)
            sheet.write(0, 7, u'入职时间',style_heading)

            #写入数据
            excel_row=1
            for obj in obj_list:
                engname=obj.engname
                chnname=obj.chnname
                extnum=(obj.extnum)
                dept=obj.dept.deptname
                email=obj.email
                phonenum=str(obj.phonenum)

                status_obj=obj.status
                if not status_obj:
                    status=" "
                else:
                    status=obj.status.status


                if not obj.entry_time:
                    entry_time=" "
                else:
                    #tt=time.strftime(obj.entry_time,"%Y/%m/%d")
                    entry_time=obj.entry_time.strftime("%Y/%m/%d")
                    timeArray = time.strptime(entry_time, "%Y/%m/%d")
                    #xx=entry_time.strftime("%Y-%m-%d");
                    #xx=time.strptime("%Y/%m/%d", entry_time)



                sheet.write(excel_row, 0, engname,style_body)
                sheet.write(excel_row, 1, chnname, style_body)
                sheet.write(excel_row, 2, extnum, style_body)
                sheet.write(excel_row, 3, dept, style_body)
                sheet.write(excel_row, 4, email, style_body)
                sheet.write(excel_row, 5, phonenum, style_body)
                sheet.write(excel_row, 6, status, style_body)
                sheet.write(excel_row, 7, entry_time,style)
                excel_row += 1

            fname='usersfile.xls'
            agent = request.META.get('HTTP_USER_AGENT')
            output=StringIO.StringIO()
            ws.save(output)
            output.seek(0)
            response = HttpResponse(output.getvalue(), content_type='application/vnd.ms-excel')
            response['Content-Disposition'] = 'attachment; filename=%s' % fname
            response.write(output.getvalue())
            return response


@login_required
def UpUser(request):
    username = request.user.username
    if request.method=='POST':
        form = UpForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                xlsfiles = request.FILES.get('upform', '')
                filename = xlsfiles.name
                # 创建文件存储路径
                fname=os.path.join(settings.MEDIA_ROOT, 'uploads/users/%s' % strftime("%Y/%m/%d", localtime()),filename)
                if os.path.exists(fname):
                    os.remove(fname)
                dirs = os.path.dirname(fname)
                if not os.path.exists(dirs):
                    os.makedirs(dirs)
                # 写入文件
                if os.path.isfile(fname):
                    os.remove(fname)
                content = xlsfiles.read()
                fp = open(fname, 'wb')
                fp.write(content)
                fp.close()

                # 格式化数据保存到数据库
                book = xlrd.open_workbook(fname)
                sheet = book.sheet_by_index(0)
                for row_index in range(1,sheet.nrows):
                    record = sheet.row_values(row_index, 0)
                    try:
                        engname = record[0].strip()
                        chnname = record[1].strip()
                        extnum = str(record[2]).rstrip(".0")

                        dp = record[3].strip()
                        try:
                            deptid=Dept.objects.get(deptname=dp)
                        except Dept.DoesNotExist,e:
                            traceback.print_stack()
                            traceback.print_exc()
                        #deptid = Dept.objects.get(deptname=dp)
                        email = record[4].strip()
                        phonenum = str(record[5]).rstrip(".0")
                        status_obj = record[6].strip()
                        if status_obj:
                            try:
                                status_id=UserStatus.objects.get(status=status_obj)
                            except UserStatus.DoesNotExist:
                                traceback.print_stack()
                                traceback.print_exc()
                        else:
                            status_id=None

                        e_date=record[7]
                        if e_date:
                            tp=type(e_date)
                            if tp==float:

                                entry_time = xlrd.xldate.xldate_as_datetime(record[7],0)
                                #mk=type(entry_time)
                            elif tp==unicode:
                                #s=e_date.split('/')
                                entry_time=datetime.datetime.strptime(e_date,'%Y/%m/%d')
                                #entry_time=datetime.datetime(s[0],s[1],s[2])
                                #mk = type(entry_time)


                            #datetimeObj = entry_time
                        else:
                            entry_time=None

                        users = EmployeeUser(engname=engname, chnname=chnname,extnum=extnum,dept=deptid,email=email,phonenum=phonenum,status=status_id,entry_time=entry_time)

                        users.save()
                    except EmployeeUser.DoesNotExist, e:
                        traceback.print_stack()
                        traceback.print_exc()
                        print e
                successinfo = "上传"
                success = True
                return render_to_response('include/employee/upuser.html', {
                    "title": '导入员工信息',
                    'form': form,
                    'successinfo': successinfo,
                    'success': success,
                    'username': username}, context_instance=RequestContext(request))
            except Exception, e:
                traceback.print_stack()
                traceback.print_exc()
                print e
        else:
            return render_to_response('include/employee/upuser.html', {
                "title": '导入员工信息',
                'form': form,
                'username': username}, context_instance=RequestContext(request))


    return render_to_response('include/employee/upuser.html', RequestContext(request))