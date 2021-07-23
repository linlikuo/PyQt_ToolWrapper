import os, paramiko, subprocess
import time
from stat import S_ISDIR as isdir
from PyQt5 import QtCore

import utils


class Server(QtCore.QThread):
    download_progress_signal = QtCore.pyqtSignal(int)

    def __init__(self, hostname, username, password, port=22, parent=None, progressBar=None):
        super(Server, self).__init__()
        self._hostname = hostname
        self._username = username
        self._password = password
        self._port = port
        self._ssh = None
        self._sftp = None
        self._msg = ''
        self._status = None
        self._parent = parent
        self._statusTimer = QtCore.QTimer(self._parent)
        self._statusTimer.timeout.connect(self.check_available)
        self._connectTimer = QtCore.QTimer(self._parent)
        self._connectTimer.timeout.connect(self.connect)
        self._reconnect = True
        self.workToDo = [] # list of (from, to)
        self._startdownload_flag = False
        self._startevaluate_flag = False
        self._start_after_evaluate_flag = False
        self.evalute_pair_list = []
        self.progressBar = progressBar

    def startStatusTimer(self):
        self._statusTimer.start(7000)

    def endStatusTimer(self):
        self._statusTimer.stop()

    def startConnectTimer(self):
        self._connectTimer.start(7000)

    def endConnectTimer(self):
        self._connectTimer.stop()

    def check_available(self):
        #HOST_DOWN = True if os.system('ping -w {timeout} -n 1 {ip}'.format(timeout=1, ip=self._hostname)) else False
        DETACHED_PROCESS = 0x00000008
        HOST_DOWN = True if subprocess.call('ping -w {timeout} -n 1 {ip}'.format(timeout=1, ip=self._hostname), creationflags=DETACHED_PROCESS) else False
        if HOST_DOWN:
            print('not available')
            self._status = 'Offline'
            self._reconnect = True
            self._ssh = None
            self._sftp = None
            return False
        return True

    def connect(self):
        if self._reconnect:
            if self.check_available():

                try:
                    self._ssh = paramiko.SSHClient()
                    self._ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                    self._ssh.connect(hostname=self._hostname, port=self._port, username=self._username, password=self._password)
                    self._sftp = self._ssh.open_sftp()
                    self._reconnect = False
                    self._status = 'Online'
                except:
                    print('Failed to build connection between server.\n')
                    self._reconnect = True
                    self._status = 'Offline'



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

    def startDownload(self):
        self._startdownload_flag = True

    def stopDownload(self):
        self._startdownload_flag = False

    def startEvalute(self, start_after_evaluate_flag = False):
        self._startevaluate_flag = True
        if start_after_evaluate_flag:
            self._start_after_evaluate_flag = start_after_evaluate_flag


    def stopEvalute(self):
        self._startevaluate_flag = False

    def evaluateWorkVolume(self, work_pair=None):
        if not work_pair:
            return
        remote_dir_name, local_dir_name = work_pair
        remote_file = self._sftp.stat(remote_dir_name)
        if isdir(remote_file.st_mode):
            self.check_local_dir(local_dir_name)
            remote_file_name_list = self._sftp.listdir(remote_dir_name)
            sub_remote_list = list(map(lambda x : '/'.join([remote_dir_name, x]), remote_file_name_list))
            sub_local_list = list(map(lambda x: os.path.join(local_dir_name, x), remote_file_name_list))
            for pair in list(zip(sub_remote_list, sub_local_list)):
                self.evaluateWorkVolume(pair)
        else:
            self.workToDo += [(remote_dir_name, local_dir_name)]
            return

    def addWork(self, _from, _to):
        if _from and _to:
            self.evalute_pair_list += [(_from, _to)]


    def run(self):
        amount_work = 0
        while True:
            if self._startevaluate_flag:
                if self.evalute_pair_list:
                    _from, _to = self.evalute_pair_list.pop(0)
                    self.evaluateWorkVolume((_from, _to))
                    if not self.evalute_pair_list:
                        self.stopEvalute()
                        if self._start_after_evaluate_flag:
                            self._start_after_evaluate_flag = False
                            self._startdownload_flag = True

            if self._startdownload_flag:
                amount_work = len(self.workToDo)
                if not self.workToDo:
                    self.stopDownload()
                    amount_work = 0
                else:
                    remote_dir_name, local_dir_name = self.workToDo.pop(0)
                    self.download_from_remote(remote_dir_name, local_dir_name)
                    self.download_progress_signal.emit(int((1-(len(self.workToDo)/amount_work))*100))


    def check_local_dir(self, local_dir_name):
        if not os.path.exists(local_dir_name):
            os.makedirs(local_dir_name)

    def getMessage(self):
        return self._msg

    def __str__(self):
        attrs = vars(self)
        return ', '.join("%s: %s" % item for item in attrs.items())