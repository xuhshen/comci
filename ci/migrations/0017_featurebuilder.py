# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-09-19 07:06
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ci', '0016_auto_20170919_1443'),
    ]

    operations = [
        migrations.CreateModel(
            name='Featurebuilder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('builds', models.ManyToManyField(to='ci.Build')),
                ('feature', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ci.Feature')),
            ],
        ),
    ]
