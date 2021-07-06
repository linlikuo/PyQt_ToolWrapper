from windowclass import ToolItem

class ToolItemManager:
    def __init__(self):
        self._toolDict = dict()

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

class WindowManager:
    def __init__(self):
        self.windowlist = None
