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
            name='itno',
            field=models.ForeignKey(verbose_name='IT\u8d44\u4ea7\u7f16\u53f7', to='assets.AssetDetails'),
        ),
        migrations.AlterField(
            model_name='repairinfo',
            name='itno',
            field=models.ForeignKey(verbose_name='IT\u8d44\u4ea7\u7f16\u53f7', to='assets.AssetDetails'),
        ),
        migrations.AlterField(
            model_name='userrecord',
            name='itno',
            field=models.ForeignKey(verbose_name='IT\u8d44\u4ea7\u7f16\u53f7', to='assets.AssetDetails'),
        ),
    ]
