import win32gui
from PyQt5 import QtCore, QtGui, QtWidgets

class WindowHandle():
    def __init__(self, hwnd=None, window=None, widget=None, windowclass=None, windowname=None):
        self._hwnd = hwnd
        self._window = window
        self._widget = widget
        self._windowclass = windowclass
        self._windowname = windowname

    def __str__(self):
        attrs = vars(self)
        return ', '.join("%s: %s" % item for item in attrs.items())


    @property
    def hwnd(self):
        return self._hwnd

    @hwnd.setter
    def hwnd(self, new_hwnd):
        self._hwnd = new_hwnd

    @property
    def window(self):
        return self._window

    @window.setter
    def window(self, new_window):
        self._window = new_window

    @property
    def widget(self):
        return self._widget

    def widget(self, new_widget):
        self._widget = new_widget

    @property
    def windoclass(self):
        return self._windowclass

    @window.setter
    def windowclass(self, new_windowclass):
        self._windowclass = new_windowclass

    @property
    def windowname(self):
        return self._windowname
    @window.setter
    def windowname(self, new_windowname):
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

        self._hwnd = win32gui.FindWindow(wclass, wname)
        if not self._hwnd:
            return False

        self._window = QtGui.QWindow.fromWinId(self._hwnd)
        self._widget = QtWidgets.QWidget.createWindowContainer(self._window)
        return True


class ConsoleWindow(WindowHandle):
    def __init__(self, myhwnd=None, mywindow=None, mywidget=None, mywindowname=None):
        super(ConsoleWindow, self).__init__(hwnd=myhwnd, window=mywindow, widget=mywidget, windowclass='ConsoleWindowClass', windowname=mywindowname)


class ToolWindow(WindowHandle):
    def __init__(self, myhwnd=None, mywindow=None, mywidget=None, mywindowname=None):
        super(ToolWindow, self).__init__(hwnd=myhwnd, window=mywindow, widget=mywidget, windowclass='WindowClass', windowname=mywindowname)


class FolderWindow(WindowHandle):
    def __init__(self, myhwnd=None, mywindow=None, mywidget=None, mywindowname=None):
        super(FolderWindow, self).__init__(hwnd=myhwnd, window=mywindow, widget=mywidget, windowclass='CabinetWClass', windowname=mywindowname)

class ToolItem:
    def __init__(self):
        self.console = ConsoleWindow()
        self.tool = ToolWindow()
        self.folder = FolderWindow()

    def setUpAllWindow(self, consoleWindowClass=None, consoleWindowName=None, toolWindowClass=None, toolWindowName=None, folderWindowClass=None, folderWindowName=None):
        self.console.findWindow(consoleWindowClass, consoleWindowName)
        self.tool.findWindow(toolWindowClass, toolWindowName)
        self.folder.findWindow(folderWindowClass, folderWindowName)
        return True

    def __str__(self):
        temp = 'Item info as below:\n'
        for name, item in zip(['console', 'tool', 'folder'], [self.console, self.tool, self.folder]):
            temp += '[{}]:\n'.format(name)
            temp += item.__str__()
            temp += '\n'
        return temp



if __name__ == '__main__':
    pass