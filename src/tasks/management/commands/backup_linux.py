import os

from bot.models import SlackNotice
from django.core.management.base import BaseCommand
import paramiko
import datetime
from django.conf import settings
from django.db.models import Q

from main.models import CharacteristicSP, TypeServicePoint, TypeCharacteristicSP


def log(message, path_to_log):
    f = open(path_to_log + 'log.txt', 'a')
    time = datetime.datetime.now()
    f.write(time.strftime("%d.%m.%y %H:%M:   ") + message + '\n')
    f.close()
    print(message)


def backup(ip, path_to_backup, path_to_log):
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
    log("\t\tИмя компьютера: " + hostname, path_to_log)

    sftp = ssh.open_sftp()
    # заливаем скрипт
    log("\t\tзаливаем скрипт", path_to_log)
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
    log("\t\tзапускаем скрипт", path_to_log)
    channel = ssh.get_transport().open_session()
    channel.get_pty()
    channel.exec_command('cd /home/ufo/.UFO/ && chmod +rwx bkp.sh &&  ./bkp.sh')
    msg = 1
    while msg != b'':
        msg = channel.recv(1024)
        # print(msg)
    channel.close()

    # скачиваем архив
    log("\t\tскачиваем архив", path_to_log)
    file_list = ['bkp.tar.gz']
    remote_path = "/home/ufo/.UFO/"
    # local_path = ip + '/'
    local_path = path_to_backup
    new_file = ''
    for file in file_list:
        if not os.path.exists(local_path + file):
            sftp.get(remote_path + file, local_path + file)
            # переименовываем файл
            new_file = 'bkp_' + hostname + ".tar.gz"
            os.rename(local_path + file, local_path + new_file)

    log("\t\tБэкап выполнен: " + new_file, path_to_log)
    log("\t\tотключаемся", path_to_log)
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
        # создаем папку с архивами "yyyy.mm.dd"
        path_to_backup = settings.__getattr__('BACKUP_ROOT') + '/'
        if not os.path.exists(path_to_backup):
            os.mkdir(path_to_backup)
        date = datetime.datetime.now()
        path_to_backup += date.strftime("%Y.%m.%d") + '/'
        if not os.path.exists(path_to_backup):
            os.mkdir(path_to_backup)
        path_to_log = path_to_backup

        chr = CharacteristicSP.objects.filter(
            Q(service_point__type__type=TypeServicePoint.POS, service_point__is_active=True) or
            Q(service_point__type__type=TypeServicePoint.OIL, service_point__is_active=True)
        )
        sp_count = chr.count()
        sp_complete = 0
        for c in chr:
            if c.type.type == TypeCharacteristicSP.IP:
                ip = c.value1
                error_text = ''
                try:
                    # создаем папку с номером азк
                    path_bkp_azk = path_to_backup + str(c.service_point.azs.name) + '/'
                    if not os.path.exists(path_bkp_azk):
                        os.mkdir(path_bkp_azk)

                    # запускаем выполнение архивации
                    log("Подключение к " + str(c.service_point), path_to_log)
                    backup(ip, path_bkp_azk, path_to_log)
                    sp_complete += 1
                except paramiko.ssh_exception.AuthenticationException:
                    error_text = 'Не подходит логин или пароль.'
                except TimeoutError:
                    error_text = 'Таймаут подключения к хосту.'
                except Exception as e:
                    error_text = 'Ошибка: ' + e.__str__()
                if error_text:
                    log(error_text, path_to_log)
                    self.send_to_slack(c.service_point, ip, error_text)

                log("\t\t", path_to_log)
                log("\t\t", path_to_log)

        log("Задание по выполнению архивации параметров Linux выполнена на %s из %s ПК" % (
            sp_complete, sp_count
        ), path_to_log)
