# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-09-18 06:50
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ci', '0002_auto_20170918_1446'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Builds',
            new_name='Build',
        ),
    ]
