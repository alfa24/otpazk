from django.core.management import call_command

def cron_task():
    print("DEBUG: call manage.py task")
    call_command('task')

