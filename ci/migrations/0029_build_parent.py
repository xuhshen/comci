# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-09-21 06:00
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ci', '0028_auto_20170921_1115'),
    ]

    operations = [
        migrations.AddField(
            model_name='build',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='ci.Build'),
        ),
    ]
