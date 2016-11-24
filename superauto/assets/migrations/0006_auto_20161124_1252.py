# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0005_auto_20161124_1250'),
    ]

    operations = [
        migrations.AlterField(
            model_name='repairinfo',
            name='end_time',
            field=models.DateField(auto_now=True, verbose_name='\u7ef4\u62a4\u7ed3\u675f\u65f6\u95f4', null=True),
        ),
        migrations.AlterField(
            model_name='repairinfo',
            name='start_time',
            field=models.DateField(auto_now=True, verbose_name='\u7ef4\u62a4\u5f00\u59cb\u65f6\u95f4'),
        ),
    ]
