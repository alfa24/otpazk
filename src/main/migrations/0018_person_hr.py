# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-02-07 01:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0017_auto_20180206_1131'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='hr',
            field=models.BooleanField(default=False, verbose_name='Модератор'),
        ),
    ]