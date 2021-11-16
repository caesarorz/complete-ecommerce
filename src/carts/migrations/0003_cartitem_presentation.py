# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-12-07 14:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0002_auto_20181206_1612'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitem',
            name='presentation',
            field=models.CharField(choices=[('unidad', 'la unidad'), ('peso', 'Kilo')], default='unidad', max_length=120),
        ),
    ]
