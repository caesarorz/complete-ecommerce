# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2016-02-11 18:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='variation',
            name='featured',
            field=models.BooleanField(default=False),
        ),
    ]
