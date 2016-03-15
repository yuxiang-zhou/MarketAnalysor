# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-02-02 18:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('market', '0004_stockanalysis'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stockanalysis',
            name='stock',
        ),
        migrations.AddField(
            model_name='stock',
            name='halfyearly_change',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='stock',
            name='monthly_change',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='stock',
            name='seasonally_change',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='stock',
            name='weekly_change',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='stock',
            name='yearly_change',
            field=models.FloatField(default=0),
        ),
        migrations.DeleteModel(
            name='StockAnalysis',
        ),
    ]