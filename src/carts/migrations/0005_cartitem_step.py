# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-01-21 20:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0004_auto_20181207_1321'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitem',
            name='step',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=6),
        ),
    ]
