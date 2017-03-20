# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qtdesigner.ui'
#
# Created by: PyQt5 UI code generator 5.7
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MplMainWindow(object):
    def setupUi(self, MplMainWindow):
        MplMainWindow.setObjectName("MplMainWindow")
        MplMainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MplMainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.mpllineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.mpllineEdit.setObjectName("mpllineEdit")
        self.horizontalLayout.addWidget(self.mpllineEdit)
        self.mplpushButton = QtWidgets.QPushButton(self.centralwidget)
        self.mplpushButton.setObjectName("mplpushButton")
        self.horizontalLayout.addWidget(self.mplpushButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.mpl = MplWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.mpl.sizePolicy().hasHeightForWidth())
        self.mpl.setSizePolicy(sizePolicy)
        self.mpl.setObjectName("mpl")
        self.verticalLayout.addWidget(self.mpl)
        MplMainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MplMainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 28))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        MplMainWindow.setMenuBar(self.menubar)
        self.mplactionOpen = QtWidgets.QAction(MplMainWindow)
        self.mplactionOpen.setObjectName("mplactionOpen")
        self.mplactionQuit = QtWidgets.QAction(MplMainWindow)
        self.mplactionQuit.setObjectName("mplactionQuit")
        self.menuFile.addAction(self.mplactionOpen)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.mplactionQuit)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MplMainWindow)
        QtCore.QMetaObject.connectSlotsByName(MplMainWindow)

    def retranslateUi(self, MplMainWindow):
        _translate = QtCore.QCoreApplication.translate
        MplMainWindow.setWindowTitle(_translate("MplMainWindow", "MainWindow"))
        self.mplpushButton.setText(_translate("MplMainWindow", "PushButton"))
        self.menuFile.setTitle(_translate("MplMainWindow", "File"))
        self.mplactionOpen.setText(_translate("MplMainWindow", "Open"))
        self.mplactionQuit.setText(_translate("MplMainWindow", "Quit"))

from mplwidget import MplWidget
