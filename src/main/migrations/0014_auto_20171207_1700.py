# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-12-07 09:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0013_employeesazk_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employeesazk',
            name='status',
            field=models.IntegerField(choices=[(0, 'В обработке'), (1, 'Активный'), (2, 'Заблокированный')], default=0, verbose_name='Статус'),
        ),
    ]
