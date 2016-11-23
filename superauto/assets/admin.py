# -*- coding: utf-8 -*-#
from django.contrib import admin
from assets.models import Dept,EmployeeUser,AssetDetails,UserRecord,AssetInfo,RepairInfo,SupplierInfo,SiteInfo,UserStatus,AssetCdrom,AssetType,AssetChang,AssetStatus,AssetBrands,RecordStatus
from django.utils.text import capfirst
from django.utils.datastructures import SortedDict

def find_model_index(name):
    count=0
    for model,model_admin in admin.site._registry.items():
        if capfirst(model._meta.verbose_name_plural) == name:
            return count
        else:
            count += 1
    return count

def index_decorator(func):
    def inner(*args, **kwargs):
        templateresponse = func(*args, **kwargs)
        for app in templateresponse.context_data['app_list']:
            app['models'].sort(key=lambda x: find_model_index(x['name']))
        return templateresponse
    return inner


registry = SortedDict()
registry.update(admin.site._registry)
admin.site._registry = registry
admin.site.index = index_decorator(admin.site.index)
admin.site.app_index = index_decorator(admin.site.app_index)
#admin.site.register(yourmodel, yourmodeladmin)

# Register your models here.

class SiteinfoAdmin(admin.ModelAdmin):
    list_display = ('sitename',)


class DeptAdmin(admin.ModelAdmin):

    #添加搜索框
    search_fields = ('deptname',)
    #管理列表显示数据字段
    list_display = ('deptname','parentdept','delstatus','create_time')
    #添加过滤器，以下面字段进行过滤
    list_filter = ('deptname','delstatus','create_time')
    #新建面板中可以被编辑的字段
    #fields = ('content','user','ip','create_time','update_time','click_count','is_top')

class EmployeeUserAdmin(admin.ModelAdmin):
    # 添加搜索框
    search_fields = ('engname',)
    # 管理列表显示数据字段
    list_display = ('engname','dept', 'chnname','extnum','email','phonenum','entry_time','status','delstatus')
    # 添加过滤器，以下面字段进行过滤
    list_filter = ('engname', 'dept','status','delstatus')
    # 新建面板中可以被编辑的字段
    # fields = ('content','user','ip','create_time','update_time','click_count','is_top')

class AssetDetailsAdmin(admin.ModelAdmin):
    search_fields = ('itno','assettype','version','status')
    list_display = ('itno', 'financeno', 'assettype', 'brands', 'version','status','where','configinfo')
    list_filter = ('assettype', 'brands','version','status','configinfo')
    # fields = ('content','user','ip','create_time','update_time','click_count','is_top')

class UserRecordAdmin(admin.ModelAdmin):
    search_fields = ('itno','chang','user')
    list_display = ('itno', 'user', 'chang', 'start_time', 'yend_time','send_time','secordtatus','recordtype','delstatus')
    list_filter = ('itno', 'user', 'chang', 'start_time', 'recordtype')
    fields = ('itno', 'user', 'chang', 'start_time', 'yend_time','send_time','secordtatus','recordtype','delstatus')

class AssetInfoAdmin(admin.ModelAdmin):
    search_fields = ('infoname', 'mac')
    list_display = ('infoname', 'cpname', 'disktb', 'memory', 'cdrom', 'videocard', 'cpu','displaycard','ipadress','buy_time')
    list_filter = ('infoname',)
    # fields = ('content','user','ip','create_time','update_time','click_count','is_top')

class RepairInfoAdmin(admin.ModelAdmin):
    search_fields = ('itno', 'start_time','issure')
    list_display = (
    'itno', 'start_time', 'end_time', 'repinfo', 'issure', 'whorep', 'whophone')
    list_filter = ('itno','start_time','issure')
    # fields = ('content','user','ip','create_time','update_time','click_count','is_top')

class SupplierInfoAdmin(admin.ModelAdmin):
    search_fields = ('corporate_name', 'contect_name')
    list_display = (
    'corporate_name', 'corporate_adress', 'corporate_phone', 'corporate_site', 'contect_name', 'contect_phone', 'contect_email')
    list_filter = ('corporate_name','contect_name')
    # fields = ('content','user','ip','create_time','update_time','click_count','is_top')


class UserStatusAdmin(admin.ModelAdmin):
    list_display = ('status',)

class AssetTypeAdmin(admin.ModelAdmin):
    list_display = ('assettype',)

class AssetBrandsAdmin(admin.ModelAdmin):
    list_display = ('assetbrands',)

class AssetStatusAdmin(admin.ModelAdmin):
    list_display = ('assettatus',)

class AssetCdromAdmin(admin.ModelAdmin):
    list_display = ('assetcdrom',)

class AssetChangAdmin(admin.ModelAdmin):
    list_display = ('assetchang',)

class RecordStatusAdmin(admin.ModelAdmin):
    list_display = ('recordstatus',)


admin.site.register(Dept,DeptAdmin)
admin.site.register(EmployeeUser,EmployeeUserAdmin)
admin.site.register(AssetDetails,AssetDetailsAdmin)
admin.site.register(AssetInfo,AssetInfoAdmin)
admin.site.register(UserRecord,UserRecordAdmin)

admin.site.register(RepairInfo,RepairInfoAdmin)
admin.site.register(SupplierInfo,SupplierInfoAdmin)
admin.site.register(SiteInfo,SiteinfoAdmin)
admin.site.register(RecordStatus,RecordStatusAdmin)
admin.site.register(UserStatus,UserStatusAdmin)
admin.site.register(AssetStatus,AssetStatusAdmin)
admin.site.register(AssetBrands,AssetBrandsAdmin)
admin.site.register(AssetType,AssetTypeAdmin)
admin.site.register(AssetCdrom,AssetCdromAdmin)
admin.site.register(AssetChang,AssetChangAdmin)

