# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0006_auto_20161124_1252'),
    ]

    operations = [
        migrations.AlterField(
            model_name='repairinfo',
            name='end_time',
            field=models.DateField(null=True, verbose_name='\u7ef4\u62a4\u7ed3\u675f\u65f6\u95f4', blank=True),
        ),
        migrations.AlterField(
            model_name='repairinfo',
            name='start_time',
            field=models.DateField(null=True, verbose_name='\u7ef4\u62a4\u5f00\u59cb\u65f6\u95f4', blank=True),
        ),
        migrations.AlterField(
            model_name='supplierinfo',
            name='corporate_site',
            field=models.URLField(null=True, verbose_name='\u516c\u53f8\u7f51\u7ad9', blank=True),
        ),
    ]
