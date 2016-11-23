#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2016/10/28 10:00
# @Author  : eric
# @Site    : 
# @File    : forms.py
# @Software: PyCharm

from django import forms
from fields import UsernameField,PasswordField
from django.contrib.auth import authenticate,login
from django.forms import ModelForm
from assets.models import Dept,EmployeeUser,AssetDetails,AssetInfo,UserRecord
from django.contrib.auth.models import User
from bootstrap_toolkit.widgets import BootstrapDateInput,BootstrapTextInput,BootstrapUneditableInput

from django.contrib.admin import widgets


"""
class LoginForm(forms.Form):
    username=UsernameField(required=True,max_length=12,min_length=6)
    password = PasswordField(required=True, max_length=12, min_length=6)

    def __init__(self,request=None,*args,**kwargs):
        self.request=request
        self.user_cache = None
        super(LoginForm,self.__init__(*args,**kwargs))

    def clean(self):
        username=self.cleaned_data.get('username')
        password=self.cleaned_data.get('password')
        if username and password:
            self.user_cache=authenticate(username=username,password=password)
            if self.user_cache is None:
                raise forms.ValidationError(U'用户名或者密码错误')
            elif not self.user_cache.is_active or not self.user_cache.is_staff:
                raise forms.ValidationError(u'用户名或者密码错误')
            else:
                login(self.request,self.user_cache)
        return self.user_cache


    def get_user_id(self):
        if self.user_cache:
            return self.user_cache.id
        return None

    def get_user(self):
        return self.user_cache




"""
class LoginForm(forms.Form):
    username=forms.CharField(
        required=True,

        error_messages={'required':u'请输入用户名'},
        widget=forms.TextInput(
            attrs={
                'class':'form-group form-control span12',
                'placeholder': u"用户名",
            }
        ),
    )

    password=forms.CharField(
        required=True,

        error_messages={'required':u'请输入密码'},
        widget=forms.PasswordInput(
            attrs={
                'class':'form-group form-controlspan12 form-control',
                'placeholder':u'密码',
            }
        ),

    )

    def clean(self):
        if not self.is_valid():
            raise forms.ValidationError(u'请输入正确的用户名和密码')
        else:
            cleaned_data=super(LoginForm,self).clean()



class AddDeptForm(ModelForm):
    class Meta:
        model=Dept
        fields=('deptname','parentdept')
        widgets = {
            'deptname': forms.TextInput(attrs={'class': 'form-control'}),


        }



class DeptModelForm(ModelForm):
    class Meta:
        model=Dept
        exclude=()


class UpForm(forms.Form):
    upform = forms.FileField(required=True,error_messages={
        'required':u'必须选择一个导入文件',
        'invalid':u'上传文件是以xls结尾的excel'})

class UpUserForm(forms.Form):
    userform=forms.FileField(required=True,error_messages={
        'required': u'必须选择一个导入文件',
        'invalid': u'上传文件是以xls结尾的excel'})


class AddUserForm(ModelForm):
    """
    def __init__(self, *args, **kwarg):
        super(AddUserForm, self).__init__(*args,**kwarg)
        self.fields['entry_time']=forms.DateField(widget=widgets.AdminDateWidget(), label=u'入职日期')
"""
    #entry_time = forms.DateField(widget=widgets.AdminDateWidget(), label=u'入职日期')
    class Meta:
        model=EmployeeUser
        fields=('engname','chnname','extnum','phonenum','email','status','entry_time','dept')
        widgets={
            #'entry_time':widgets.AdminDateWidget()
            "entry_time":forms.TextInput(attrs={"class":"laydate-icon","onclick":"laydate()"})
        }
    #def clean_entry_time(self):
        #entry_time=forms.DateField(widget=widgets.AdminDateWidget(), label=u'入职日期')


class AddAssetDetailsForm(ModelForm):
    class Meta:
        model=AssetDetails
        fields=('itno','financeno','assettype','brands','version','status','where','configinfo')

class AddAssetinfoForm(ModelForm):
    class Meta:
        model=AssetInfo
        fields=('__all__')


class AddRecordForm(ModelForm):
    class Meta:
        model=UserRecord
        fields=('__all__')

