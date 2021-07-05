import win32gui
from PyQt5 import QtCore, QtGui, QtWidgets

class WindowHandle():
    def __init__(self, hwnd=None, window=None, widget=None):
        self._hwnd = hwnd
        self._window = window
        self._widget = widget

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

    def findWindow(self, windowclass, windowname):
        self._hwnd = win32gui.FindWindow(windowclass, windowname)
        if not self._hwnd:
            return False
        self._window = QtGui.QWindow.fromWinId(self._hwnd)
        self._widget = QtWidgets.QWidget.createWindowContainer(self._window)
        return True


class ConsoleWindow(WindowHandle):
    def __init__(self):
        super(ConsoleWindow, self).__init__()

    def findWindow(self, windowname):
        return super(ConsoleWindow, self).findWindow('ConsoleWindowClass', windowname)

class ToolWindow(WindowHandle):
    def __init__(self):
        super(ToolWindow, self).__init__()

    def findWindow(self, windowname):
        return super(ToolWindow, self).findWindow('WindowClass', windowname)

class FolderWindow(WindowHandle):
    def __init__(self):
        super(FolderWindow, self).__init__()

    def findWindow(self, windowname):
        return super(FolderWindow, self).findWindow('CabinetWclass', windowname)

