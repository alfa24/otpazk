from django.db import models

from  main.models import ServicePoint
from tasks.models import Task


# Задачи
class Log(models.Model):
    ERROR = 0
    INFO = 1
    WARNING = 2

    Type = (
        (ERROR, 'Ошибка'),
        (INFO, 'Информация'),
        (WARNING, 'Предупреждение'),
    )

    task = models.ForeignKey(Task, on_delete=models.DO_NOTHING)
    service_point = models.ForeignKey(ServicePoint, on_delete=models.DO_NOTHING)
    description = models.CharField(verbose_name='Название', max_length=150, blank=True)
    datetime = models.DateTimeField(verbose_name='Дата')
    type = models.IntegerField(verbose_name='Задача', choices=Type, default=INFO, blank=False, null=False)
    is_active = models.BooleanField(verbose_name="Активная", default=True)
    created = models.DateTimeField(verbose_name="Создан", auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(verbose_name="Изменен", auto_now_add=False, auto_now=True)

    def __str__(self):
        return "%s  %s: %s" % (self.datetime, self.type, self.description)

    class Meta:
        verbose_name = 'Лог'
        verbose_name_plural = 'Логи'