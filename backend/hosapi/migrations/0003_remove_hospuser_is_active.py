# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-23 16:24
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hosapi', '0002_auto_20171117_1457'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hospuser',
            name='is_active',
        ),
    ]
