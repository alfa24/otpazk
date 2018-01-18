from django.db import models

from  main.models import ServicePoint


# Задачи
class Task(models.Model):
    SYNCTIME = 'synctime'

    task_type = (
        (SYNCTIME, 'Синхронизация времени на Linux'),
    )

    name = models.CharField(verbose_name='Название', max_length=100, blank=True)
    service_point = models.ManyToManyField(ServicePoint)
    task = models.CharField(verbose_name='Задача', choices=task_type, max_length=100, default=SYNCTIME, blank=False, null=False)
    is_active = models.BooleanField(verbose_name="Активная", default=True)
    created = models.DateTimeField(verbose_name="Создан", auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(verbose_name="Изменен", auto_now_add=False, auto_now=True)

    def __str__(self):
        return "%s" % self.name

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'
