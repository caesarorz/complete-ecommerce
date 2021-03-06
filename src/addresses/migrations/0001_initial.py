# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-11-20 18:27
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('billing', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address_type', models.CharField(choices=[('shipping', 'Envio')], max_length=120)),
                ('direccion_linea_1', models.CharField(max_length=120)),
                ('direccion_linea_2', models.CharField(blank=True, max_length=120, null=True)),
                ('pais', models.CharField(default='Costa Rica', max_length=120)),
                ('provincia', models.CharField(max_length=120)),
                ('canton', models.CharField(max_length=120)),
                ('distrito', models.CharField(blank=True, max_length=120, null=True)),
                ('billing_profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='billing.BillingProfile')),
            ],
        ),
    ]
