# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-30 03:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stockCode', '0005_auto_20160830_1037'),
    ]

    operations = [
        migrations.AddField(
            model_name='codetable',
            name='group_name',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='\u7ec4\u522b'),
        ),
    ]
