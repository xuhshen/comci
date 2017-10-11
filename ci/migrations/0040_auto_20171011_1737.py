# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-10-11 09:37
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ci', '0039_auto_20171011_1313'),
    ]

    operations = [
        migrations.CreateModel(
            name='FilterTables',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='TaskParam',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('value', models.CharField(max_length=200)),
            ],
        ),
        migrations.AlterField(
            model_name='feature',
            name='params',
            field=models.ManyToManyField(to='ci.Param', verbose_name='Params'),
        ),
        migrations.AlterField(
            model_name='key_tables',
            name='table',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ci.FilterTables'),
        ),
    ]
