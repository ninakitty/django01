# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-01-18 10:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0003_auto_20180112_1622'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='category',
            field=models.CharField(default='后端开发', max_length=30, verbose_name='课程类别'),
        ),
    ]