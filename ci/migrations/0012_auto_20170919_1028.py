# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-09-19 02:28
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ci', '0011_auto_20170919_1026'),
    ]

    operations = [
        migrations.RenameField(
            model_name='module',
            old_name='subrepository',
            new_name='repository',
        ),
    ]
