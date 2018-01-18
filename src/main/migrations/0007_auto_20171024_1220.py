# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-10-24 04:20
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_auto_20171024_1123'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='azs',
            options={'verbose_name': 'АЗК', 'verbose_name_plural': 'АЗК/АЗС'},
        ),
        migrations.AlterModelOptions(
            name='azsgroup',
            options={'verbose_name': 'Группа АЗК', 'verbose_name_plural': 'Группы АЗК (территориально)'},
        ),
        migrations.AlterModelOptions(
            name='personal',
            options={'verbose_name': 'Сотрудник АЗК', 'verbose_name_plural': 'Персонал АЗК'},
        ),
        migrations.AlterModelOptions(
            name='servicepoint',
            options={'verbose_name': 'АРМ', 'verbose_name_plural': 'АРМы'},
        ),
        migrations.AlterModelOptions(
            name='typecharacteristicsp',
            options={'verbose_name': 'Тип характеристики АРМ', 'verbose_name_plural': 'Типы характеристик АРМ'},
        ),
        migrations.AlterModelOptions(
            name='typeservicepoint',
            options={'verbose_name': 'Тип АРМ', 'verbose_name_plural': 'Типы АРМ'},
        ),
    ]
