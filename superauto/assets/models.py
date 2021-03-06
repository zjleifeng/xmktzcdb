#coding:utf-8
from django.db import models


# Create your models here.




ASSET_TYPE={
        0: u'笔记本',
        1: u'台式机',
        2: u'服务器',
        3: u'其他',
}

BRANDS={
    0:u'DELL(戴尔)',
    1:u'Lenovo(联想)',
    2:u'Asus(华硕)',
    3:u'Apple(苹果)',
    4:u'Sony(索尼)',

}
CDROM={
    0:U'无光驱',
    1:u'有光驱',
}
STATUS={
    0: U'闲置',
    1: u'使用中',
    2:u'损坏',
    3:u'已报废',
}

CHANG={
    0:u'正常领用',
    1:u'短期借用',
    2:u'调拨外地',
    3:u'其他',
}




class UserStatus(models.Model):
    status=models.CharField(max_length=100,unique=True,verbose_name=u'当前员工状态')
    class Meta:
        verbose_name_plural=u'当前员工状态管理'

    def __unicode__(self):
        return self.status

    __str__ = __unicode__

class AssetType(models.Model):
    assettype=models.CharField(max_length=100,unique=True,verbose_name=u'资产类型')
    class Meta:
        verbose_name_plural=u'资产类型管理'

    def __unicode__(self):
        return self.assettype
    __str__ = __unicode__

class AssetBrands(models.Model):
    assetbrands=models.CharField(max_length=100,unique=True,verbose_name=u'资产型号')
    class Meta:
        verbose_name_plural=u'资产型号管理'
    def __unicode__(self):
        return self.assetbrands
    __str__ = __unicode__

class AssetStatus(models.Model):
    assettatus=models.CharField(max_length=100,unique=True,verbose_name=u'资产状态')
    class Meta:
        verbose_name_plural=u'资产状态管理'

    def __unicode__(self):
        return self.assettatus
    __str__ = __unicode__

class AssetCdrom(models.Model):
    assetcdrom=models.CharField(max_length=100,unique=True,verbose_name=u'光驱')
    class Meta:
        verbose_name_plural=u'光驱管理'
    def __unicode__(self):
        return self.assetcdrom
    __str__ = __unicode__

class AssetChang(models.Model):
    assetchang=models.CharField(max_length=100,unique=True,verbose_name=u'使用类型')
    class Meta:
        verbose_name_plural=u'使用类型管理'

    def __unicode__(self):
        return self.assetchang
    __str__ = __unicode__


class RecordStatus(models.Model):
    recordstatus = models.CharField(max_length=100, unique=True, verbose_name=u'是否归还')


    class Meta:
        verbose_name_plural = u'归还状态'

    def __unicode__(self):
        return self.recordstatus

    __str__ = __unicode__


#部门表
class Dept(models.Model):
    deptname=models.CharField(max_length=200,unique=True,verbose_name=u'部门名称')
    parentdept=models.ForeignKey('self',blank=True,null=True,verbose_name=u'上级部门')
    create_time=models.DateTimeField(auto_now_add=True,verbose_name=u'创建时间')
    delstatus=models.IntegerField(default=0,verbose_name=u'删除状态(0:未删除,1:已删除不可显示)')

    class Meta:
        verbose_name_plural=u'部门管理'
        ordering=['-create_time']

    def __unicode__(self):
        return self.deptname

    __str__ = __unicode__

#员工信息表
class EmployeeUser(models.Model):
    engname=models.CharField(max_length=200,unique=True,verbose_name=u'英文名')
    dept=models.ForeignKey(Dept,blank=True, null=True,on_delete=models.SET_NULL,verbose_name=u'部门')
    chnname=models.CharField(max_length=200,verbose_name=u'中文名')
    extnum=models.IntegerField(verbose_name=u'分机号')
    phonenum=models.BigIntegerField(verbose_name=u'手机号')
    email=models.EmailField(verbose_name=u'邮箱地址')
    entry_time=models.DateField(blank=True,null=True,verbose_name=u'入职日期')
    status=models.ForeignKey(UserStatus, blank=True, null=True,on_delete=models.SET_NULL,verbose_name=u'当前员工状态')
    delstatus = models.IntegerField(default=0, verbose_name=u'删除状态(0:未删除,1:已删除不可显示)')
    creare_time=models.DateTimeField(auto_now_add=True,verbose_name=u'创建时间')

    class Meta:
        verbose_name_plural=u'员工管理'
        ordering=['-creare_time']

    def __unicode__(self):
        return self.engname

    __str__ = __unicode__


class SiteInfo(models.Model):
    sitename=models.CharField(max_length=200,verbose_name=u'网站名称')
    class Meta:
        verbose_name_plural=u'网站基本信息'

    def __unicode__(self):
        return self.sitename

    __str__ = __unicode__

    # 资产信息

class AssetInfo(models.Model):
        # itno=models.ForeignKey(AssetDetails,verbose_name=u'IT资产编号')
        infoname = models.CharField(max_length=200, unique=True, verbose_name=u'配置名称')

        disktb = models.CharField(max_length=100, verbose_name=u'硬盘容量')
        memory = models.CharField(max_length=20, verbose_name=u'内存大小')
        cdrom = models.ForeignKey(AssetCdrom, blank=True, null=True, on_delete=models.SET_NULL, verbose_name=u'是否有光驱')
        videocard = models.CharField(max_length=200, blank=True, null=True, verbose_name=u'显卡')
        cpu = models.CharField(max_length=200, blank=True, null=True, verbose_name=u'CPU')
        displaycard = models.CharField(max_length=200, blank=True, null=True, verbose_name=u'显示屏')
        cpname = models.CharField(max_length=200, verbose_name=u'机器名', blank=True, null=True)
        mac = models.CharField(max_length=200, blank=True, null=True, verbose_name=u'MAC地址')
        ipadress = models.GenericIPAddressField(blank=True, null=True, verbose_name=u'IP地址')
        wifi_mac = models.CharField(max_length=200, blank=True, null=True, verbose_name=u'wifi-MAC地址')
        wifi_ip = models.GenericIPAddressField(blank=True, null=True, verbose_name=u'wifi-IP地址')
        delstatus = models.IntegerField(default=0, verbose_name=u'删除状态(0:未删除,1:已删除不可显示)')
        buy_time = models.DateField(blank=True, null=True, verbose_name=u'购买日期')
        create_time = models.DateTimeField(auto_now_add=True, verbose_name=u'创建时间')

        class Meta:
            verbose_name_plural = u'资产详细资料'
            ordering = ['-create_time']

        def __unicode__(self):
            return self.infoname

        __str__ = __unicode__


#资产列表信息

class AssetDetails(models.Model):
    itno=models.CharField(max_length=200,unique=True,verbose_name=u'IT资产编号')
    financeno=models.CharField(max_length=100,blank=True,null=True,verbose_name=u'财务资产编号')
    newno=models.CharField(max_length=100,blank=True,null=True,verbose_name=u'新资产编号')
    assettype=models.ForeignKey(AssetType, blank=True, null=True,on_delete=models.SET_NULL,verbose_name=u'资产类型')
    brands=models.ForeignKey(AssetBrands, blank=True, null=True,on_delete=models.SET_NULL,verbose_name=u'品牌')
    version=models.CharField(max_length=200,verbose_name=u'型号')
    status = models.ForeignKey(AssetStatus, blank=True, null=True,on_delete=models.SET_NULL,verbose_name=u'使用状态')
    where = models.ForeignKey(EmployeeUser,blank=True,null=True,on_delete=models.SET_NULL, verbose_name=u'存放地点')
    delstatus = models.IntegerField(default=0, verbose_name=u'删除状态(0:未删除,1:已删除不可显示)')
    configinfo=models.ForeignKey(AssetInfo,blank=True,null=True,on_delete=models.SET_NULL,verbose_name=u'配置信息')
    creare_time = models.DateTimeField(auto_now_add=True, verbose_name=u'创建时间')

    class Meta:
        verbose_name_plural = u'资产列表'
        ordering = ['-creare_time']


    def __unicode__(self):
        return self.itno

    __str__ = __unicode__



#使用记录
class UserRecord(models.Model):

    itno=models.ForeignKey(AssetDetails,verbose_name=u'IT资产编号')
    chang=models.ForeignKey(AssetChang, blank=True, null=True,on_delete=models.SET_NULL,verbose_name=u'使用类型')
    user=models.ForeignKey(EmployeeUser,verbose_name=u'使用者',on_delete=models.SET_NULL,blank=True,null=True)
    start_time=models.DateField(verbose_name=u'领用日期')
    yend_time=models.DateField(verbose_name=u'预计归还日期',blank=True,null=True)
    send_time=models.DateField(verbose_name=u'实际归还时间',blank=True,null=True)
    secordtatus=models.ForeignKey(RecordStatus,blank=True,null=True,on_delete=u'已归还',verbose_name=u'归还状态')
    recordtype = models.CharField(max_length=200,blank=True,null=True, verbose_name=u'备注')
    delstatus = models.IntegerField(default=0, verbose_name=u'删除状态(0:未删除,1:已删除不可显示)')
    creare_time = models.DateTimeField(auto_now_add=True, verbose_name=u'创建时间')
    class Meta:
        verbose_name_plural=u'使用记录'
        ordering=['start_time']

    def __unicode__(self):
        return self.itno.itno

    __str__ = __unicode__









#维修信息
class RepairInfo(models.Model):
    itno = models.ForeignKey(AssetDetails, verbose_name=u'IT资产编号')
    start_time=models.DateField(verbose_name=u'维护开始时间',blank=True,null=True)
    end_time=models.DateField(verbose_name=u'维护结束时间',blank=True,null=True)
    repinfo=models.CharField(max_length=500,verbose_name=u'维护内容说明')
    issure=models.BooleanField(default=True,verbose_name=u'是否完成')
    whorep=models.CharField(max_length=200,blank=True,null=True,verbose_name=u'维护人员')
    whophone=models.BigIntegerField(blank=True,null=True,verbose_name=u'维护人电话')
    delstatus = models.IntegerField(default=0, verbose_name=u'删除状态(0:未删除,1:已删除不可显示)')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name=u'创建时间')



    class Meta:
        verbose_name_plural=u'设备维护记录'
        ordering=['create_time']


    def __unicode__(self):
        return self.itno.itno
    __str__ = __unicode__

class SupplierInfo(models.Model):
    corporate_name=models.CharField(max_length=200,verbose_name=u'公司名称')
    corporate_adress=models.CharField(max_length=200,verbose_name=u'公司地址')
    corporate_phone=models.BigIntegerField(verbose_name=u'公司电话',blank=True,null=True)
    corporate_site=models.URLField(blank=True,null=True,verbose_name=u'公司网站')
    contect_name=models.CharField(max_length=200,verbose_name=u'联系人')
    contect_phone=models.BigIntegerField(verbose_name=u'联系人电话')
    contect_email=models.EmailField(blank=True,null=True,verbose_name=u'联系人邮箱')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name=u'创建时间')
    delstatus = models.IntegerField(default=0, verbose_name=u'删除状态(0:未删除,1:已删除不可显示)')

    class Meta:
        verbose_name_plural='供应商信息'


    def __unicode__(self):
        return self.corporate_name


    __str__ = __unicode__



