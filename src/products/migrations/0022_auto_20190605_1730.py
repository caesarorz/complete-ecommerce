# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-06-05 23:30
from __future__ import unicode_literals

from django.db import migrations, models
import products.models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0021_auto_20190605_1727'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productfile',
            name='file',
            field=models.FileField(upload_to=products.models.upload_product_file_loc),
        ),
    ]
