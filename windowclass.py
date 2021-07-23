import win32con
import win32gui
from PyQt5 import QtCore, QtGui, QtWidgets
import time

class WindowHandle():
    def __init__(self, hwnd=None, window=None, widget=None, windowclass=None, windowname=None):
        self.hwnd = hwnd
        self.window = window
        self.widget = widget
        self.windowclass = windowclass
        self.windowname = windowname
        self.isDone = False

    def __str__(self):
        attrs = vars(self)
        return ', '.join("%s: %s" % item for item in attrs.items())


    def get_hwnd(self):
        return self.hwnd

    def set_hwnd(self, new_hwnd):
        self.hwnd = new_hwnd

    def get_window(self):
        return self.window

    def set_window(self, new_window):
        self.window = new_window

    def get_widget(self):
        return self.widget

    def set_widget(self, new_widget):
        self.widget = new_widget

    def get_windoclass(self):
        return self.windowclass

    def set_windowclass(self, new_windowclass):
        self.windowclass = new_windowclass

    def get_windowname(self):
        return self._windowname

    def set_windowname(self, new_windowname):
        self._windowname = new_windowname


    def findWindow(self, windowclass=None, windowname=None):
        wclass = windowclass
        wname = windowname
        if not wclass:
            wclass = self.windowclass
        else:
            self.windowclass = wclass
        if not wname:
            wname = self.windowname
        else:
            self.windowname = wname

        self.hwnd = win32gui.FindWindow(wclass, wname)
        if not self.hwnd:
            self.isDone = False
            return False

        self.window = QtGui.QWindow.fromWinId(self.hwnd)
        self.widget = QtWidgets.QWidget.createWindowContainer(self.window)

        self.widget.setFixedSize(self.window.size())
        self.isDone = True
        return True

    def stop(self):
        win32gui.SendMessage(self.hwnd, win32con.WM_CLOSE, 0, 0)
        self.hwnd = None
        self.window = None
        self.widget = None
        self.isDone = False


class ConsoleWindow(WindowHandle):
    def __init__(self, myhwnd=None, mywindow=None, mywidget=None, mywindowname=None):
        super(ConsoleWindow, self).__init__(hwnd=myhwnd, window=mywindow, widget=mywidget, windowclass='ConsoleWindowClass', windowname=mywindowname)


class ToolWindow(WindowHandle):
    def __init__(self, myhwnd=None, mywindow=None, mywidget=None, mywindowname=None):
        super(ToolWindow, self).__init__(hwnd=myhwnd, window=mywindow, widget=mywidget, windowclass='WindowClass', windowname=mywindowname)


class FolderWindow(WindowHandle):
    def __init__(self, myhwnd=None, mywindow=None, mywidget=None, mywindowname=None):
        super(FolderWindow, self).__init__(hwnd=myhwnd, window=mywindow, widget=mywidget, windowclass='CabinetWClass', windowname=mywindowname)

class ToolItem(QtCore.QThread):
    def __init__(self, consoleWindowName=None, toolWindowName=None, folderWindowName=None, parent=None, timeout=120):
        super(ToolItem, self).__init__(parent)
        self.toolname = toolWindowName
        self.console = ConsoleWindow(mywindowname=consoleWindowName)
        self.tool = ToolWindow(mywindowname=toolWindowName)
        self.folder = FolderWindow(folderWindowName)
        self.status = False
        self.parent = parent
        self.timeout_setup = timeout # 90(s)
        self._setupTimer = QtCore.QTimer(parent)
        self._setupTimer.timeout.connect(self.setup)
        self._timestamp = None

    def setUpAllWindow(self):
        if not self.folder.isDone:
            self.folder.findWindow(self.folder.windowclass, self.folder.windowname)
            return False
        if not self.tool.isDone:
            self.tool.findWindow(self.tool.windowclass, self.tool.windowname)
            return False
        if not self.console.isDone:
            self.console.findWindow(self.console.windowclass, self.console.windowname)
            return False

        self.console.widget.setFixedHeight(self.tool.window.height())
        self.console.widget.setFixedWidth(self.console.window.width()//2)
        self.status = True
        return True

    def startSetup(self):
        self._setupTimer.start(2000)

    def stopSetup(self):
        self._setupTimer.stop()

    def setup(self):
        if not self._timestamp:
            self._timestamp = time.time()
        if (time.time()-self._timestamp) > self.timeout_setup:
            print('Finding window timeout.')
            nowRow = -1
            for i in range(self.parent.ui.ToolList_tableWidget.rowCount()):
                if self.parent.ui.ToolList_tableWidget.item(i, self.parent.toollist.findColumnIndex(
                        'ToolName')).text() == self.toolname:
                    nowRow = i
                    break
            if self.status:
                print('Finishing finding window.')

                if nowRow != -1:
                    self.parent.ui.ToolList_tableWidget.item(nowRow,
                                                             self.parent.toollist.findColumnIndex('Status')).setText(
                        'Opened')
            else:
                print('Failed to find window.')
                if nowRow != -1:
                    self.parent.ui.ToolList_tableWidget.item(nowRow,
                                                             self.parent.toollist.findColumnIndex('Status')).setText(
                        'Failed to opened')
            self.stopSetup()
        else:
            self.setUpAllWindow()
            print('Finding window...')

            if self.status:
                nowRow = -1
                for i in range(self.parent.ui.ToolList_tableWidget.rowCount()):
                    if self.parent.ui.ToolList_tableWidget.item(i, self.parent.toollist.findColumnIndex(
                            'ToolName')).text() == self.toolname:
                        nowRow = i
                        break
                if self.status:
                    print('Finishing finding window.')

                    if nowRow != -1:
                        self.parent.ui.ToolList_tableWidget.item(nowRow,
                                                                 self.parent.toollist.findColumnIndex('Status')).setText(
                            'Opened')
                else:
                    print('Failed to find window.')
                    if nowRow != -1:
                        self.parent.ui.ToolList_tableWidget.item(nowRow,
                                                                 self.parent.toollist.findColumnIndex('Status')).setText(
                            'Failed to opened')
                self.stopSetup()

    def run(self):
        start = time.time()
        while (not self.setUpAllWindow()) and ((time.time()-start) <= self.timeout_setup):
            print('Finding window...')
            #time.sleep(2)

        nowRow = -1
        for i in range(self.parent.ui.ToolList_tableWidget.rowCount()):
            if self.parent.ui.ToolList_tableWidget.item(i, self.parent.toollist.findColumnIndex(
                    'ToolName')).text() == self.toolname:
                nowRow = i
                break
        if self.status:
            print('Finishing finding window.')

            if nowRow != -1:
                self.parent.ui.ToolList_tableWidget.item(nowRow, self.parent.toollist.findColumnIndex('Status')).setText('Opened')
        else:
            print('Failed to find window.')
            if nowRow != -1:
                self.parent.ui.ToolList_tableWidget.item(nowRow, self.parent.toollist.findColumnIndex('Status')).setText('Failed to opened')


    def __str__(self):
        temp = 'Item info as below:\n'
        for name, item in zip(['console', 'tool', 'folder'], [self.console, self.tool, self.folder]):
            temp += '[{}]:\n'.format(name)
            temp += item.__str__()
            temp += '\n'
        return temp

    def stop(self):
        self.tool.stop()
        self.folder.stop()
        self.status = False



if __name__ == '__main__':
    pass