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



@login_required
def UsersView(request):
    paginate_by=settings.PAGE_NUM
    obj_list=EmployeeUser.objects.all().order_by('id')
    allcount=obj_list.count()
    paginator=Paginator(obj_list,paginate_by)
    page=request.GET.get('page')
    try:
        obj_list=paginator.page(page)
    except PageNotAnInteger:  # 如果请求中的page不是数字,也就是为空的情况下
        obj_list = paginator.page(1)
    except EmptyPage:
        # 如果请求的页码数超出paginator.page_range(),则返回paginator页码对象的最后一页
        obj_list = paginator.page(paginator.num_pages)
    return render(request,'include/employee/users.html',{'obj_list':obj_list,'allcount':allcount})

@login_required
def UserSearchView(request):
    S=request.POST.get('word','')
    users_list=EmployeeUser.objects.filter(Q(engname__contains=S)|Q(chnname__contains=S)|Q(dept__deptname__contains=S))
   # sqlyu= EmployeeUser.objects.filter(Q(engname__contains=S)|Q(chnname__contains=S)|Q(dept__deptname__contains=S)).query
    count=users_list.count()
    allcount=EmployeeUser.objects.all().count()
    paginate_by = settings.PAGE_NUM
    paginator=Paginator(users_list,paginate_by)
    page=request.GET.get('page')
    try:
        users_list=paginator.page(page)
    except PageNotAnInteger:
        users_list=paginator.page(1)
    except EmptyPage:
        users_list=paginator.page(paginator.num_pages)
    return render(request,'include/employee/users.html',{'obj_list':users_list,'count':count,'allcount':allcount})

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
    obj_list=EmployeeUser.objects.get(id=users_id)
    if request.method=='POST':
        form=AddUserForm(request.POST,instance=obj_list)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/users/')
    else:
        form=AddUserForm(instance=obj_list)
        return render(request,'include/employee/edituser.html',{'form':form})


@login_required
def DelUser(request,users_id):
        try:
            obj_list = EmployeeUser.objects.get(id=users_id)
            if request.method == 'POST':
                obj_list.delete()

                return HttpResponseRedirect('/users/')
                #return render_to_response('/users/', RequestContext(request, {'success': success,'obj_list':obj_list}))
            else:

                return render(request,'include/employee/deluser.html',{'obj_list':obj_list})
        except EmployeeUser.DoesNotExist:
            raise PermissionDenied



@login_required
def UpUser(request):
    pass

@login_required
def LoadUser(request):
    pass