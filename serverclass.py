import os, paramiko
from stat import S_ISDIR as isdir
class Server:
    def __init__(self, hostname, username, password, port=22):
        self._hostname = hostname
        self._username = username
        self._password = password
        self._port = port
        self._ssh = None
        self._sftp = None
        self._msg = ''
        self._status = None

    def connect(self):
        if not self._ssh:
            self._ssh = paramiko.SSHClient()
        self._ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self._ssh.connect(hostname=self._hostname, port=self._port, username=self._username, password=self._password)
        self._sftp = self._ssh.open_sftp()

    def sendCommand(self, cmd, clear=False):
        if clear:
            self._msg = ''
        if not self._ssh:
            self._msg = 'No connection between server\n'
            return
        _, stdout, _ = self._ssh.exec_command(cmd)
        for line in stdout.readlines():
            self._msg += line

    def download_from_remote(self, remote_dir_name, local_dir_name):
        remote_file = self._sftp.stat(remote_dir_name)
        if isdir(remote_file.st_mode):
            self.check_local_dir(local_dir_name)
            print('Start downloading folder: '+remote_dir_name)
            for remote_file_name in self._sftp.listdir(remote_dir_name):
                sub_remote = '/'.join([remote_dir_name, remote_file_name])
                #sub_remote = sub_remote.replace(r'/', r'\\')
                sub_local = os.path.join(local_dir_name, remote_file_name)
                #sub_local = sub_local.replace(r'/', r'\\')
                self.download_from_remote(sub_remote, sub_local)
        else:
            print('Start downloading file: '+remote_dir_name)
            self._sftp.get(remote_dir_name, local_dir_name)


    def check_local_dir(self, local_dir_name):
        if not os.path.exists(local_dir_name):
            os.makedirs(local_dir_name)

    def getMessage(self):
        return self._msg

    def __str__(self):
        attrs = vars(self)
        return ', '.join("%s: %s" % item for item in attrs.items())