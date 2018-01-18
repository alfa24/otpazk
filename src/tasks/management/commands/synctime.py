from bot.models import SlackNotice
from django.core.management.base import BaseCommand
import paramiko
import datetime

from main.models import CharacteristicSP, TypeServicePoint, TypeCharacteristicSP


def synctime(ip):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip, username="ufo", password="ufo17azk")
        cur_date = datetime.datetime.today()
        channel = ssh.get_transport().open_session()
        channel.get_pty()
        channel.settimeout(5)
        channel.exec_command('su')
        msg = channel.recv(1024)
        channel.send('admin17azk\n')
        msg = channel.recv(1024)
        channel.send('date --set ' + str(cur_date.hour) + ':' + str(cur_date.minute) + ':' + str(cur_date.second) + '\n')
        print("Set TIME: " + str(cur_date.hour) + ':' + str(cur_date.minute) + ':' + str(cur_date.second))
        msg = channel.recv(1024)
        msg = channel.recv(1024)
        channel.close()
    except Exception as e:
        raise e


class Command(BaseCommand):
    help = 'Linux sync time'

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
            notice.send('Ошибка установки времени!',attachments)

    def handle(self, *args, **options):
        if len(options['service_point_id']) != 0:
            chr = CharacteristicSP.objects.filter(service_point_id=options['service_point_id'][0])
            for c in chr:
                if c.type.type == TypeCharacteristicSP.IP:
                    if c.service_point.type.type == TypeServicePoint.POS or c.service_point.type.type == TypeServicePoint.OIL:
                        ip = c.value1
                        self.stdout.write(self.style.SUCCESS("Service point: " + str(c.service_point)))
                        try:
                            synctime(ip)
                        except:
                            self.send_to_slack(c.service_point, ip)
