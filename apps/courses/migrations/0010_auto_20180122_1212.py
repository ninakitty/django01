# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-01-22 12:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0009_auto_20180122_1129'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='needknow',
            field=models.CharField(default='', max_length=300, verbose_name='课程须知'),
        ),
        migrations.AddField(
            model_name='course',
            name='teacher_tell',
            field=models.CharField(default='', max_length=300, verbose_name='老师告诉你'),
        ),
    ]
