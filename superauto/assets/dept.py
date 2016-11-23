#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2016/11/3 14:19
# @Author  : eric
# @Site    : 
# @File    : dept.py
# @Software: PyCharm

from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from superauto import settings
from assets.models import Dept
from forms import AddDeptForm
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response,render,redirect
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.core.exceptions import PermissionDenied
from django.db.models import Q

@login_required
def DeptView(request):
    paginate_by = settings.PAGE_NUM
    dept_list=Dept.objects.all().order_by('id')
    obj_list = []
    for obj in dept_list:
        if obj.delstatus == 0:
            obj_list.append(obj)

    paginator = Paginator(obj_list, paginate_by)
    page = request.GET.get('page')

    obj_list=[]
    for obj in dept_list:
        if obj.delstatus==0:
            obj_list.append(obj)


    try:
        obj_list = paginator.page(page)  # 返回用户请求的页码对象
    except PageNotAnInteger:  # 如果请求中的page不是数字,也就是为空的情况下
        obj_list = paginator.page(1)
    except EmptyPage:
        # 如果请求的页码数超出paginator.page_range(),则返回paginator页码对象的最后一页
        obj_list = paginator.page(paginator.num_pages)

    return render(request, 'include/dept/dept.html', {'obj_list': obj_list})

    #return render_to_response('include/dept.html', locals())


@login_required
def DeptSearchView(request):
    #if request.method=='POST':

        S=request.GET.get('word','')
        dept_list=Dept.objects.filter(Q(deptname__icontains=S))
        if 'S' in request.GET and request.GET['S']:
            S = request.GET['S']


        paginate_by = settings.PAGE_NUM
        paginator = Paginator(dept_list, paginate_by)
        page = request.GET.get('page')
        try:
            dept_list = paginator.page(page)  # 返回用户请求的页码对象
        except PageNotAnInteger:  # 如果请求中的page不是数字,也就是为空的情况下
            dept_list = paginator.page(1)
        except EmptyPage:
        # 如果请求的页码数超出paginator.page_range(),则返回paginator页码对象的最后一页
            dept_list = paginator.page(paginator.num_pages)
        return render(request, 'include/dept/dept.html', {'obj_list': dept_list})




@login_required
def AddDept(request):
    if request.method=='GET':
        form=AddDeptForm
        return render_to_response('include/dept/adddept.html', RequestContext(request, {'form': form, }))
    else:
        form=AddDeptForm(request.POST)
        if form.is_valid():
            deptinfo = form.save()
            deptinfo.save()
            return HttpResponseRedirect('/dept/')
        else:
            form = AddDeptForm()
            return render(request, 'include/dept/adddept.html', {'form': form})


"""
@login_required
def EditDept(request):


    if request.method=='POST':
        dept_obj = Dept.objects.get()
        form=AddDeptForm(request.POST)
        if form.is_valid():
            form.update()
            success=True
            successinfo='修改'
            return HttpResponseRedirect('/dept/')
        else:
            form=AddDeptForm()
        return render(request, 'include/dept/editdept.html', {'form': form})
"""
@login_required
def EditDept_detail(request,dept_id):

    dept_obj = Dept.objects.get(id=dept_id)
    if request.method=='POST':

        form = AddDeptForm(request.POST,instance=dept_obj)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/dept/')
    else:
        form=AddDeptForm(instance=dept_obj)
        return render(request, 'include/dept/editdept.html', {'form': form})

@login_required
def DelDept_detail(request,did):
    #did=request.POST.get('deldeptid','')
    try:
        deldept_list=Dept.objects.get(id=did)
        if request.method=='POST':
            deldept_list.delstatus=1
            deldept_list.save()
            return HttpResponseRedirect('/dept/')
        else:
            return render(request, 'include/dept/deldept.html', {'deldept_list':deldept_list})

    except Dept.DoesNotExist:
        raise PermissionDenied