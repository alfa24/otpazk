from bot.models import SlackNotice
from django.core.management.base import BaseCommand
import paramiko
import datetime

from main.models import CharacteristicSP, TypeServicePoint, TypeCharacteristicSP


def checktime(ip):
    try:
        text = ip
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip, username="ufo", password="ufo17azk")

        cur_date = datetime.datetime.today()
        channel = ssh.get_transport().open_session()
        channel.get_pty()
        channel.settimeout(5)
        channel.exec_command('date')
        text += ": " + str(cur_date.hour) + ':' + str(cur_date.minute) + ':' + str(cur_date.second) + ' - '

        msg = channel.recv(1024)
        print(text, msg[11:24])
        msg = channel.recv(1024)
        #print(msg)
        channel.close()

    except Exception as e:
        #print('Ошибка: ' + ip)
        raise e


class Command(BaseCommand):
    help = 'Linux check time'

    def add_arguments(self, parser):
        parser.add_argument('service_point_id', nargs='*', type=int)

    def send_to_slack(self, sp, ip):
        main_text = 'Ошибка установки времени!'

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
                ],
            },
        ]
        noticies = SlackNotice.objects.filter(type=SlackNotice.ERROR_SYNCTIME)
        for notice in noticies:
            notice.send('Ошибка установки времени!', attachments)

    def handle(self, *args, **options):

        chr = CharacteristicSP.objects.filter(service_point__type__type=TypeServicePoint.POS)
        for c in chr:
            if c.type.type == TypeCharacteristicSP.IP:
                if c.service_point.type.type == TypeServicePoint.POS or c.service_point.type.type == TypeServicePoint.OIL:
                    ip = c.value1
                    self.stdout.write(self.style.SUCCESS("Service point: " + str(c.service_point)))
                    try:
                        checktime(ip)
                    except:
                        pass
                #self.send_to_slack(c.service_point, ip)
