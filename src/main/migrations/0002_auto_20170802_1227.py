# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-08-02 04:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='azs',
            name='address',
            field=models.TextField(blank=True, default=None, null=True, verbose_name='Адрес'),
        ),
        migrations.AlterField(
            model_name='azs',
            name='is_deleted',
            field=models.BooleanField(default=False, verbose_name='Пометка удаления'),
        ),
        migrations.AlterField(
            model_name='azsgroup',
            name='is_deleted',
            field=models.BooleanField(default=False, verbose_name='Пометка удаления'),
        ),
        migrations.AlterField(
            model_name='invent',
            name='is_deleted',
            field=models.BooleanField(default=False, verbose_name='Пометка удаления'),
        ),
        migrations.AlterField(
            model_name='personal',
            name='is_deleted',
            field=models.BooleanField(default=False, verbose_name='Пометка удаления'),
        ),
    ]
