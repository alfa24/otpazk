import os

from bot.models import SlackNotice
from django.core.management.base import BaseCommand
import paramiko
import datetime
from django.conf import settings

from main.models import CharacteristicSP, TypeServicePoint, TypeCharacteristicSP


def backup(ip):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(ip, username=settings.__getattr__('POS_USERNAME'),
                    password=settings.__getattr__('POS_PASSWORD'))
    except paramiko.ssh_exception.AuthenticationException as e:
        ssh.connect(ip, username=settings.__getattr__('POS_USERNAME'),
                    password=settings.__getattr__('POS_OLD_PASSWORD'))

    channel = ssh.get_transport().open_session()
    channel.get_pty()
    channel.settimeout(5)
    channel.exec_command('hostname')
    msg = channel.recv(1024)
    hostname = msg.decode('utf-8').rstrip()
    if hostname.__len__() < 8:
        hostname = ip + '_' + hostname
    channel.close()
    print("Имя компьютера: " + hostname)

    # создаем папку АЗК
    path_to_backup = settings.__getattr__('BACKUP_ROOT') + '/'
    sftp = ssh.open_sftp()
    if not os.path.exists(path_to_backup):
        os.mkdir(path_to_backup)

    # заливаем скрипт
    print("заливаем скрипт")
    file_list = ['bkp.sh']
    remote_path = "/home/ufo/.UFO/"
    local_path = settings.__getattr__('BACKUP_SCRIPTS') + '/'
    for file in file_list:
        try:
            sftp.remove(remote_path + file)
        except:
            pass
            # такого файла нет
        sftp.put(local_path + file, remote_path + file)

    # запускаем скрипт
    print("запускаем скрипт")
    channel = ssh.get_transport().open_session()
    channel.get_pty()
    channel.exec_command('cd /home/ufo/.UFO/ && chmod +rwx bkp.sh &&  ./bkp.sh')
    msg = 1
    while msg != b'':
        msg = channel.recv(1024)
        # print(msg)
    channel.close()

    # скачиваем архив
    print("скачиваем архив")
    file_list = ['bkp.tar.gz']
    remote_path = "/home/ufo/.UFO/"
    # local_path = ip + '/'
    local_path = path_to_backup
    new_file = ''
    for file in file_list:
        if not os.path.exists(local_path + file):
            sftp.get(remote_path + file, local_path + file)
            date = datetime.datetime.now()
            # переименовываем файл
            new_file = 'bkp_' + hostname + date.strftime("_%y_%m_%d.tar.gz")
            os.rename(local_path + file, local_path + new_file)

    print("Бэкап выполнен: " + new_file)
    print("отключаемся")
    ssh.close()
    # return cur_date, then, delta_minutes


class Command(BaseCommand):
    help = 'Linux check time'

    def add_arguments(self, parser):
        parser.add_argument('service_point_id', nargs='*', type=int)

    def send_to_slack(self, sp, ip, error_text):
        main_text = 'Ошибка получения бэкапа'

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
                        "title": 'Текст ошибки:',
                        "value": str(error_text),
                        "short": False,
                    },
                ],
            },
        ]
        noticies = SlackNotice.objects.filter(type=SlackNotice.ERROR_BACKUP)
        for notice in noticies:
            notice.send(main_text, attachments)

    def handle(self, *args, **options):
        k = 0
        chr = CharacteristicSP.objects.filter(service_point__type__type=TypeServicePoint.POS)
        for c in chr:
            if c.type.type == TypeCharacteristicSP.IP:
                if c.service_point.type.type == TypeServicePoint.POS or c.service_point.type.type == TypeServicePoint.OIL:
                    ip = c.value1
                    error_text = ''
                    try:
                        self.stdout.write(self.style.SUCCESS("Подключение к " + str(c.service_point)))
                        backup(ip)
                    except paramiko.ssh_exception.AuthenticationException:
                        error_text = 'Не подходит логин или пароль.'
                    except TimeoutError:
                        error_text = 'Таймаут подключения к хосту.'
                    except Exception as e:
                        error_text = 'Ошибка: ' + e.__str__()
                    if error_text:
                        self.stdout.write(self.style.ERROR(error_text))
                        self.send_to_slack(c.service_point, ip, error_text)
