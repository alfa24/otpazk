from django.core.management.base import BaseCommand
from main.models import *


class Command(BaseCommand):
    def handle(self, *args, **options):
        persons = Person.objects.all()
        for person in persons:
            person.hr = False
            person.is_active = False
            person.save()
