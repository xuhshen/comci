# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-09-21 03:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ci', '0027_auto_20170921_1114'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='depends',
            field=models.ManyToManyField(blank=True, related_name='_task_depends_+', to='ci.Task'),
        ),
    ]
