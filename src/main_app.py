# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '../ui/main.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1070, 750)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QtCore.QSize(1070, 750))
        MainWindow.setMaximumSize(QtCore.QSize(16777215, 16777215))
        MainWindow.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout()
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setMinimumSize(QtCore.QSize(0, 50))
        self.label_4.setMaximumSize(QtCore.QSize(16777215, 50))
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_10.addWidget(self.label_4)
        self.verticalLayout.addLayout(self.horizontalLayout_10)
        self.verticalLayout_6.addLayout(self.verticalLayout)
        self.tableView = QtWidgets.QTableView(self.centralwidget)
        self.tableView.setObjectName("tableView")
        self.verticalLayout_6.addWidget(self.tableView)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSpacing(30)
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.DownloadButton = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.DownloadButton.sizePolicy().hasHeightForWidth())
        self.DownloadButton.setSizePolicy(sizePolicy)
        self.DownloadButton.setMinimumSize(QtCore.QSize(150, 35))
        self.DownloadButton.setObjectName("DownloadButton")
        self.horizontalLayout.addWidget(self.DownloadButton)
        self.AddButton = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.AddButton.sizePolicy().hasHeightForWidth())
        self.AddButton.setSizePolicy(sizePolicy)
        self.AddButton.setMinimumSize(QtCore.QSize(150, 35))
        self.AddButton.setObjectName("AddButton")
        self.horizontalLayout.addWidget(self.AddButton)
        self.DeleteButton = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.DeleteButton.sizePolicy().hasHeightForWidth())
        self.DeleteButton.setSizePolicy(sizePolicy)
        self.DeleteButton.setMinimumSize(QtCore.QSize(150, 35))
        self.DeleteButton.setObjectName("DeleteButton")
        self.horizontalLayout.addWidget(self.DeleteButton)
        self.SaveButton = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.SaveButton.sizePolicy().hasHeightForWidth())
        self.SaveButton.setSizePolicy(sizePolicy)
        self.SaveButton.setMinimumSize(QtCore.QSize(150, 35))
        self.SaveButton.setObjectName("SaveButton")
        self.horizontalLayout.addWidget(self.SaveButton)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.verticalLayout_6.addLayout(self.horizontalLayout)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        spacerItem2 = QtWidgets.QSpacerItem(20, 50, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout_2.addItem(spacerItem2)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setSpacing(30)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem3)
        self.propertylineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.propertylineEdit.setMinimumSize(QtCore.QSize(250, 35))
        self.propertylineEdit.setObjectName("propertylineEdit")
        self.horizontalLayout_4.addWidget(self.propertylineEdit)
        self.PointButton = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.PointButton.sizePolicy().hasHeightForWidth())
        self.PointButton.setSizePolicy(sizePolicy)
        self.PointButton.setMinimumSize(QtCore.QSize(250, 50))
        self.PointButton.setObjectName("PointButton")
        self.horizontalLayout_4.addWidget(self.PointButton)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem4)
        self.verticalLayout_2.addLayout(self.horizontalLayout_4)
        spacerItem5 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout_2.addItem(spacerItem5)
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setMinimumSize(QtCore.QSize(250, 21))
        font = QtGui.QFont()
        font.setFamily("Acquainted")
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.horizontalLayout_3.addWidget(self.label)
        self.verticalLayout_3.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.ValueMinEdit = QtWidgets.QTextEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ValueMinEdit.sizePolicy().hasHeightForWidth())
        self.ValueMinEdit.setSizePolicy(sizePolicy)
        self.ValueMinEdit.setMinimumSize(QtCore.QSize(250, 60))
        self.ValueMinEdit.setMaximumSize(QtCore.QSize(250, 60))
        self.ValueMinEdit.setObjectName("ValueMinEdit")
        self.horizontalLayout_2.addWidget(self.ValueMinEdit)
        self.verticalLayout_3.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_9.addLayout(self.verticalLayout_3)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setMinimumSize(QtCore.QSize(250, 21))
        font = QtGui.QFont()
        font.setFamily("Acquainted")
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_6.addWidget(self.label_2)
        self.verticalLayout_4.addLayout(self.horizontalLayout_6)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.ValueAvgEdit = QtWidgets.QTextEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ValueAvgEdit.sizePolicy().hasHeightForWidth())
        self.ValueAvgEdit.setSizePolicy(sizePolicy)
        self.ValueAvgEdit.setMinimumSize(QtCore.QSize(250, 60))
        self.ValueAvgEdit.setMaximumSize(QtCore.QSize(250, 60))
        self.ValueAvgEdit.setObjectName("ValueAvgEdit")
        self.horizontalLayout_5.addWidget(self.ValueAvgEdit)
        self.verticalLayout_4.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_9.addLayout(self.verticalLayout_4)
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        self.label_3.setMinimumSize(QtCore.QSize(250, 21))
        font = QtGui.QFont()
        font.setFamily("Acquainted")
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_7.addWidget(self.label_3)
        self.verticalLayout_5.addLayout(self.horizontalLayout_7)
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.ValueMaxEdit = QtWidgets.QTextEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ValueMaxEdit.sizePolicy().hasHeightForWidth())
        self.ValueMaxEdit.setSizePolicy(sizePolicy)
        self.ValueMaxEdit.setMinimumSize(QtCore.QSize(250, 60))
        self.ValueMaxEdit.setMaximumSize(QtCore.QSize(250, 60))
        self.ValueMaxEdit.setObjectName("ValueMaxEdit")
        self.horizontalLayout_8.addWidget(self.ValueMaxEdit)
        self.verticalLayout_5.addLayout(self.horizontalLayout_8)
        self.horizontalLayout_9.addLayout(self.verticalLayout_5)
        self.verticalLayout_2.addLayout(self.horizontalLayout_9)
        self.verticalLayout_6.addLayout(self.verticalLayout_2)
        self.verticalLayout_7.addLayout(self.verticalLayout_6)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Statistical compression of one-dimential arrays"))
        self.label_4.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:20pt;\">Исходные данные</span></p></body></html>"))
        self.DownloadButton.setText(_translate("MainWindow", "Загрузить данные"))
        self.AddButton.setText(_translate("MainWindow", "Добавить данные"))
        self.DeleteButton.setText(_translate("MainWindow", "Удалить данные"))
        self.SaveButton.setText(_translate("MainWindow", "Сохранить данные"))
        self.PointButton.setText(_translate("MainWindow", "Рассчитать трехточку"))
        self.label.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:14pt;\">Среднее минимальное</span></p></body></html>"))
        self.label_2.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:14pt;\">Среднее</span></p></body></html>"))
        self.label_3.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:14pt;\">Среднее максимальное</span></p></body></html>"))
