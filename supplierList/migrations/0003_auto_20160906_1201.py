# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-06 04:01
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('supplierList', '0002_auto_20160905_1019'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='supplierlist',
            options={'managed': False, 'permissions': (('add_new_supplier', 'Can add new supplier'), ('update_all_supplier', 'can update all supplier'), ('update_contract', 'Can update contract'))},
        ),
    ]
