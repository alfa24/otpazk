# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-08-02 02:13
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Azs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, default=None, max_length=10, null=True, verbose_name='Наименование')),
                ('full_name', models.CharField(blank=True, default=None, max_length=10, null=True, verbose_name='Полное наименование')),
                ('sublan', models.CharField(blank=True, default=None, max_length=19, null=True, verbose_name='Подсеть')),
                ('phone', models.CharField(blank=True, default=None, max_length=165, null=True, verbose_name='Телефон')),
                ('eMail', models.EmailField(blank=True, default=None, max_length=254, null=True, verbose_name='E-Mail')),
                ('address', models.CharField(blank=True, default=None, max_length=150, null=True, verbose_name='Адрес')),
                ('is_deleted', models.BooleanField(default=True, verbose_name='Пометка удаления')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Создан')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Изменен')),
            ],
            options={
                'verbose_name': 'АЗК',
                'verbose_name_plural': 'Заправки',
            },
        ),
        migrations.CreateModel(
            name='AzsGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, default=None, max_length=50, null=True, verbose_name='Название')),
                ('is_deleted', models.BooleanField(default=True, verbose_name='Пометка удаления')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Создан')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Изменен')),
            ],
            options={
                'verbose_name': 'Группа АЗК',
                'verbose_name_plural': 'Группы АЗК',
            },
        ),
        migrations.CreateModel(
            name='Invent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dateStart', models.DateTimeField(blank=True, default=None, null=True, verbose_name='Дата с')),
                ('dateEnd', models.DateTimeField(blank=True, default=None, null=True, verbose_name='Дата по')),
                ('enabled', models.BooleanField(default=True, verbose_name='Вкл.')),
                ('is_deleted', models.BooleanField(default=True, verbose_name='Пометка удаления')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Создан')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Изменен')),
                ('azs', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Azs')),
            ],
        ),
        migrations.CreateModel(
            name='Personal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fio', models.CharField(blank=True, max_length=100, verbose_name='Имя')),
                ('phone', models.CharField(blank=True, max_length=165, verbose_name='Телефон')),
                ('is_deleted', models.BooleanField(default=True, verbose_name='Пометка удаления')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Создан')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Изменен')),
            ],
        ),
        migrations.AddField(
            model_name='azs',
            name='azs_group',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.AzsGroup', verbose_name='Группа'),
        ),
        migrations.AddField(
            model_name='azs',
            name='manager',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.Personal', verbose_name='Менеджер'),
        ),
    ]
