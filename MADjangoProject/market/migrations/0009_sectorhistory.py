# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-02-25 18:32
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('market', '0008_auto_20160224_1843'),
    ]

    operations = [
        migrations.CreateModel(
            name='SectorHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Sector', models.CharField(max_length=100)),
                ('Symbol', models.CharField(max_length=20)),
                ('Open', models.FloatField(default=0)),
                ('Close', models.FloatField(default=0)),
                ('High', models.FloatField(default=0)),
                ('Low', models.FloatField(default=0)),
                ('Volumn', models.FloatField(default=0)),
                ('pub_date', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
    ]
