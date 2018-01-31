from django.db import models


# Персонал АЗК
class Personal(models.Model):
    fio = models.CharField(verbose_name='Имя', max_length=100, blank=True)
    phone = models.CharField(verbose_name="Телефон", max_length=165, blank=True)
    is_deleted = models.BooleanField(verbose_name="Пометка удаления", default=False)
    created = models.DateTimeField(verbose_name="Создан", auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(verbose_name="Изменен", auto_now_add=False, auto_now=True)

    def __str__(self):
        return "%s" % self.fio

    class Meta:
        verbose_name = 'Сотрудник АЗК'
        verbose_name_plural = 'Персонал АЗК'


# Группа АЗК (территориально)
class AzsGroup(models.Model):
    name = models.CharField(verbose_name="Название", max_length=50, blank=True, null=True, default=None)
    is_deleted = models.BooleanField(verbose_name="Пометка удаления", default=False)
    created = models.DateTimeField(verbose_name="Создан", auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(verbose_name="Изменен", auto_now_add=False, auto_now=True)

    def __str__(self):
        return "%s" % (self.name)

    class Meta:
        verbose_name = 'Группа АЗК'
        verbose_name_plural = 'Группы АЗК (территориально)'


# Модель АЗС
class Azs(models.Model):
    name = models.CharField(verbose_name='Наименование', max_length=10, blank=True, null=True, default=None)
    full_name = models.CharField(verbose_name='Полное наименование', max_length=50, blank=True, null=True, default=None)
    sublan = models.CharField(verbose_name="Подсеть", max_length=19, blank=True, null=True, default=None)
    phone = models.CharField(verbose_name="Телефон", max_length=165, blank=True, null=True, default=None)
    eMail = models.EmailField(verbose_name="E-Mail", blank=True, null=True, default=None)
    manager = models.ForeignKey(Personal, verbose_name="Менеджер", on_delete=models.DO_NOTHING, blank=True, null=True, default=None)
    address = models.TextField(verbose_name="Адрес", blank=True, null=True, default=None)
    azs_group = models.ForeignKey(AzsGroup, verbose_name="Группа", on_delete=models.DO_NOTHING, blank=True, null=True, default=None)
    is_deleted = models.BooleanField(verbose_name="Пометка удаления", default=False)
    created = models.DateTimeField(verbose_name="Создан", auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(verbose_name="Изменен", auto_now_add=False, auto_now=True)

    def __str__(self):
        return "%s" % (self.full_name)

    class Meta:
        verbose_name = 'АЗК'
        verbose_name_plural = 'АЗК/АЗС'


# Расписание инвентаризации
class Invent(models.Model):
    azs = models.ForeignKey(Azs, on_delete=models.DO_NOTHING)
    dateStart = models.DateTimeField(verbose_name="Дата с", blank=True, null=True, default=None)
    dateEnd = models.DateTimeField(verbose_name="Дата по", blank=True, null=True, default=None)
    enabled = models.BooleanField(verbose_name="Вкл.", default=True)
    is_deleted = models.BooleanField(verbose_name="Пометка удаления", default=False)
    created = models.DateTimeField(verbose_name="Создан", auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(verbose_name="Изменен", auto_now_add=False, auto_now=True)


# Тип точки обслуживания
# например POS1, POS2
class TypeServicePoint(models.Model):
    OTHER = -1
    SM = 0
    POS = 1
    OIL = 2

    Type = (
        (OTHER, 'Другое'),
        (SM, 'Система управления'),
        (POS, 'Касса'),
        (OIL, 'Контроллер'),
    )

    name = models.CharField(verbose_name="Название", max_length=50, blank=True, null=True, default=None)
    type = models.IntegerField(verbose_name='Тип', choices=Type, default=OTHER, blank=False, null=False)

    def __str__(self):
        return "%s" % (self.name)

    class Meta:
        verbose_name = 'Тип АРМ'
        verbose_name_plural = 'Типы АРМ'


# точка обслуживания (АРМ)
class ServicePoint(models.Model):
    azs = models.ForeignKey(Azs, verbose_name='АЗК/АЗС', on_delete=models.DO_NOTHING)
    type = models.ForeignKey(TypeServicePoint, verbose_name='Тип АРМ', on_delete=models.DO_NOTHING)
    description = models.TextField(verbose_name='Комментарий', blank=True, null=True, default=None)
    is_active = models.BooleanField(verbose_name="Активный", default=True)
    created = models.DateTimeField(verbose_name="Создан", auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(verbose_name="Изменен", auto_now_add=False, auto_now=True)

    def __str__(self):
        return "%s - %s" % (self.azs.full_name, self.type )

    class Meta:
        verbose_name = 'АРМ'
        verbose_name_plural = 'АРМы'


# Название характеристик для рабочего места
class TypeCharacteristicSP(models.Model):
    OTHER = -1
    IP = 0
    OS = 1

    Type = (
        (OTHER, 'Другое'),
        (IP, 'IP адрес'),
        (OS, 'Операционная система'),
    )

    name = models.CharField(verbose_name="Название", max_length=50, blank=True, null=True, default=None)
    type = models.IntegerField(verbose_name='Тип', choices=Type, default=OTHER, blank=False, null=False)
    is_active = models.BooleanField(verbose_name="Активный", default=True)
    created = models.DateTimeField(verbose_name="Создан", auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(verbose_name="Изменен", auto_now_add=False, auto_now=True)

    def __str__(self):
        return "%s" % (self.name)

    class Meta:
        verbose_name = 'Тип характеристики АРМ'
        verbose_name_plural = 'Типы характеристик АРМ'


# Характеристики АРМ
class CharacteristicSP(models.Model):
    service_point = models.ForeignKey(ServicePoint,  on_delete=models.DO_NOTHING)
    type = models.ForeignKey(TypeCharacteristicSP, on_delete=models.DO_NOTHING)
    value1 = models.CharField(verbose_name="Значение 1", max_length=100, blank=True, null=True, default=None)
    value2 = models.CharField(verbose_name="Значение 2", max_length=100, blank=True, null=True, default=None)
    value3 = models.CharField(verbose_name="Значение 3", max_length=100, blank=True, null=True, default=None)
    value4 = models.CharField(verbose_name="Значение 4", max_length=100, blank=True, null=True, default=None)
    description = models.TextField(verbose_name='Комментарий', blank=True, null=True, default=None)
    is_active = models.BooleanField(verbose_name="Активный", default=True)
    created = models.DateTimeField(verbose_name="Создан", auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(verbose_name="Изменен", auto_now_add=False, auto_now=True)

    def __str__(self):
        return "%s - %s  -  %s" % (self.type, self.value1, self.value2)

    class Meta:
        verbose_name = 'Характеристика АРМ'
        verbose_name_plural = 'Характеристики АРМ'


# Физические лица
class Person(models.Model):
    name = models.CharField(verbose_name="ФИО", max_length=100, blank=True, null=True, default=None)
    phone = models.CharField(verbose_name="Телефон", max_length=100, blank=True, null=True, default=None)
    telegram_id = models.IntegerField(verbose_name="ID telegram", blank=True, null=True, default=None, unique=True)
    description = models.TextField(verbose_name='Комментарий', blank=True, null=True, default=None)
    is_active = models.BooleanField(verbose_name="Активный", default=True)
    created = models.DateTimeField(verbose_name="Создан", auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(verbose_name="Изменен", auto_now_add=False, auto_now=True)

    def __str__(self):
        return "%s" % (self.name)

    class Meta:
        verbose_name = 'Физическое лицо'
        verbose_name_plural = 'Физические лица'


# Должности
class Position(models.Model):
    name = models.CharField(verbose_name="Название", max_length=100, blank=True, null=True, default=None)
    description = models.TextField(verbose_name='Комментарий', blank=True, null=True, default=None)
    is_active = models.BooleanField(verbose_name="Активный", default=True)
    created = models.DateTimeField(verbose_name="Создан", auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(verbose_name="Изменен", auto_now_add=False, auto_now=True)

    def __str__(self):
        return "%s" % (self.name)

    class Meta:
        verbose_name = 'Должность'
        verbose_name_plural = 'Должности'


# Роли в ТХ
class Permission(models.Model):
    name = models.CharField(verbose_name="Название", max_length=100, blank=True, null=True, default=None)
    description = models.TextField(verbose_name='Комментарий', blank=True, null=True, default=None)
    is_active = models.BooleanField(verbose_name="Активный", default=True)
    created = models.DateTimeField(verbose_name="Создан", auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(verbose_name="Изменен", auto_now_add=False, auto_now=True)

    def __str__(self):
        return "%s" % (self.name)

    class Meta:
        verbose_name = 'Роль в TradeHouse'
        verbose_name_plural = 'Роли в TradeHouse'


# Сотрудники
class EmployeesAZK(models.Model):
    IN_PROCESSING = 0
    ACTIVE = 1
    BLOCKED = 2

    Status = (
        (IN_PROCESSING, 'В обработке'),
        (ACTIVE, 'Активный'),
        (BLOCKED, 'Заблокированный'),
    )
    azk = models.ForeignKey(Azs, verbose_name="АЗК", on_delete=models.DO_NOTHING)
    person = models.ForeignKey(Person, verbose_name="Физ. лицо", on_delete=models.DO_NOTHING)
    position = models.ForeignKey(Position, verbose_name="Должность", on_delete=models.DO_NOTHING, blank=True, null=True, default=None)
    permission = models.ManyToManyField(Permission, verbose_name="Роли")
    status = models.IntegerField(verbose_name='Статус', choices=Status, default=IN_PROCESSING, blank=False, null=False)
    login = models.CharField(verbose_name="Логин", max_length=100, blank=True, null=True, default=None)
    password = models.CharField(verbose_name="Пароль", max_length=100, blank=True, null=True, default=None)
    description = models.TextField(verbose_name='Комментарий', blank=True, null=True, default=None)
    is_active = models.BooleanField(verbose_name="Активный", default=True)
    created = models.DateTimeField(verbose_name="Создан", auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(verbose_name="Изменен", auto_now_add=False, auto_now=True)

    def __str__(self):
        return "%s (%s)" % (self.person, self.azk)

    class Meta:
        verbose_name = 'Сотрудник АЗК'
        verbose_name_plural = 'Сотрудники АЗК'