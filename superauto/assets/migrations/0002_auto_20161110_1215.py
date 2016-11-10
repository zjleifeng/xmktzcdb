# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employeeuser',
            name='entry_time',
            field=models.DateField(null=True, verbose_name='\u5165\u804c\u65e5\u671f', blank=True),
        ),
    ]
