# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2017-04-06 17:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0005_auto_20170405_1439'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacher',
            name='age',
            field=models.IntegerField(default=18, verbose_name='\u5e74\u9f84'),
        ),
    ]
