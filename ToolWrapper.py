# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ToolWrapper.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from customizedwidgetclass import ComboBox

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1231, 872)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.ToolList_tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.ToolList_tableWidget.setObjectName("ToolList_tableWidget")
        self.ToolList_tableWidget.setColumnCount(5)
        self.ToolList_tableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.ToolList_tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.ToolList_tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.ToolList_tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.ToolList_tableWidget.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.ToolList_tableWidget.setHorizontalHeaderItem(4, item)
        self.verticalLayout_3.addWidget(self.ToolList_tableWidget)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.Username_label = QtWidgets.QLabel(self.centralwidget)
        self.Username_label.setObjectName("Username_label")
        self.gridLayout.addWidget(self.Username_label, 0, 0, 1, 1)
        self.Username_lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.Username_lineEdit.setObjectName("Username_lineEdit")
        self.gridLayout.addWidget(self.Username_lineEdit, 0, 1, 1, 1)
        self.ToolName_label = QtWidgets.QLabel(self.centralwidget)
        self.ToolName_label.setObjectName("ToolName_label")
        self.gridLayout.addWidget(self.ToolName_label, 1, 0, 1, 1)
        self.ToolName_lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.ToolName_lineEdit.setObjectName("ToolName_lineEdit")
        self.gridLayout.addWidget(self.ToolName_lineEdit, 1, 1, 1, 1)
        self.FolderName_label = QtWidgets.QLabel(self.centralwidget)
        self.FolderName_label.setObjectName("FolderName_label")
        self.gridLayout.addWidget(self.FolderName_label, 2, 0, 1, 1)
        self.FolderName_lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.FolderName_lineEdit.setObjectName("FolderName_lineEdit")
        self.gridLayout.addWidget(self.FolderName_lineEdit, 2, 1, 1, 1)
        self.horizontalLayout.addLayout(self.gridLayout)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.Build_pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.Build_pushButton.setObjectName("Build_pushButton")
        self.verticalLayout.addWidget(self.Build_pushButton)
        self.Open_pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.Open_pushButton.setObjectName("Open_pushButton")
        self.verticalLayout.addWidget(self.Open_pushButton)
        self.Close_pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.Close_pushButton.setObjectName("Close_pushButton")
        self.verticalLayout.addWidget(self.Close_pushButton)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.verticalLayout_3.addLayout(self.horizontalLayout)
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.RefreshToolList_pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.RefreshToolList_pushButton.setObjectName("RefreshToolList_pushButton")
        self.gridLayout_2.addWidget(self.RefreshToolList_pushButton, 0, 0, 1, 1)
        self.RefreshFWList_pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.RefreshFWList_pushButton.setObjectName("RefreshFWList_pushButton")
        self.gridLayout_2.addWidget(self.RefreshFWList_pushButton, 0, 1, 1, 1)
        self.UpdateTool_pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.UpdateTool_pushButton.setObjectName("UpdateTool_pushButton")
        self.gridLayout_2.addWidget(self.UpdateTool_pushButton, 1, 0, 1, 1)
        self.UpdateFW_pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.UpdateFW_pushButton.setObjectName("UpdateFW_pushButton")
        self.gridLayout_2.addWidget(self.UpdateFW_pushButton, 1, 1, 1, 1)
        self.ToolVersion_comboBox = ComboBox(self.centralwidget)
        self.ToolVersion_comboBox.setObjectName("ToolVersion_comboBox")
        self.gridLayout_2.addWidget(self.ToolVersion_comboBox, 2, 0, 1, 1)
        self.FwVersion_comboBox = ComboBox(self.centralwidget)
        self.FwVersion_comboBox.setObjectName("FwVersion_comboBox")
        self.gridLayout_2.addWidget(self.FwVersion_comboBox, 2, 1, 1, 1)
        self.verticalLayout_3.addLayout(self.gridLayout_2)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.CustomizedToolPath_checkBox = QtWidgets.QCheckBox(self.centralwidget)
        self.CustomizedToolPath_checkBox.setObjectName("CustomizedToolPath_checkBox")
        self.verticalLayout_2.addWidget(self.CustomizedToolPath_checkBox)
        self.CustomizedToolPath_lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.CustomizedToolPath_lineEdit.setObjectName("CustomizedToolPath_lineEdit")
        self.verticalLayout_2.addWidget(self.CustomizedToolPath_lineEdit)
        self.verticalLayout_3.addLayout(self.verticalLayout_2)
        self.Message_textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.Message_textEdit.setReadOnly(True)
        self.Message_textEdit.setObjectName("Message_textEdit")
        self.verticalLayout_3.addWidget(self.Message_textEdit)
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.verticalLayout_3.addWidget(self.progressBar)
        self.verticalLayout_3.setStretch(0, 5)
        self.verticalLayout_3.setStretch(4, 1)
        self.verticalLayout_3.setStretch(5, 1)
        self.horizontalLayout_2.addLayout(self.verticalLayout_3)
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setTabsClosable(True)
        self.tabWidget.setMovable(True)
        self.tabWidget.setObjectName("tabWidget")
        self.horizontalLayout_2.addWidget(self.tabWidget)
        self.horizontalLayout_2.setStretch(0, 1)
        self.horizontalLayout_2.setStretch(1, 4)
        self.gridLayout_3.addLayout(self.horizontalLayout_2, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1231, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(-1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        item = self.ToolList_tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Status"))
        item = self.ToolList_tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "ToolName"))
        item = self.ToolList_tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "UserName"))
        item = self.ToolList_tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "FolderPath"))
        item = self.ToolList_tableWidget.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "Footnotes"))
        self.Username_label.setText(_translate("MainWindow", "Username"))
        self.ToolName_label.setText(_translate("MainWindow", "Tool Name"))
        self.FolderName_label.setText(_translate("MainWindow", "FolderName"))
        self.Build_pushButton.setText(_translate("MainWindow", "Build"))
        self.Open_pushButton.setText(_translate("MainWindow", "Open"))
        self.Close_pushButton.setText(_translate("MainWindow", "Close"))
        self.RefreshToolList_pushButton.setText(_translate("MainWindow", "RefreshToolList"))
        self.RefreshFWList_pushButton.setText(_translate("MainWindow", "RefreshFWList"))
        self.UpdateTool_pushButton.setText(_translate("MainWindow", "UpdateTool"))
        self.UpdateFW_pushButton.setText(_translate("MainWindow", "UpdateFW"))
        self.CustomizedToolPath_checkBox.setText(_translate("MainWindow", "User defined tool path (Below)"))
