# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-01-22 11:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0008_course_notice'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='notice',
            field=models.CharField(blank=True, default='', max_length=50, null=True, verbose_name='课程公告'),
        ),
    ]