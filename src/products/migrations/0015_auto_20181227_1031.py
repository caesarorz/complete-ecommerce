# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-12-27 16:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0014_product_presentation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='presentation',
            field=models.CharField(default='Peso', help_text='En que presentación se vende el producto', max_length=120),
        ),
    ]
