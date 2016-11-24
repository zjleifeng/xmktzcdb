# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0003_auto_20161118_1317'),
    ]

    operations = [
        migrations.AddField(
            model_name='repairinfo',
            name='delstatus',
            field=models.IntegerField(default=0, verbose_name='\u5220\u9664\u72b6\u6001(0:\u672a\u5220\u9664,1:\u5df2\u5220\u9664\u4e0d\u53ef\u663e\u793a)'),
        ),
        migrations.AddField(
            model_name='supplierinfo',
            name='delstatus',
            field=models.IntegerField(default=0, verbose_name='\u5220\u9664\u72b6\u6001(0:\u672a\u5220\u9664,1:\u5df2\u5220\u9664\u4e0d\u53ef\u663e\u793a)'),
        ),
        migrations.AlterField(
            model_name='userrecord',
            name='send_time',
            field=models.DateField(null=True, verbose_name='\u5b9e\u9645\u5f52\u8fd8\u65f6\u95f4', blank=True),
        ),
        migrations.AlterField(
            model_name='userrecord',
            name='start_time',
            field=models.DateField(verbose_name='\u9886\u7528\u65e5\u671f'),
        ),
        migrations.AlterField(
            model_name='userrecord',
            name='yend_time',
            field=models.DateField(null=True, verbose_name='\u9884\u8ba1\u5f52\u8fd8\u65e5\u671f', blank=True),
        ),
    ]
