from django.core.management.base import BaseCommand
import csv, sys, os
from portalotp.settings import MEDIA_ROOT
from main.models import *


class Command(BaseCommand):
    help = 'Import AZK from CSV'

    def import_to_azk(self, azk_list):
        for azk_obj in azk_list[1:]:
            # получаем или создаем менеджеров
            manager = Personal.objects.filter(fio=azk_obj["manager"], phone=azk_obj["manager_phone"])
            if manager.count() == 0:
                Personal.objects.filter(fio=azk_obj["manager"]).update_or_create(fio=azk_obj["manager"],
                                                                                 phone=azk_obj["manager_phone"])
                manager = Personal.objects.filter(fio=azk_obj["manager"], phone=azk_obj["manager_phone"])
            manager = manager.first()

            # получаем или создаем группу АЗК
            azk_group = AzsGroup.objects.filter(name=azk_obj["azk_group"])
            if azk_group.count() == 0:
                AzsGroup.objects.filter(name=azk_obj["azk_group"]).update_or_create(name=azk_obj["azk_group"])
                azk_group = AzsGroup.objects.filter(name=azk_obj["azk_group"])
            azk_group = azk_group.first()

            azk = Azs.objects.filter(name=azk_obj["azk_name"]).update_or_create(
                name=azk_obj["azk_name"],
                full_name=azk_obj["azk_full_name"],
                sublan=azk_obj["sublan"],
                phone=azk_obj["azk_phone"],
                eMail=azk_obj["email"],
                manager=manager,
                address=azk_obj["address"],
                azs_group=azk_group
            )

            self.stdout.write(self.style.SUCCESS("AZK: " + azk + "  Group: " + azk_group + " Manager: " + manager))

    def handle(self, *args, **options):
        path = os.path.join(MEDIA_ROOT, 'importAZK.csv')

        azk_list = list()
        data = csv.reader(open(path, encoding='cp1251'), delimiter=";")
        for row in data:
            azk_obj = dict()
            azk_obj.update({"pp": row[0]})
            azk_obj.update({"azk_name": row[1]})
            azk_obj.update({"azk_full_name": row[2]})
            azk_obj.update({"address": row[3]})
            azk_obj.update({"email": row[4]})
            azk_obj.update({"azk_phone": row[5]})
            azk_obj.update({"manager": row[6]})
            azk_obj.update({"manager_phone": row[7]})
            azk_obj.update({"azk_group": row[8]})
            azk_obj.update({"sublan": row[9]})
            azk_list.append(azk_obj)

        self.import_to_azk(azk_list)
