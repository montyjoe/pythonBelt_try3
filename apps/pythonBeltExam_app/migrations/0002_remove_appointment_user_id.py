# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-05-06 02:35
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pythonBeltExam_app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='appointment',
            name='user_id',
        ),
    ]
