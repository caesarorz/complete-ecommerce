# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2016-02-11 20:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_variation_featured'),
    ]

    operations = [
        migrations.AlterField(
            model_name='variation',
            name='inventory',
            field=models.IntegerField(default=0),
        ),
    ]
