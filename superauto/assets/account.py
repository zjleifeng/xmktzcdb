#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2016/11/2 16:40
# @Author  : eric
# @Site    : 
# @File    : account.py
# @Software: PyCharm

from forms import LoginForm
from django.contrib import auth
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth import authenticate,login as auth_login,logout as auth_logout

def userlogin(request):
    error=[]
    if request.method == 'GET':
        form = LoginForm()
        return render_to_response('user_login.html', RequestContext(request, {'form': form, }))
    else:
        form = LoginForm(request.POST)
        if form.is_valid():
            username = request.POST.get('username', '')
            password = request.POST.get('password', '')
            user = auth.authenticate(username=username, password=password)
            if user is not None and user.is_active:
                auth.login(request, user)
                return render_to_response('index.html', RequestContext(request))
            else:

                return render_to_response('user_login.html',
                                          RequestContext(request, {'form': form, 'password_is_wrong': True}))
        else:

            return render_to_response('user_login.html', RequestContext(request, {'form': form,'password_is_None':True }))