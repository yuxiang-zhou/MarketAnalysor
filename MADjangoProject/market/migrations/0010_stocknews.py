# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-02-29 18:08
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('market', '0009_sectorhistory'),
    ]

    operations = [
        migrations.CreateModel(
            name='StockNews',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='', max_length=256)),
                ('url', models.CharField(default='', max_length=512)),
                ('pub_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('stock', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='market.Stock')),
            ],
        ),
    ]
