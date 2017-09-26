# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-09-19 03:05
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ci', '0014_auto_20170919_1100'),
    ]

    operations = [
        migrations.CreateModel(
            name='Devcasetags',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('caseset', models.ManyToManyField(to='ci.Casetags', verbose_name='test case tag')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ci.Product')),
            ],
        ),
        migrations.CreateModel(
            name='Relcasetags',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('caseset', models.ManyToManyField(to='ci.Casetags', verbose_name='case tag')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ci.Product')),
            ],
        ),
        migrations.AlterField(
            model_name='feature',
            name='devtags',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='ci.Devcasetags'),
        ),
        migrations.AlterField(
            model_name='feature',
            name='reltags',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='ci.Relcasetags'),
        ),
        migrations.AlterField(
            model_name='relcaseset',
            name='caseset',
            field=models.ManyToManyField(to='ci.Caseset', verbose_name='case set'),
        ),
    ]
