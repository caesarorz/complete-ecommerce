# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-01-14 16:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('addresses', '0002_remove_address_pais'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='pais',
            field=models.CharField(default='Costa Rica', max_length=120),
        ),
    ]
