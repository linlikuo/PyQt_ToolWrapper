from PyQt5 import QtWidgets, QtGui, QtCore
from ToolWrapper import Ui_MainWindow
from windowclass import ToolItem
from managerclass import ToolItemManager
import sys
import win32gui

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.settingsPath = 'settings.ini'
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.LoadSettings(self.settingsPath)

        #item = ToolItem()
        #print(item)
        #if item.setUpAllWindow(consoleWindowName=r'C:\Users\NVMTG-C08\Desktop\App_20210609\App_U0622A0.exe', toolWindowName='NVMTG APP U0621', folderWindowName='App_20210609'):
        #    print('Find window successfully')
        #    print(item)

    def changeSettingPath(self, path):
        self.settingsPath = path


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())