# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-01-15 18:22
from __future__ import unicode_literals

import aboutpage.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='About',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('header_one', models.CharField(default='Hello World', max_length=220)),
                ('paragraph', models.TextField(blank=True, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to=aboutpage.models.upload_image_path)),
            ],
        ),
    ]
