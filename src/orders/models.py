# import datetime
#
# from django.db import models
#
# # Create your models here.
# class Azs(models.Model):
#     name = models.TextField('Название',max_length=10)
#     ipAddress = models.TextField("ИП адрес", max_length=15)
#
#     def __str__(self):
#         return self.name
#
#
# class Invent(models.Model):
#     # azs
#     azs = models.ForeignKey(Azs)
#     dateStart = models.DateTimeField("Дата с")
#     # timeStart = models.TimeField("Время с")
#     dateEnd = models.DateTimeField("Дата по")
#     # timeEnd = models.TimeField("Время по")
#     enabled = models.BooleanField("Вкл.")
