# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0004_auto_20161124_1246'),
    ]

    operations = [
        migrations.AlterField(
            model_name='repairinfo',
            name='whophone',
            field=models.BigIntegerField(null=True, verbose_name='\u7ef4\u62a4\u4eba\u7535\u8bdd', blank=True),
        ),
    ]
