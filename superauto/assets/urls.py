#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2016/10/27 13:40
# @Author  : eric
# @Site    : 
# @File    : urls.py
# @Software: PyCharm

from django.conf.urls import *
from django.contrib import admin
from assets import views
from assets.views import index
from assets.dept import EditDept_detail
from assets.users import UserSearchView
from django.views.generic.base import RedirectView
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView, DetailView
from assets.assetdetails import AssetDetailsView,Record_search
from django.contrib.auth.decorators import login_required

urlpatterns = [
    #(r'^accounts/', include('userena.urls')),



    url(r'^$',index),
    url(r'^accounts/login/$', 'assets.account.userlogin', name="userlogin"),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout',
        {'next_page': '/accounts/login/'}, name="userlogout"),
    url(r'^accounts/changepwd/$', 'assets.views.changepwd',name='changepwd'),

    url(r'^forgetpassword/$','assets.views.forgetpassword',name='forgetpassword-view'),

    url(r'^resetpassword/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$',
            'assets.views.resetpassword',
                name='resetpassword-view'),

    #url(r'^usercontrol/(?P<slug>\w+)$', UserControl.as_view()),
    url(r'^syscolor/$', 'assets.views.syscolor'),

    url(r'^dept/$','assets.dept.DeptView',name='dept-view'),
    url(r'^adddept/$','assets.dept.AddDept',name='adddept-view'),
    #url(r'^editdept/$','assets.dept.EditDept',name='editdept-view'),
    url(r'^dept/(\d+)/$', EditDept_detail,name='editdept-view'),
    url(r'^deldept/(\d+)/$', 'assets.dept.DelDept_detail', name='deldept-view'),
    url(r'^deptsearch/$', 'assets.dept.DeptSearchView',name='deptsearch-view'),
    url(r'^xlwtdept/$', 'assets.upxlwt.dept_xlwt',name='xlwtdept-view'),
    #url(r'^xlrddept/$', 'assets.upxlwt.dept_xlrd',name='xlrddept-view'),
    url(r'^updept/$', 'assets.upxlwt.deptup',name='updept-view'),

    url(r'^users/$', 'assets.users.UsersView',name='users-view'),
    url(r'^usersearch/$', UserSearchView,name='usersearch-view'),
    url(r'^adduser/$','assets.users.AddUser',name='adduser-view'),
    #url(r'^edituser/$','assets.users.EditUser',name='edituser-view'),
    url(r'^users/(\d+)/$','assets.users.EditUser',name='edituser-view'),
    url(r'^delusers/(\d+)/$', 'assets.users.DelUser'),
    url(r'^upuser/$', 'assets.users.UpUser',name='upuser-view'),
    url(r'^loaduser/$', 'assets.users.LoadUser',name='loaduser-view'),

    #url(r'^assetdetails/$',AssetDetailsView.as_view() ,name='assetdetails-view'),
    url(r'^assetdetails/$',login_required(AssetDetailsView.as_view()),name='assetdetails-view'),
    url(r'^assetdetailssearch/$', 'assets.assetdetails.AssetDetailsSearchView',name='assetdetailssearch-view'),
    url(r'^addassetdetails/$','assets.assetdetails.AddAssetDetailsView',name='addassetdetails-view'),
    #url(r'^edituser/$','assets.users.EditUser',name='edituser-view'),
    url(r'^assetdetails/(\d+)/$','assets.assetdetails.EditAssetDetailsView',name='editassetdetails-view'),
    url(r'^delassetdetails/(\d+)/$', 'assets.assetdetails.DelAssetDetailsView',name='delassetdetails-view'),
    url(r'^upassetdetails/$', 'assets.assetdetails.UpAssetDetailsView',name='upassetdetails-view'),
    url(r'^loadassetdetails/$', 'assets.assetdetails.LoadAssetDetailsView',name='loadassetdetails-view'),

    url(r'^assetinfo/$', 'assets.assetinfo.AssetinfoView',name='assetinfo-view'),
    url(r'^assetinfosearch/$', 'assets.assetinfo.AssetinfoSearchView',name='assetinfosearch-view'),
    url(r'^addassetinfo/$','assets.assetinfo.AddAssetinfoView',name='addassetinfo-view'),
    #url(r'^edituser/$','assets.users.EditUser',name='edituser-view'),
    url(r'^assetinfo/(\d+)/$','assets.assetinfo.EditAssetinfoView',name='assetinfo-view'),
    url(r'^delassetinfo/(\d+)/$', 'assets.assetinfo.DelAssetinfoView',name='delassetinfo-view'),
    url(r'^upassetinfo/$', 'assets.assetinfo.UpAssetinfoView',name='upassetinfo-view'),
    url(r'^loadassetinfo/$', 'assets.assetinfo.LoadAssetinfoView',name='loadassetinfo-view'),


    #url(r'^record/(?P<slug>\w+).html$',
            #Record_search.as_view(), name='record-view'),
    url(r'^record/(\d+)/$', 'assets.assetdetails.Record_search', name='record-view'),#使用记录
    url(r'^sassetinfo/(\d+)/$', 'assets.assetdetails.Asset_Search', name='sassetinfo-view'),#配置查询

    url(r'^userecord/$', 'assets.userecord.UseRecordView',name='userecord-view'),
    url(r'^userecordsearch/$', 'assets.userecord.UseRecordSearch',name='userecordsearch-view'),
    url(r'^adduserecord/$','assets.userecord.AddUseRecordView',name='adduserecord-view'),
    url(r'^userecord/(\d+)/$','assets.userecord.EditUseRecordView',name='edituserecord-view'),
    url(r'^deluserecord/(\d+)/$', 'assets.userecord.DelUseRecordView',name='deluserecord-view'),
    url(r'^upuserecord/$', 'assets.userecord.UpUseRecordView',name='upuserecord-view'),
    url(r'^loaduserecord/$', 'assets.userecord.LoadUseRecordView',name='loaduserecord-view'),

    url(r'^repairinfo/$', 'assets.repairinfo.RepairInfoView',name='repairinfo-view'),
    url(r'^repairinfosearch/$', 'assets.repairinfo.RepairInfoSearch',name='repairinfosearch-view'),
    url(r'^addrepairinfo/$','assets.repairinfo.AddRepairInfoView',name='addrepairinfo-view'),
    url(r'^repairinfo/(\d+)/$','assets.repairinfo.EditRepairInfoView',name='editrepairinfo-view'),
    url(r'^delrepairinfo/(\d+)/$', 'assets.repairinfo.DelRepairInfoView',name='delrepairinfo-view'),
    url(r'^uprepairinfo/$', 'assets.repairinfo.UpRepairInfoView',name='uprepairinfo-view'),
    url(r'^loadrepairinfo/$', 'assets.repairinfo.LoadRepairInfoView',name='loadrepairinfo-view'),

    url(r'^supplier/$', 'assets.supplierinfo.SupplierView', name='supplier-view'),
    url(r'^suppliersearch/$', 'assets.supplierinfo.SupplierSearch', name='suppliersearch-view'),
    url(r'^addsupplier/$', 'assets.supplierinfo.AddSupplierView', name='addsupplier-view'),
    url(r'^supplier/(\d+)/$', 'assets.supplierinfo.EditSupplierView', name='editsupplier-view'),
    url(r'^delsupplier/(\d+)/$', 'assets.supplierinfo.DelSupplierView', name='delsupplier-view'),
    url(r'^upsupplier/$', 'assets.supplierinfo.UpSupplierView', name='upsupplier-view'),
    url(r'^loadsupplier/$', 'assets.supplierinfo.LoadSupplierView', name='loadsupplier-view'),



]
