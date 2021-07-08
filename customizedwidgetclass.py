from PyQt5 import QtCore, QtWidgets

class ComboBox(QtWidgets.QComboBox):
    popupAboutToBeShown = QtCore.pyqtSignal()

    def showPopup(self) -> None:
        self.popupAboutToBeShown.emit()
        super(ComboBox, self).showPopup()