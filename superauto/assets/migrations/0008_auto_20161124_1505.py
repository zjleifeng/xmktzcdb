# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0007_auto_20161124_1504'),
    ]

    operations = [
        migrations.AlterField(
            model_name='supplierinfo',
            name='contect_phone',
            field=models.BigIntegerField(verbose_name='\u8054\u7cfb\u4eba\u7535\u8bdd'),
        ),
        migrations.AlterField(
            model_name='supplierinfo',
            name='corporate_phone',
            field=models.BigIntegerField(null=True, verbose_name='\u516c\u53f8\u7535\u8bdd', blank=True),
        ),
    ]
