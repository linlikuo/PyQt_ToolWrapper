from windowclass import ToolItem
from PyQt5 import QtCore

class ToolListTableManager:
    def __init__(self):
        self.header = ['Status', 'ToolName', 'UserName', 'FolderPath', 'Footnote']
        self.numItems = 0
        self.items = {}

    def __len__(self):
        return self.numItems

    def findColumnIndex(self, col):
        for idx, name in enumerate(self.header):
            if col == name:
                return idx
        return -1

    def removeItem(self, key):
        if key not in self.items:
            return False
        del self.items[key]
        self.numItems -= 1
        return True

    def addItem(self, item):
        iteminfo = item.split(',')
        name = ''
        for info in iteminfo:
            temp = info.split(':')
            if 'ToolName' in temp:
                name = temp[1]
                if (not name) or (name in self.items):
                    return False

        if not name:
            return False
        self.items[name] = iteminfo
        self.numItems += 1
        return True

class ToolItemManager(QtCore.QThread):
    def __init__(self, tablewidget, toollist):
        super(ToolItemManager, self).__init__()
        self._toolDict = dict()
        self.tableWidget = tablewidget
        self.toolList = toollist
        #self.checkOpenTimer = QtCore.QTimer()
        #self.checkOpenTimer.timeout.connect()

    def __len__(self):
        return len(self._toolDict)

    def addTool(self, toolname, item):
        if toolname not in self._toolDict:
            self._toolDict[toolname] = item
            return True
        return False

    def removeTool(self, toolname):
        if toolname not in self._toolDict:
            return False
        del self._toolDict[toolname]

    def getTool(self, toolname):
        if toolname not in self._toolDict:
            return None
        return self._toolDict[toolname]

    def run(self):
        while True:
            maxRow = self.tableWidget.rowCount()
            toolnameCol = self.toolList.findColumnIndex('ToolName')
            statusCol = self.toolList.findColumnIndex('Status')
            for row in range(maxRow):
                print('on Row {}\n'.format(row))
                status = self.tableWidget.item(row, statusCol).text()
                if status == 'Built':
                    toolname = self.tableWidget.item(row, toolnameCol).text()
                    if toolname in self._toolDict:
                        if not self._toolDict[toolname].is_alive():
                            if self._toolDict[toolname].status:
                                self.tableWidget.item(row, statusCol).setText('Opened')
                                print('Opened tool {} successfully.'.format(toolname))
                            else:
                                print('Failed to open tool.')
                                self.removeTool(toolname)





class WindowManager:
    def __init__(self):
        self.windowlist = None
