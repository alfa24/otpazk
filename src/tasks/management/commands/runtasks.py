from django.core import management
from django.core.management.base import BaseCommand

from tasks.models import Task


class Command(BaseCommand):
    help = 'Run tasks'

    def handle(self, *args, **options):
        tasks = Task.objects.filter(is_active=True)
        for task in tasks:
            for sp in task.service_point.all():
                management.call_command(task.task, str(sp.id))
        pass
