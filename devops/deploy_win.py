import paramiko


def main(ip):
    try:
        username = 'root'
        password = input('Enter password: ')
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip, username=username, password=password)

        channel = ssh.get_transport().open_session()
        channel.get_pty()
        channel.settimeout(5)

        channel.exec_command('cd /opt/otpazk/ && git pull')
        msg = 1
        while msg != b'':
            msg = channel.recv(1024)
            print(msg)

        channel = ssh.get_transport().open_session()
        channel.get_pty()
        channel.settimeout(5)

        channel.exec_command('cd /opt/otpazk/ && ./deploy_localhost.sh')

        msg = 1
        while msg != b'':
            msg = channel.recv(1024)
            print(msg)

        channel.close()

    except Exception as e:
        print('Error: ' + ip)
        raise e


main('10.248.179.130')
