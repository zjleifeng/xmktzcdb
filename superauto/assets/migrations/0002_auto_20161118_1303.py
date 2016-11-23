# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assetinfo',
            name='buy_time',
            field=models.DateField(null=True, verbose_name='\u8d2d\u4e70\u65e5\u671f', blank=True),
        ),
    ]
