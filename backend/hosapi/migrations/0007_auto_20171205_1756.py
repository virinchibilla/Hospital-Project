# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-05 17:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hosapi', '0006_auto_20171205_1753'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subject',
            name='create_date',
            field=models.DateField(blank=True),
        ),
    ]
