# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-12-13 19:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_auto_20181207_0850'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='payment_method',
            field=models.CharField(blank=True, choices=[('efectivo', 'efectivo'), ('tarjeta', 'tarjeta'), ('paypal', 'paypal')], max_length=120, null=True),
        ),
    ]
