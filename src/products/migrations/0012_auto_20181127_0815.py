# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-11-27 14:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0011_auto_20181126_1437'),
    ]

    operations = [
        migrations.AlterField(
            model_name='variation',
            name='presentation',
            field=models.CharField(choices=[('unidad', 'la unidad'), ('peso', 'Kilo')], default='unidad', max_length=120),
        ),
    ]