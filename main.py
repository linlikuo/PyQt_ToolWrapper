from PyQt5 import QtWidgets, QtGui, QtCore
from ToolWrapper import Ui_MainWindow
import sys
import win32gui

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        '''
        consoleHwnd = win32gui.FindWindow('ConsoleWindowClass', r'C:\Users\NVMTG-C08\Desktop\App_20210609\App_U0622A0.exe')
        print(consoleHwnd)
        consoleWindow = QtGui.QWindow.fromWinId(consoleHwnd)
        consoleWidget = QtWidgets.QWidget.createWindowContainer(consoleWindow)

        toolHwnd = win32gui.FindWindow('WindowClass', None)
        print(toolHwnd)
        toolWindow = QtGui.QWindow.fromWinId(toolHwnd)
        toolWidget = QtWidgets.QWidget.createWindowContainer(toolWindow)

        folderHwnd = win32gui.FindWindow('CabinetWClass', 'App_20210609')
        print(folderHwnd)
        folderWindow = QtGui.QWindow.fromWinId(folderHwnd)
        folderWidget = QtWidgets.QWidget.createWindowContainer(folderWindow)

        toolWidget.setMinimumSize(toolWindow.size())
        toolWidget.setFixedSize(toolWidget.minimumSize())
        consoleWidget.setFixedHeight(toolWidget.height())
        consoleWidget.setFixedWidth(consoleWidget.width())

        hlayout = QtWidgets.QHBoxLayout()
        hlayout.addWidget(consoleWidget)
        hlayout.addWidget(toolWidget)
        upper = QtWidgets.QWidget()
        upper.setFixedSize(toolWidget.width()+consoleWidget.width(), toolWidget.height())
        upper.setLayout(hlayout)

        folderWidget.setFixedSize(upper.width(), 600);
        overall = QtWidgets.QWidget()
        vlayout = QtWidgets.QVBoxLayout()
        vlayout.addWidget(upper)
        vlayout.addWidget(folderWidget)
        overall.setLayout(vlayout)
        overall.setFixedSize(upper.width(), upper.height()+folderWidget.height())

        self.ui.scrollAreaWidgetContents.layout().addWidget(overall)
        '''

if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())