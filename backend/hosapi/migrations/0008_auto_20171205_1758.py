# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-05 17:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hosapi', '0007_auto_20171205_1756'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subject',
            name='create_date',
            field=models.DateTimeField(blank=True),
        ),
    ]
