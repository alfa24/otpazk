from django.core.management.base import BaseCommand
import csv, sys, os
from portalotp.settings import MEDIA_ROOT
from main.models import *


class Command(BaseCommand):
    help = 'Import service point from CSV'
    COLUMN_NAME_OS = 'Операционная система'
    TYPE_CHR_OS = TypeCharacteristicSP.OS
    COLUMN_NAME_IP = 'IP адрес'
    TYPE_CHR_IP = TypeCharacteristicSP.IP

    def parse(self, obj_list):
        columns = obj_list[0]

        for obj in obj_list[1:]:
            if Azs.objects.filter(full_name=obj["azk_name"]).count() > 0:
                azk = Azs.objects.filter(full_name=obj["azk_name"]).first()

                # Кассы
                for i in range(1, 4):
                    if len(obj['pos' + str(i)]) > 0:
                        self.create_obj(azk, 'pos' + str(i), columns, obj, 'Linux', TypeServicePoint.POS)

                self.create_obj(azk, 'th', columns, obj, 'Windows 7', TypeServicePoint.SM)
                self.create_obj(azk, 'mfu', columns, obj, '', TypeServicePoint.OTHER)
                self.create_obj(azk, 'mail', columns, obj, 'Windows 7', TypeServicePoint.OTHER)
                if len(obj['oil']) > 0:
                    self.create_obj(azk, 'oil', columns, obj, 'Linux', TypeServicePoint.OIL)

    def create_obj(self, azk, name_col, columns, obj_sp, str_os, type_service_pont):

        # Создаем тип точки обслуживания
        obj = TypeServicePoint.objects.filter(name=columns[name_col], type=type_service_pont)
        if obj.count() == 0:
            TypeServicePoint.objects.filter(name=columns[name_col], type=type_service_pont).update_or_create(
                name=columns[name_col],
                type=type_service_pont
            )
            obj = TypeServicePoint.objects.filter(name=columns[name_col], type=type_service_pont)
            self.stdout.write(self.style.SUCCESS("CREATE TYPE SP: " + columns[name_col]))
        type_sp = obj.first()

        # Создаем точку обслуживания
        obj = ServicePoint.objects.filter(azs=azk, type=type_sp)
        if obj.count() == 0:
            ServicePoint.objects.filter(azs=azk, type=type_sp).update_or_create(
                azs=azk,
                type=type_sp
            )
            obj = ServicePoint.objects.filter(azs=azk, type=type_sp)
            self.stdout.write(self.style.SUCCESS("CREATE Service Point: " + str(type_sp) + ' (' + str(azk) + ')'))
        service_point = obj.first()

        # создаем характеристики ip-адрес
        obj = TypeCharacteristicSP.objects.filter(name=self.COLUMN_NAME_IP, type=self.TYPE_CHR_IP)
        if obj.count() == 0:
            TypeCharacteristicSP.objects.filter(name=self.COLUMN_NAME_IP, type=self.TYPE_CHR_IP).update_or_create(
                name=self.COLUMN_NAME_IP,
                type=self.TYPE_CHR_IP
            )
            obj = TypeCharacteristicSP.objects.filter(name=self.COLUMN_NAME_IP, type=self.TYPE_CHR_IP)
            self.stdout.write(self.style.SUCCESS("CREATE TYPE CHR: " + self.COLUMN_NAME_IP))
        type_chr = obj.first()

        if len(obj_sp[name_col]) > 0:
            obj = CharacteristicSP.objects.filter(service_point=service_point, type=type_chr,
                                                  value1=obj_sp[name_col])
            if obj.count() == 0:
                CharacteristicSP.objects.filter(service_point=service_point, type=type_chr,
                                                value1=obj_sp[name_col]).update_or_create(
                    service_point=service_point,
                    type=type_chr,
                    value1=obj_sp[name_col]
                )
                self.stdout.write(self.style.SUCCESS(
                    "CREATE CHR: %s  -  %s   -   %s: %s" % (azk, service_point, type_chr, obj_sp[name_col])))

        obj = TypeCharacteristicSP.objects.filter(name=self.COLUMN_NAME_OS, type=self.TYPE_CHR_OS)
        if obj.count() == 0:
            TypeCharacteristicSP.objects.filter(name=self.COLUMN_NAME_OS, type=self.TYPE_CHR_OS).update_or_create(
                name=self.COLUMN_NAME_OS,
                type=self.TYPE_CHR_OS
            )
            obj = TypeCharacteristicSP.objects.filter(name=self.COLUMN_NAME_OS, type=self.TYPE_CHR_OS)
            self.stdout.write(self.style.SUCCESS("CREATE TYPE CHR: " + self.COLUMN_NAME_OS))
        type_chr = obj.first()

        if len(str_os) > 0:
            obj = CharacteristicSP.objects.filter(service_point=service_point, type=type_chr, value1=str_os)
            if obj.count() == 0:
                CharacteristicSP.objects.filter(service_point=service_point, type=type_chr,
                                                value1=str_os).update_or_create(
                    service_point=service_point,
                    type=type_chr,
                    value1=str_os
                )
                self.stdout.write(self.style.SUCCESS(
                    "CREATE CHR: %s  -  %s   -   %s: %s" % (azk, service_point, type_chr, str_os)))

    def handle(self, *args, **options):
        path = os.path.join(MEDIA_ROOT, 'importSP.csv')

        obj_list = list()
        data = csv.reader(open(path, encoding='cp1251'), delimiter=";")
        for row in data:
            obj = dict()
            obj.update({"pp": row[0]})
            obj.update({"azk_name": row[1]})
            obj.update({"pos1": row[2]})
            obj.update({"pos2": row[3]})
            obj.update({"pos3": row[4]})
            obj.update({"th": row[5]})
            obj.update({"mfu": row[6]})
            obj.update({"mail": row[7]})
            obj.update({"oil": row[8]})
            obj_list.append(obj)

        self.parse(obj_list)
