import json
import threading

import requests
from django.db import models
from django.utils.safestring import mark_safe


def get_new_webhook_url():
    return mark_safe(
        u'<a href="https://my.slack.com/apps/new/A0F7XDUAZ-incoming-webhooks" target=_top)>Get Webhook URL</a>')


class SlackNotice(models.Model):
    ERROR_SYNCTIME = 0
    TBOT_ORDER = 1
    TBOT_ALL = 2
    ERROR_BACKUP = 3

    notice_type = (
        (ERROR_SYNCTIME, 'Ошибка синхронизация времени на Linux'),
        (ERROR_BACKUP, 'Ошибка скачивания бэкапа на Linux'),
        (TBOT_ORDER, 'Телеграм бот: /заявка'),
        (TBOT_ALL, 'Телеграм бот: Дублирование всех сообщений в чате'),
    )

    name = models.CharField(verbose_name='Название', max_length=50)
    type = models.IntegerField(verbose_name='Тип уведомления', choices=notice_type,
                               default=ERROR_SYNCTIME, blank=False,
                               null=False)
    url = models.URLField(verbose_name='WebHook', help_text=get_new_webhook_url(),
                          blank=True, null=False, default=None)
    description = models.TextField('Комментарий', blank=True, null=True, default=None)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Slack уведомление'
        verbose_name_plural = 'Slack уведомления'

    def send(self, caption, attachments):
        # attachments = [
        #     {
        #         'fields': [
        #             {
        #                 "title": 'title:',
        #                 "value": 'text',
        #                 "short": False,
        #             },
        #         ],
        #     },
        # ]

        data = {
            'payload': json.dumps({'text': caption, 'attachments': attachments}),
        }
        # send it
        try:
            th = threading.Thread(target=requests.post, name="th",
                                  kwargs={
                                      "url": self.url,
                                      "data": data})
            th.start()
        except Exception as e:
            pass