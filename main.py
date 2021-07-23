import os

import win32api
from PyQt5 import QtWidgets, QtGui, QtCore
from ToolWrapper import Ui_MainWindow
from windowclass import ToolItem
from managerclass import ToolItemManager
from serverclass import Server
from managerclass import ToolListTableManager
import sys, paramiko, ssl
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
        self.timeout_FindingWindow = None
        self.toollist = ToolListTableManager()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.showMaximized()
        self.setWindowIcon(QtGui.QIcon(os.path.join(os.environ['HOMEPATH'], 'Desktop', 'ToolWrapper', 'Icon.png')))
        self.itemManager = ToolItemManager(self.ui.ToolList_tableWidget, self.toollist)
        # self.itemManager.start()
        self.LoadSettings()
        self.server = Server(hostname=self.serverIP, username=self.serverUsername, password=self.serverPassword, parent=self, progressBar=self.ui.progressBar)
        self.server.connect()
        self.server.startStatusTimer()
        self.server.startConnectTimer()
        self.server.start()
        self.currentRow = None
        self.ui.FwVersion_comboBox.popupAboutToBeShown.connect(self.update_FwVersion_comboBox)
        self.ui.ToolVersion_comboBox.popupAboutToBeShown.connect(self.update_ToolVersion_comboBox)
        self.ui.Build_pushButton.clicked.connect(self.buildButton_Clicked)
        self.ui.UpdateTool_pushButton.clicked.connect(self.updatetoolButton_Clicked)
        self.ui.UpdateFW_pushButton.clicked.connect(self.updatefwButton_Clicked)
        self.ui.Open_pushButton.clicked.connect(self.openButton_Clicked)
        self.ui.ToolList_tableWidget.cellDoubleClicked.connect(self.defaultShow)
        self.ui.ToolList_tableWidget.clicked.connect(self.toolListTable_Clicked)
        self.ui.tabWidget.tabCloseRequested.connect(self.onTabCloseRequested)
        self.ui.Close_pushButton.clicked.connect(self.closeButton_Clicked)
        self.ui.Open_pushButton.setEnabled(False)

    def LoadSettings(self, path=None, group='Init'):
        if not path:
            path = self.settingsPath

        self.settings = QtCore.QSettings(path, QtCore.QSettings.IniFormat)
        self.settings.beginGroup(group)
        self.defaultRootToolFolderPath = os.path.join(os.getcwd().split('\\')[0], os.environ['HOMEPATH'], 'Desktop', self.settings.value('DEFAULT_ROOT_TOOL_FOLDER_NAME'))
        self.nowToolFolderPath = self.defaultRootToolFolderPath
        self.serverIP = self.settings.value('SERVER_IP')
        self.serverUsername = self.settings.value('SERVER_USERNAME')
        self.serverPassword = self.settings.value('SERVER_PASSWORD')
        self.serverFwFolderPath = self.settings.value('SERVER_FW_FOLDER_PATH')
        self.serverToolFolderPath = self.settings.value('SERVER_TOOL_FOLDER_PATH')
        self.timeout_FindingWindow = int(self.settings.value('TIMEOUT_FIND_WINDOW'))
        self.settings.endGroup()
        return True

    def changeSettingPath(self, path):
        self.settingsPath = path

    def set_Progressbar_val(self, val):
        self.ui.progressBar.setValue(val)


    # Event function
    def buildButton_Clicked(self):

        if not self.ui.Username_lineEdit.text():
            print('Username can not be empty.')
        elif not self.ui.ToolName_lineEdit.text():
            print('Tool name can not be empty.')
        elif ((not self.ui.FolderName_lineEdit.text()) and (not self.ui.CustomizedToolPath_checkBox.isChecked())):
            print('Folder name can not be empty.')
        elif (not self.ui.CustomizedToolPath_checkBox.isChecked()) and ((self.ui.ToolVersion_comboBox.currentIndex() in [-1, 0]) or (self.ui.FwVersion_comboBox.currentIndex() in [-1, 0])):
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
                tableItem = QtWidgets.QTableWidgetItem('Building')
                self.ui.ToolList_tableWidget.setItem(nowRowIndex, self.toollist.findColumnIndex('Status'), tableItem)
                tableItem.setFlags(tableItem.flags() ^ QtCore.Qt.ItemFlag.ItemIsEditable)
                for cell in info.split(','):
                    index = cell.index(':')
                    value = cell[index+1:]
                    tableItem = QtWidgets.QTableWidgetItem(value)
                    tableItem.setFlags(tableItem.flags() ^ QtCore.Qt.ItemFlag.ItemIsEditable)
                    self.ui.ToolList_tableWidget.setItem(nowRowIndex, self.toollist.findColumnIndex(cell[:index]), tableItem)

                if not self.ui.CustomizedToolPath_checkBox.isChecked():
                    if not os.path.isdir(self.nowToolFolderPath):
                        os.mkdir(self.nowToolFolderPath)

                    if not os.path.isdir(os.path.join(self.nowToolFolderPath, self.ui.FolderName_lineEdit.text())):
                        os.mkdir(os.path.join(self.nowToolFolderPath, self.ui.FolderName_lineEdit.text()))

                    self.server.addWork('{}/{}'.format(self.serverFwFolderPath, self.ui.FwVersion_comboBox.currentText()), os.path.join(self.nowToolFolderPath, self.ui.FolderName_lineEdit.text()))
                    self.server.addWork('{}/{}'.format(self.serverToolFolderPath, self.ui.ToolVersion_comboBox.currentText()), os.path.join(self.nowToolFolderPath, self.ui.FolderName_lineEdit.text()))
                    self.server.download_progress_signal.connect(self.set_Progressbar_val)
                    self.server.startEvalute(True)
                    self.currentRow = nowRowIndex
                    self.ui.progressBar.valueChanged.connect(self.updateToolStatus)
                else:
                    self.ui.CustomizedToolPath_checkBox.setChecked(False)
                    self.ui.CustomizedToolPath_lineEdit.clear()
                    self.ui.ToolList_tableWidget.item(nowRowIndex, self.toollist.findColumnIndex('Status')).setText('Built')
                self.ui.ToolName_lineEdit.clear()
                self.ui.FolderName_lineEdit.clear()
            else:
                print('Can not add item, please make sure Tool name is unique.')

    @QtCore.pyqtSlot(int)
    def onTabCloseRequested(self, index):
        scroll = self.ui.tabWidget.widget(index)
        self.ui.tabWidget.removeTab(index)
        overall = scroll.takeWidget()
        loop = [overall]
        while True:
            if not loop:
                break
            temp = loop.pop(0)
            while True:
                if not temp.layout():
                    break
                for i in reversed(range(temp.layout().count())):
                    loop += [temp.layout().itemAt(i).widget()]
                    temp.layout().itemAt(i).widget().setParent(None)

        scroll.close()
        del scroll

    def updateToolStatus(self):
        if self.ui.progressBar.value() == 100:
            self.ui.ToolList_tableWidget.item(self.currentRow, self.toollist.findColumnIndex('Status')) .setText('Built')
            self.ui.progressBar.valueChanged.disconnect(self.updateToolStatus)

    def openButton_Clicked(self):
        #item = ToolItem()
        row = self.ui.ToolList_tableWidget.currentRow()
        if self.ui.ToolList_tableWidget.item(row, self.toollist.findColumnIndex('Status')).text() == 'Opened':
            print('Already opened, please doubled click to show tool.')
            return

        col = self.toollist.findColumnIndex('ToolName')
        toolname = self.ui.ToolList_tableWidget.item(row, col).text()
        folderpath = self.ui.ToolList_tableWidget.item(row, self.toollist.findColumnIndex('FolderPath')).text()
        folderwindowname = folderpath.split('\\')[-1]
        exe_file = utils.runTool(folderpath, toolname)

        item = ToolItem(consoleWindowName=exe_file, toolWindowName=toolname, folderWindowName=folderwindowname, parent=self, timeout=self.timeout_FindingWindow)

        if self.itemManager.addTool(toolname, item):
            item.startSetup()

    def closeButton_Clicked(self):
        row = self.ui.ToolList_tableWidget.currentRow()
        if self.ui.ToolList_tableWidget.item(row, self.toollist.findColumnIndex('Status')).text() != 'Opened':
            print('Not opened, please select tool and open it first.')
            return

        col = self.toollist.findColumnIndex('ToolName')
        toolname = self.ui.ToolList_tableWidget.item(row, col).text()
        item = self.itemManager.getTool(toolname)
        if not item:
            print('Tool lost, please re-open one.')
            return

        for idx in range(self.ui.tabWidget.count()):
            if self.ui.tabWidget.tabText(idx) == toolname:
                self.onTabCloseRequested(idx)
                if self.ui.tabWidget.count() > 0:
                    self.ui.tabWidget.setCurrentIndex(0)
                break
        item.stop()
        self.itemManager.removeTool(toolname)
        self.ui.ToolList_tableWidget.item(row, self.toollist.findColumnIndex('Status')).setText('Built')




    def defaultShow(self):

        row = self.ui.ToolList_tableWidget.currentRow()
        col = self.toollist.findColumnIndex('ToolName')
        toolname = self.ui.ToolList_tableWidget.item(row, col).text()

        for idx in range(self.ui.tabWidget.count()):
            if self.ui.tabWidget.tabText(idx) == toolname:
                self.ui.tabWidget.setCurrentIndex(idx)
                return

        item = self.itemManager.getTool(toolname)
        if not item or not item.status:
            print('Please open tool first.\n')
            return

        hlayout = QtWidgets.QHBoxLayout()
        hlayout.addWidget(item.console.widget)
        hlayout.addWidget(item.tool.widget)

        upper = QtWidgets.QWidget()
        upper.setFixedSize(item.tool.widget.width()+item.console.widget.width(), item.tool.widget.height())

        upper.setLayout(hlayout)

        item.folder.widget.setFixedSize(upper.width(), 600)
        overall = QtWidgets.QWidget()
        vlayout = QtWidgets.QVBoxLayout()
        vlayout.addWidget(upper)
        vlayout.addWidget(item.folder.widget)
        overall.setLayout(vlayout)
        overall.setFixedSize(upper.width(), upper.height()+item.folder.widget.height()+50)
        scroll = QtWidgets.QScrollArea()
        self.ui.tabWidget.addTab(scroll, toolname)
        scroll.setWidget(overall)
        scroll.setWidgetResizable(True)
        overall.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.ui.tabWidget.setCurrentIndex(self.ui.tabWidget.count()-1)
        overall.destroyed.connect(lambda obj : print('delete {}, count: {}'.format(obj, self.ui.tabWidget.count())))

    def toolListTable_Clicked(self):
        currentRow = self.ui.ToolList_tableWidget.currentRow()
        currentStatus = self.ui.ToolList_tableWidget.item(currentRow, self.toollist.findColumnIndex('Status')).text()
        if currentStatus == 'Built':
            self.ui.Open_pushButton.setEnabled(True)
        else:
            self.ui.Open_pushButton.setEnabled(False)


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
        if self.ui.ToolVersion_comboBox.currentIndex() in [-1, 0]:
            print('Please choose Tool version.')
        else:
            row = self.ui.ToolList_tableWidget.currentRow()
            if row == -1:
                print('Please choose a tool item.')
                return
            col = self.toollist.findColumnIndex('FolderPath')
            foldername = self.ui.ToolList_tableWidget.item(row, col).text()
            self.set_Progressbar_val(0)
            self.server.addWork('{}/{}'.format(self.serverToolFolderPath, self.ui.ToolVersion_comboBox.currentText()), foldername)
            self.server.download_progress_signal.connect(self.set_Progressbar_val)
            self.server.startEvalute(True)
    def updatefwButton_Clicked(self):
        if self.ui.FwVersion_comboBox.currentIndex() in [-1, 0]:
            print('Please choose Fw version.')
        else:
            row = self.ui.ToolList_tableWidget.currentRow()
            if row == -1:
                print('Please choose a tool item.')
                return
            col = self.toollist.findColumnIndex('FolderPath')
            foldername = self.ui.ToolList_tableWidget.item(row, col).text()
            self.set_Progressbar_val(0)
            self.server.addWork('{}/{}'.format(self.serverFwFolderPath, self.ui.FwVersion_comboBox.currentText()), foldername)
            self.server.download_progress_signal.connect(self.set_Progressbar_val)
            self.server.startEvalute(True)


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.setWindowTitle('ToolWrapper')
    window.show()
    sys.exit(app.exec_())