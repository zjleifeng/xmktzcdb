# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0002_auto_20161118_1303'),
    ]

    operations = [
        migrations.CreateModel(
            name='RecordStatus',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('recordstatus', models.CharField(unique=True, max_length=100, verbose_name='\u662f\u5426\u5f52\u8fd8')),
            ],
            options={
                'verbose_name_plural': '\u5f52\u8fd8\u72b6\u6001',
            },
        ),
        migrations.AddField(
            model_name='userrecord',
            name='delstatus',
            field=models.IntegerField(default=0, verbose_name='\u5220\u9664\u72b6\u6001(0:\u672a\u5220\u9664,1:\u5df2\u5220\u9664\u4e0d\u53ef\u663e\u793a)'),
        ),
        migrations.AddField(
            model_name='userrecord',
            name='recordtype',
            field=models.CharField(max_length=200, null=True, verbose_name='\u5907\u6ce8', blank=True),
        ),
        migrations.AlterField(
            model_name='userrecord',
            name='send_time',
            field=models.DateField(auto_now=True, verbose_name='\u5b9e\u9645\u5f52\u8fd8\u65f6\u95f4', null=True),
        ),
        migrations.AlterField(
            model_name='userrecord',
            name='start_time',
            field=models.DateField(auto_now=True, verbose_name='\u9886\u7528\u65e5\u671f'),
        ),
        migrations.AlterField(
            model_name='userrecord',
            name='yend_time',
            field=models.DateField(auto_now=True, verbose_name='\u9884\u8ba1\u5f52\u8fd8\u65e5\u671f', null=True),
        ),
        migrations.AddField(
            model_name='userrecord',
            name='secordtatus',
            field=models.ForeignKey(on_delete='\u5df2\u5f52\u8fd8', verbose_name='\u5f52\u8fd8\u72b6\u6001', blank=True, to='assets.RecordStatus', null=True),
        ),
    ]
