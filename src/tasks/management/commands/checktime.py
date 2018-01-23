from bot.models import SlackNotice
from django.core.management.base import BaseCommand
import paramiko
import datetime
from django.conf import settings

from main.models import CharacteristicSP, TypeServicePoint, TypeCharacteristicSP


def checktime(ip, service_point):
    text = ip
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        ssh.connect(ip, username=settings.__getattr__('POS_USERNAME'),
                    password=settings.__getattr__('POS_PASSWORD'))
    except paramiko.ssh_exception.AuthenticationException as e:
        ssh.connect(ip, username=settings.__getattr__('POS_USERNAME'),
                    password=settings.__getattr__('POS_OLD_PASSWORD'))

    cur_date = datetime.datetime.today()

    channel = ssh.get_transport().open_session()
    channel.get_pty()
    channel.settimeout(5)
    channel.exec_command('date')
    msg = channel.recv(1024).decode('utf-8')

    text += ": " + str(cur_date.hour) + ':' + str(cur_date.minute) + ':' + str(cur_date.second) + ' - '
    print(service_point, text, msg[10:19])

    then = datetime.datetime(cur_date.year, cur_date.month, cur_date.day, int(msg[11:13]), int(msg[14:16]), 00)
    ntptime = datetime.datetime(cur_date.year, cur_date.month, cur_date.day, cur_date.hour, cur_date.minute,
                                cur_date.second)
    delta = then - ntptime
    seconds = delta.total_seconds()
    delta_minutes = (seconds // 60) + 1

    msg = channel.recv(1024)
    channel.close()
    return cur_date, then, delta_minutes


class Command(BaseCommand):
    help = 'Linux check time'

    def add_arguments(self, parser):
        parser.add_argument('service_point_id', nargs='*', type=int)

    def send_to_slack(self, sp, ip, then, cur_date, delta_minutes):
        main_text = 'Расходится время ' + str(delta_minutes) + ' минут!'

        attachments = [
            {
                'fields': [
                    {
                        "title": 'Точка обслуживания:',
                        "value": str(sp),
                        "short": False,
                    },
                    {
                        "title": 'Ip - адрес:',
                        "value": ip,
                        "short": False,
                    },
                    {
                        "title": 'Точное время:',
                        "value": str(cur_date),
                        "short": False,
                    },
                    {
                        "title": 'Время на кассе:',
                        "value": str(then),
                        "short": False,
                    },
                ],
            },
        ]
        noticies = SlackNotice.objects.filter(type=SlackNotice.ERROR_SYNCTIME)
        for notice in noticies:
            notice.send(main_text, attachments)

    def handle(self, *args, **options):
        chr = CharacteristicSP.objects.filter(service_point__type__type=TypeServicePoint.POS)
        for c in chr:
            if c.type.type == TypeCharacteristicSP.IP:
                if c.service_point.type.type == TypeServicePoint.POS or c.service_point.type.type == TypeServicePoint.OIL:
                    ip = c.value1
                    error_text = ''
                    try:
                        self.stdout.write(self.style.SUCCESS("Подключение к " + str(c.service_point)))
                        cur_date, then, delta_minutes = checktime(ip, c.service_point)
                        if int(delta_minutes) >= 5 or int(delta_minutes) <= -5:
                            self.stdout.write(
                                self.style.ERROR("Расходится время на " + str(delta_minutes) + " минут: "))
                            self.stdout.write(self.style.ERROR("Service point: " + str(c.service_point)))
                            self.stdout.write(
                                self.style.ERROR(
                                    "Время на кассе: " + str(then) + "    Точное время: " + str(cur_date)))
                            self.send_to_slack(c.service_point, ip, then, cur_date, delta_minutes)
                        else:
                            self.stdout.write(self.style.SUCCESS("Расхождение на " + str(delta_minutes) + " минут"))
                        self.stdout.write(self.style.SUCCESS(" "))
                    except paramiko.ssh_exception.AuthenticationException:
                        error_text = 'Не подходит логин или пароль.'
                    except TimeoutError:
                        error_text = 'Таймаут подключения к хосту.'
                    except Exception as e:
                        error_text = 'Ошибка: ' + e.__str__()
                    if error_text:
                        self.stdout.write(self.style.ERROR(error_text))
                        # # self.send_to_slack(c.service_point, ip)
