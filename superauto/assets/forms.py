#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2016/10/28 10:00
# @Author  : eric
# @Site    : 
# @File    : forms.py
# @Software: PyCharm

from django import forms
from django.contrib.auth.models import User
from bootstrap_toolkit.widgets import BootstrapDateInput,BootstrapTextInput,BootstrapUneditableInput


class Loginform(forms.Form):
    username=forms.CharField(
        required=True,
        label=u'用户名:',
        error_messages={'required':u'请输入用户名'},
        widget=forms.TextInput(
            attrs={
                'placeholder': u"用户名",
            }
        ),
    )

    password=forms.CharField(
        required=True,
        label=u'密码:',
        error_messages={'required':u'请输入密码'},
        widget=forms.PasswordInput(
            attrs={
                'placeholder':u'密码',
            }
        ),

    )

    def clean(self):
        if not self.is_valid():
            raise forms.ValidationError(u'请输入正确的用户名和密码')
        else:
            cleaned_data=super(Loginform,self).clean()
