# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-12-07 08:41
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_remove_employeesazk_position'),
    ]

    operations = [
        migrations.AddField(
            model_name='employeesazk',
            name='position',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.Position', verbose_name='Должность'),
        ),
        migrations.AlterField(
            model_name='employeesazk',
            name='azk',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Azs', verbose_name='АЗК'),
        ),
        migrations.AlterField(
            model_name='employeesazk',
            name='permission',
            field=models.ManyToManyField(to='main.Permission', verbose_name='Роли'),
        ),
        migrations.AlterField(
            model_name='employeesazk',
            name='person',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Person', verbose_name='Физ. лицо'),
        ),
    ]