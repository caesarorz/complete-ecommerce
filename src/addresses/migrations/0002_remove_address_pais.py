# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-01-14 15:40
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('addresses', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='address',
            name='pais',
        ),
    ]