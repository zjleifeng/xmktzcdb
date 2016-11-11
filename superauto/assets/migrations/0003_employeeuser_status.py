# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0002_auto_20161110_1215'),
    ]

    operations = [
        migrations.AddField(
            model_name='employeeuser',
            name='status',
            field=models.IntegerField(default=0, verbose_name='\u72b6\u6001', choices=[(0, '\u5728\u804c'), (1, '\u79bb\u804c'), (2, '\u4f11\u5047')]),
        ),
    ]
