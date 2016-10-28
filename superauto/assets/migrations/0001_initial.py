# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AssetDetails',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('itno', models.CharField(max_length=200, verbose_name='IT\u8d44\u4ea7\u7f16\u53f7')),
                ('financeno', models.CharField(max_length=100, null=True, verbose_name='\u8d22\u52a1\u8d44\u4ea7\u7f16\u53f7', blank=True)),
                ('newno', models.CharField(max_length=100, null=True, verbose_name='\u65b0\u8d44\u4ea7\u7f16\u53f7', blank=True)),
                ('assettype', models.IntegerField(verbose_name='\u8d44\u4ea7\u7c7b\u578b', choices=[(0, '\u7b14\u8bb0\u672c'), (1, '\u53f0\u5f0f\u673a'), (2, '\u670d\u52a1\u5668'), (3, '\u5176\u4ed6')])),
                ('brands', models.IntegerField(default=0, verbose_name='\u54c1\u724c', choices=[(0, 'DELL(\u6234\u5c14)'), (1, 'Lenovo(\u8054\u60f3)'), (2, 'Asus(\u534e\u7855)'), (3, 'Apple(\u82f9\u679c)'), (4, 'Sony(\u7d22\u5c3c)')])),
                ('version', models.CharField(max_length=200, verbose_name='\u578b\u53f7')),
                ('status', models.IntegerField(default=0, choices=[(0, '\u95f2\u7f6e'), (1, '\u4f7f\u7528\u4e2d')])),
                ('where', models.CharField(max_length=200, verbose_name='\u5b58\u653e\u5730\u70b9')),
                ('creare_time', models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
            ],
            options={
                'ordering': ['-creare_time'],
                'verbose_name_plural': '\u8d44\u4ea7\u4fe1\u606f',
            },
        ),
        migrations.CreateModel(
            name='AssetInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('disktb', models.CharField(max_length=100, verbose_name='\u786c\u76d8\u5bb9\u91cf')),
                ('memory', models.CharField(max_length=20, verbose_name='\u5185\u5b58\u5927\u5c0f')),
                ('cdrom', models.IntegerField(default=0, verbose_name='\u662f\u5426\u6709\u5149\u9a71', choices=[(0, '\u65e0\u5149\u9a71'), (1, '\u6709\u5149\u9a71')])),
                ('videocard', models.CharField(max_length=200, null=True, verbose_name='\u663e\u5361', blank=True)),
                ('cpu', models.CharField(max_length=200, null=True, verbose_name='CPU', blank=True)),
                ('displaycard', models.CharField(max_length=200, null=True, verbose_name='\u663e\u793a\u5c4f', blank=True)),
                ('cpname', models.CharField(max_length=200, null=True, verbose_name='\u673a\u5668\u540d', blank=True)),
                ('mac', models.CharField(max_length=200, null=True, verbose_name='MAC\u5730\u5740', blank=True)),
                ('ipadress', models.GenericIPAddressField(null=True, verbose_name='IP\u5730\u5740', blank=True)),
                ('wifi_mac', models.CharField(max_length=200, null=True, verbose_name='wifi-MAC\u5730\u5740', blank=True)),
                ('wifi_ip', models.GenericIPAddressField(null=True, verbose_name='wifi-IP\u5730\u5740', blank=True)),
                ('buy_time', models.DateTimeField(null=True, verbose_name='\u8d2d\u4e70\u65e5\u671f', blank=True)),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('itno', models.ForeignKey(verbose_name='\u8d44\u4ea7\u4fe1\u606f', to='assets.AssetDetails')),
            ],
            options={
                'ordering': ['-create_time'],
                'verbose_name_plural': '\u8d44\u4ea7\u8be6\u7ec6\u8d44\u6599',
            },
        ),
        migrations.CreateModel(
            name='Dept',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('deptname', models.CharField(max_length=200, verbose_name='\u90e8\u95e8\u540d\u79f0')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('parentdept', models.ForeignKey(default=None, blank=True, to='assets.Dept', null=True, verbose_name='\u4e0a\u7ea7\u90e8\u95e8')),
            ],
            options={
                'ordering': ['-create_time'],
                'verbose_name_plural': '\u90e8\u95e8\u7ba1\u7406',
            },
        ),
        migrations.CreateModel(
            name='EmployeeUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('engname', models.CharField(max_length=200, verbose_name='\u82f1\u6587\u540d')),
                ('chnname', models.CharField(max_length=200, verbose_name='\u4e2d\u6587\u540d')),
                ('extnum', models.IntegerField(verbose_name='\u5206\u673a\u53f7')),
                ('phonenum', models.IntegerField(null=True, verbose_name='\u624b\u673a\u53f7', blank=True)),
                ('email', models.EmailField(max_length=254, verbose_name='\u90ae\u7bb1\u5730\u5740')),
                ('entry_time', models.DateTimeField(null=True, verbose_name='\u5165\u804c\u65f6\u95f4', blank=True)),
                ('creare_time', models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('dept', models.ForeignKey(verbose_name='\u90e8\u95e8', to='assets.Dept')),
            ],
            options={
                'ordering': ['-creare_time'],
                'verbose_name_plural': '\u5458\u5de5\u7ba1\u7406',
            },
        ),
        migrations.CreateModel(
            name='RepairInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start_time', models.DateTimeField(auto_now=True, verbose_name='\u7ef4\u62a4\u5f00\u59cb\u65f6\u95f4')),
                ('end_time', models.DateTimeField(auto_now=True, verbose_name='\u7ef4\u62a4\u7ed3\u675f\u65f6\u95f4', null=True)),
                ('repinfo', models.CharField(max_length=500, verbose_name='\u7ef4\u62a4\u5185\u5bb9\u8bf4\u660e')),
                ('issure', models.BooleanField(default=True, verbose_name='\u662f\u5426\u5b8c\u6210')),
                ('whorep', models.CharField(max_length=200, null=True, verbose_name='\u7ef4\u62a4\u4eba\u5458', blank=True)),
                ('whophone', models.IntegerField(null=True, verbose_name='\u7ef4\u62a4\u4eba\u7535\u8bdd', blank=True)),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('itno', models.ForeignKey(verbose_name='\u8d44\u4ea7\u4fe1\u606f', to='assets.AssetDetails')),
            ],
            options={
                'ordering': ['create_time'],
                'verbose_name_plural': '\u8bbe\u5907\u7ef4\u62a4\u8bb0\u5f55',
            },
        ),
        migrations.CreateModel(
            name='SupplierInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('corporate_name', models.CharField(max_length=200, verbose_name='\u516c\u53f8\u540d\u79f0')),
                ('corporate_adress', models.CharField(max_length=200, verbose_name='\u516c\u53f8\u5730\u5740')),
                ('corporate_phone', models.IntegerField(null=True, verbose_name='\u516c\u53f8\u7535\u8bdd', blank=True)),
                ('corporate_site', models.SlugField(null=True, verbose_name='\u516c\u53f8\u7f51\u7ad9', blank=True)),
                ('contect_name', models.CharField(max_length=200, verbose_name='\u8054\u7cfb\u4eba')),
                ('contect_phone', models.IntegerField(verbose_name='\u8054\u7cfb\u4eba\u7535\u8bdd')),
                ('contect_email', models.EmailField(max_length=254, null=True, verbose_name='\u8054\u7cfb\u4eba\u90ae\u7bb1', blank=True)),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
            ],
            options={
                'verbose_name_plural': '\u4f9b\u5e94\u5546\u4fe1\u606f',
            },
        ),
        migrations.CreateModel(
            name='UserRecord',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('chang', models.IntegerField(default=0, verbose_name='\u4f7f\u7528\u7c7b\u578b', choices=[(0, '\u6b63\u5e38\u9886\u7528'), (1, '\u77ed\u671f\u501f\u7528'), (2, '\u8c03\u62e8\u5916\u5730'), (3, '\u5176\u4ed6')])),
                ('start_time', models.DateTimeField(auto_now=True, verbose_name='\u9886\u7528\u65e5\u671f')),
                ('yend_time', models.DateTimeField(auto_now=True, verbose_name='\u9884\u8ba1\u5f52\u8fd8\u65e5\u671f', null=True)),
                ('send_time', models.DateTimeField(auto_now=True, verbose_name='\u5b9e\u9645\u5f52\u8fd8\u65f6\u95f4', null=True)),
                ('creare_time', models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('itno', models.ForeignKey(verbose_name='\u8d44\u4ea7\u4fe1\u606f', to='assets.AssetDetails')),
                ('user', models.ForeignKey(verbose_name='\u4f7f\u7528\u8005', blank=True, to='assets.EmployeeUser', null=True)),
            ],
            options={
                'ordering': ['start_time'],
                'verbose_name_plural': '\u4f7f\u7528\u8bb0\u5f55',
            },
        ),
    ]
