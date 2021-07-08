import os

import win32api
from PyQt5 import QtWidgets, QtGui, QtCore
from ToolWrapper import Ui_MainWindow
from windowclass import ToolItem
from managerclass import ToolItemManager
from serverclass import Server
from widgetmanager import ToolListTableManager
import sys, paramiko
import win32gui
import utils

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.settingsPath = 'settings.ini'
        self.defaultRootToolFolderPath = None
        self.nowToolFolderPath = None
        self.serverIP = None
        self.serverUsername = None
        self.serverPassword = None
        self.serverFwFolderPath = None
        self.serverToolFolderPath = None
        self.toollist = ToolListTableManager()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.LoadSettings()
        self.server = Server(hostname=self.serverIP, username=self.serverUsername, password=self.serverPassword)
        self.server.connect()
        self.ui.FwVersion_comboBox.popupAboutToBeShown.connect(self.update_FwVersion_comboBox)
        self.ui.ToolVersion_comboBox.popupAboutToBeShown.connect(self.update_ToolVersion_comboBox)
        self.ui.Build_pushButton.clicked.connect(self.buildButton_Clicked)
        self.ui.UpdateTool_pushButton.clicked.connect(self.updatetoolButton_Clicked)
        self.ui.UpdateFW_pushButton.clicked.connect(self.updatefwButton_Clicked)






        #item = ToolItem()
        #print(item)
        #if item.setUpAllWindow(consoleWindowName=r'C:\Users\NVMTG-C08\Desktop\App_20210609\App_U0622A0.exe', toolWindowName='NVMTG APP U0621', folderWindowName='App_20210609'):
        #    print('Find window successfully')
        #    print(item)

    def LoadSettings(self, path=None, group='Init'):
        if not path:
            path = self.settingsPath

        self.settings = QtCore.QSettings(path, QtCore.QSettings.IniFormat)
        self.settings.beginGroup(group)
        self.defaultRootToolFolderPath = os.path.join(os.environ['HOMEPATH'], 'Desktop', self.settings.value('DEFAULT_ROOT_TOOL_FOLDER_NAME'))
        self.nowToolFolderPath = self.defaultRootToolFolderPath
        self.serverIP = self.settings.value('SERVER_IP')
        self.serverUsername = self.settings.value('SERVER_USERNAME')
        self.serverPassword = self.settings.value('SERVER_PASSWORD')
        self.serverFwFolderPath = self.settings.value('SERVER_FW_FOLDER_PATH')
        self.serverToolFolderPath = self.settings.value('SERVER_TOOL_FOLDER_PATH')
        self.settings.endGroup()
        return True

    def changeSettingPath(self, path):
        self.settingsPath = path

    # Event function
    def buildButton_Clicked(self):
        if not self.ui.Username_lineEdit.text():
            print('Username can not be empty.')
        elif not self.ui.ToolName_lineEdit.text():
            print('Tool name can not be empty.')
        elif ((not self.ui.FolderName_lineEdit.text()) and (not self.ui.CustomizedToolPath_checkBox.isChecked())):
            print('Folder name can not be empty.')
        elif (not self.ui.CustomizedToolPath_checkBox.isChecked()) and ((self.ui.ToolVersion_comboBox.currentIndex() == 0) or (self.ui.FwVersion_comboBox.currentIndex() == 0)):
            print('Please choose Tool version and Fw version.')
        else:
            username = self.ui.Username_lineEdit.text()
            toolname = self.ui.ToolName_lineEdit.text()
            if self.ui.CustomizedToolPath_checkBox.isChecked():
                folderpath = self.ui.CustomizedToolPath_lineEdit.text()
            else:
                folderpath = '\\'.join([self.nowToolFolderPath, self.ui.FolderName_lineEdit.text()])

            info = 'ToolName:{},UserName:{},FolderPath:{},Footnotes:{}'.format(toolname, username, folderpath, ' ')

            if self.toollist.addItem(info):
                nowRowIndex = self.ui.ToolList_tableWidget.rowCount()
                self.ui.ToolList_tableWidget.insertRow(nowRowIndex)
                for cell in info.split(','):
                    index = cell.index(':')
                    value = cell[index+1:]
                    tableItem = QtWidgets.QTableWidgetItem(value)
                    tableItem.setFlags(tableItem.flags() ^ QtCore.Qt.ItemFlag.ItemIsEditable)
                    self.ui.ToolList_tableWidget.setItem(nowRowIndex, self.toollist.findColumnIndex(cell[:index]), tableItem)
                if not os.path.isdir(self.nowToolFolderPath):
                    os.mkdir(self.nowToolFolderPath)

                if not os.path.isdir(os.path.join(self.nowToolFolderPath, self.ui.FolderName_lineEdit.text())):
                    os.mkdir(os.path.join(self.nowToolFolderPath, self.ui.FolderName_lineEdit.text()))

                #print(self.ui.FwVersion_comboBox.currentText())
                self.server.download_from_remote('{}/{}'.format(self.serverFwFolderPath, self.ui.FwVersion_comboBox.currentText()), os.path.join(self.nowToolFolderPath, self.ui.FolderName_lineEdit.text()))
                self.server.download_from_remote('{}/{}'.format(self.serverToolFolderPath, self.ui.ToolVersion_comboBox.currentText()), os.path.join(self.nowToolFolderPath, self.ui.FolderName_lineEdit.text()))
            else:
                print('Can not add item, please make sure Tool name is unique.')


    def on_RefreshFWList_pushButton_clicked(self):
        self.server.sendCommand('ls {}'.format(self.serverFwFolderPath), clear=True)
        msg = self.server.getMessage()
        self.ui.FwVersion_comboBox.clear()
        self.ui.FwVersion_comboBox.insertItem(0, 'Select FW version.')
        index = 1
        for m in msg.split('\n'):
            if m:
                self.ui.FwVersion_comboBox.insertItem(index, m)
                index += 1

    def update_FwVersion_comboBox(self):
        self.server.sendCommand('ls {}'.format(self.serverFwFolderPath), clear=True)
        msg = self.server.getMessage()
        self.ui.FwVersion_comboBox.clear()
        self.ui.FwVersion_comboBox.insertItem(0, 'Select FW version.')
        index = 1
        for m in msg.split('\n'):
            if m:
                self.ui.FwVersion_comboBox.insertItem(index, m)
                index += 1

    def update_ToolVersion_comboBox(self):
        self.server.sendCommand('ls {}'.format(self.serverToolFolderPath), clear=True)
        msg = self.server.getMessage()
        self.ui.ToolVersion_comboBox.clear()
        self.ui.ToolVersion_comboBox.insertItem(0, 'Select Tool version.')
        index = 1
        for m in msg.split('\n'):
            if m:
                self.ui.ToolVersion_comboBox.insertItem(index, m)
                index += 1

    def updatetoolButton_Clicked(self):
        if self.ui.ToolVersion_comboBox.currentIndex() == 0:
            print('Please choose Tool version.')
        else:
            self.server.download_from_remote(
                '{}/{}'.format(self.serverToolFolderPath, self.ui.ToolVersion_comboBox.currentText()),
                os.path.join(self.nowToolFolderPath, self.ui.FolderName_lineEdit.text()))
    def updatefwButton_Clicked(self):
        if self.ui.FwVersion_comboBox.currentIndex() == 0:
            print('Please choose Fw version.')
        else:
            self.server.download_from_remote(
                '{}/{}'.format(self.serverFwFolderPath, self.ui.FwVersion_comboBox.currentText()),
                os.path.join(self.nowToolFolderPath, self.ui.FolderName_lineEdit.text()))


if __name__ == '__main__':
    utils.runAsAdmin([r'C:\Users\NVMTG-C08\Desktop\App_20210609\App_U0622A0.exe', ''], False)
    #import win32com.shell.shell as shell
    #import win32con
    #commands = r'C:\\Users\\NVMTG-C08\\Desktop\\App_20210609\\App_U0622A0.exe'
    #shell.ShellExecuteEx(lpVerb='runas', lpFile='cmd.exe', lpParameters='/c '+commands)
    #from win32api import ShellExecute
    #from win32com.shell.shell import ShellExecuteEx
    #ShellExecuteEx(lpVerb='runas',
    #             lpFile=commands,
    #             lpParameters='',
    #             nShow=win32con.SW_SHOWNORMAL)
    #win32api.ShellExecute(0, 'runas', commands, '', None, 1)
    #app = QtWidgets.QApplication([])
    #window = MainWindow()
    #window.show()
    #sys.exit(app.exec_())