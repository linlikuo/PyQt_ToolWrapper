
class ToolListTableManager:
    def __init__(self):
        self.header = ['All', 'ToolName', 'UserName', 'FolderPath', 'Footnotes']
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