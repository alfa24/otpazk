# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-01-10 04:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SlackNotice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Название')),
                ('type', models.IntegerField(choices=[(0, 'Ошибка синхронизация времени на Linux'), (1, 'Телеграм бот: /заявка'), (2, 'Телеграм бот: Дублирование всех сообщений в чате')], default=0, verbose_name='Тип уведомления')),
                ('url', models.URLField(blank=True, default=None, help_text='<a href="https://my.slack.com/apps/new/A0F7XDUAZ-incoming-webhooks" target=_top)>Get Webhook URL</a>', verbose_name='WebHook')),
                ('description', models.TextField(verbose_name='Комментарий')),
            ],
            options={
                'verbose_name': 'Slack уведомление',
                'verbose_name_plural': 'Slack уведомления',
            },
        ),
    ]