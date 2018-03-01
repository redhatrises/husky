# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/MainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.formLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.formLayoutWidget.setGeometry(QtCore.QRect(59, 119, 711, 401))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.scapprofile = QtWidgets.QFormLayout(self.formLayoutWidget)
        self.scapprofile.setContentsMargins(0, 0, 0, 0)
        self.scapprofile.setObjectName("scapprofile")
        self.lblscapprofile = QtWidgets.QLabel(self.formLayoutWidget)
        self.lblscapprofile.setObjectName("lblscapprofile")
        self.scapprofile.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.lblscapprofile)
        self.txtProfileTitle = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.txtProfileTitle.setObjectName("txtProfileTitle")
        self.scapprofile.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.txtProfileTitle)
        self.lblprofiledesc = QtWidgets.QLabel(self.formLayoutWidget)
        self.lblprofiledesc.setObjectName("lblprofiledesc")
        self.scapprofile.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.lblprofiledesc)
        self.txtProfileDesc = QtWidgets.QPlainTextEdit(self.formLayoutWidget)
        self.txtProfileDesc.setObjectName("txtProfileDesc")
        self.scapprofile.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.txtProfileDesc)
        self.treeView = QtWidgets.QTreeView(self.centralwidget)
        self.treeView.setGeometry(QtCore.QRect(0, 0, 256, 192))
        self.treeView.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.treeView.setObjectName("treeView")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 20))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuNew = QtWidgets.QMenu(self.menuFile)
        self.menuNew.setObjectName("menuNew")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionSCAP_Profile = QtWidgets.QAction(MainWindow)
        self.actionSCAP_Profile.setObjectName("actionSCAP_Profile")
        self.menuNew.addAction(self.actionSCAP_Profile)
        self.menuFile.addAction(self.menuNew.menuAction())
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "SCAP Writer"))
        self.lblscapprofile.setText(_translate("MainWindow", "Title"))
        self.lblprofiledesc.setText(_translate("MainWindow", "Profile Description"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuNew.setTitle(_translate("MainWindow", "New"))
        self.actionSCAP_Profile.setText(_translate("MainWindow", "SCAP Profile"))

