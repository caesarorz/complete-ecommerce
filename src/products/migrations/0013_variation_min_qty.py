# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-12-07 20:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0012_auto_20181127_0815'),
    ]

    operations = [
        migrations.AddField(
            model_name='variation',
            name='min_qty',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=6),
        ),
    ]
