from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QFileSystemModel, QTreeView, QWidget, QVBoxLayout, QFileDialog, QMessageBox, QApplication
from PyQt5.QtGui import QIcon
from ui.MainWindow import Ui_MainWindow
import sys
import os
import yaml
import codecs

severity = ("High", "Medium", "Low", "Unknown")


def open_yaml(yaml_file):
    with codecs.open(yaml_file, "r", "utf8") as stream:
        yaml_contents = yaml.load(stream)
        if "documentation_complete" in yaml_contents and \
                yaml_contents["documentation_complete"] == "false":
            return None

        return yaml_contents


def user_home():
    if sys.version_info >= (3, 0):
        from pathlib import Path

        return str(Path.home())
    else:
        from os.path import expanduser

        return expanduser("~")


def load_yaml_to_gui(self, path):
    if path.endswith(".rule"):
        self.ui.tabWidget.addTab(addXCCDFTab(self.ui, path), os.path.basename(path))
        rule = open_yaml(path)
        self.ui.txtTitle.setText(rule['title'])
        self.ui.txtDesc.setPlainText(rule['description'])
        self.ui.severityComboBox.setCurrentText(rule['severity'].title())
        self.ui.txtOCILclause.setText(rule['ocil_clause'])
        self.ui.txtOCIL.setPlainText(rule['ocil'])
        self.ui.txtRationale.setPlainText(rule['rationale'])
 
        self.ui.txtDesc.textChanged.connect(self.onChange)
        self.ui.txtTitle.textChanged.connect(self.onChange)
        self.ui.severityComboBox.activated.connect(self.onChange)
        self.ui.txtOCIL.textChanged.connect(self.onChange)
        self.ui.txtOCIL.textChanged.connect(self.onChange)
        self.ui.txtRationale.textChanged.connect(self.onChange)

    if path.endswith(".group"):
        self.ui.tabWidget.addTab(addXCCDFTab(self.ui, path), os.path.basename(path))
        group = open_yaml(path)
        self.ui.txtTitle.setText(group['title'])
        self.ui.txtDesc.setPlainText(group['description'])

        self.ui.txtDesc.textChanged.connect(self.onChange)
        self.ui.txtTitle.textChanged.connect(self.onChange)


def setDirectory(self, directory):
    self.ui.treeView.setModel(self.proxyModel)
    self.ui.treeView.setRootIndex(self.model.index(directory))


def addXCCDFTab(self, path):
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.formLayoutWidget = QtWidgets.QWidget(self.tab)
        self.formLayoutWidget.setGeometry(QtCore.QRect(10, 10, 501, 541))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.scap = QtWidgets.QFormLayout(self.formLayoutWidget)
        self.scap.setContentsMargins(1, 1, 1, 1)
        self.scap.setObjectName("scap")
        self.lblscap = QtWidgets.QLabel(self.formLayoutWidget)
        self.lblscap.setObjectName("lblscap")
        self.scap.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.lblscap)
        self.txtTitle = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.txtTitle.setObjectName("txtTitle")
        self.scap.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.txtTitle)
        self.lbldesc = QtWidgets.QLabel(self.formLayoutWidget)
        self.lbldesc.setObjectName("lbldesc")
        self.scap.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.lbldesc)
        self.txtDesc = QtWidgets.QPlainTextEdit(self.formLayoutWidget)
        self.txtDesc.setObjectName("txtDesc")
        self.scap.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.txtDesc)
        self.severityLabel = QtWidgets.QLabel(self.formLayoutWidget)

        if path.endswith(".rule"):
            self.severityLabel.setObjectName("severityLabel")
            self.scap.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.severityLabel)
            self.severityComboBox = QtWidgets.QComboBox(self.formLayoutWidget)
            self.severityComboBox.setObjectName("severityComboBox")
            self.scap.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.severityComboBox)
            self.oCILClauseLabel = QtWidgets.QLabel(self.formLayoutWidget)
            self.oCILClauseLabel.setObjectName("oCILClauseLabel")
            self.scap.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.oCILClauseLabel)
            self.txtOCILclause = QtWidgets.QLineEdit(self.formLayoutWidget)
            self.txtOCILclause.setObjectName("txtOCILclause")
            self.scap.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.txtOCILclause)
            self.oCILLabel = QtWidgets.QLabel(self.formLayoutWidget)
            self.oCILLabel.setObjectName("oCILLabel")
            self.scap.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.oCILLabel)
            self.txtOCIL = QtWidgets.QPlainTextEdit(self.formLayoutWidget)
            self.txtOCIL.setObjectName("txtOCIL")
            self.scap.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.txtOCIL)
            self.oRationaleLabel = QtWidgets.QLabel(self.formLayoutWidget)
            self.oRationaleLabel.setFrameShape(QtWidgets.QFrame.NoFrame)
            self.oRationaleLabel.setObjectName("oRationaleLabel")
            self.scap.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.oRationaleLabel)
            self.txtRationale = QtWidgets.QPlainTextEdit(self.formLayoutWidget)
            self.txtRationale.setObjectName("txtRationale")
            self.scap.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.txtRationale)

            [self.severityComboBox.addItem(sevs) for sevs in severity]

        return self.tab


class ApplicationWindow(QtWidgets. QMainWindow):
    def __init__(self):
        super(ApplicationWindow, self).__init__()
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.retranslateUi(self) 

        self.ui.tabWidget.clear()

        self.model = QFileSystemModel()
        self.model.setRootPath(QtCore.QDir().rootPath())
        source = self.model.index(user_home())

        self.proxyModel = QtCore.QSortFilterProxyModel(self)
        self.proxyModel.setSourceModel(self.model)
        self.proxyModel.setDynamicSortFilter(True)
        index = self.proxyModel.mapFromSource(source)
        
        self.ui.treeView.setModel(self.proxyModel)
        self.ui.treeView.setRootIndex(index)

#        self.ui.treeView.setRootIndex(self.model.index(user_home()))
#        self.ui.treeView.setModel(self.proxyModel)
#        self.ui.treeView.setRootIndex(self.proxyModel)

        [self.ui.treeView.setColumnHidden(cols, True) for cols in range(1,4)]
        self.ui.treeView.doubleClicked.connect(self.onClick)
        self.ui.treeView.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.ui.treeView.customContextMenuRequested.connect(self.create_popup_menu)

        self.ui.filedirsearch.textChanged.connect(self.textFilter)
        self.ui.actionOpen.triggered.connect(self.openDirDialog)
        self.ui.actionAbout_Qt.triggered.connect(self.aboutQt)
        self.ui.actionQuit.triggered.connect(self.close)

        self.ui.tabWidget.tabCloseRequested.connect(self.removeTab)
        self.textFilter()


    def add_cb(self):
        print "add callback"


    def new_file(self):
        pass


    def onClick(self, index):
        path = self.sender().model().filePath(index)

        load_yaml_to_gui(self, path)


    def openDirDialog(self):
        dirname = QFileDialog()
        dirname.setFileMode(QFileDialog.Directory)
        dirname = QFileDialog.getExistingDirectory(self, "Open Folder", 
        options=QFileDialog.DontUseNativeDialog|QFileDialog.HideNameFilterDetails)

        if dirname != "":
            setDirectory(self, dirname)
        else:
            setDirectory(self, user_home())


    def saveFileDialog(self, ):
        quit_msg = "Save changes before closing?"
        reply = QtWidgets.QMessageBox.question(self, 'Message',
                quit_msg, QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.No)

#        if reply == QtGui.QMessageBox.Yes:
#            event.accept()
#        else:
#            event.ignore()


    def create_popup_menu(self, pos):
        self.popup_menu = QtWidgets.QMenu()
        self.popup_menu.addAction("New", self.add_cb)
        self.popup_menu.addAction("Rename", self.add_cb)
        self.popup_menu.addSeparator()
        self.popup_menu.addAction("Delete", self.add_cb)

        self.popup_menu.exec_(self.ui.treeView.viewport().mapToGlobal(pos))


    def on_context_menu(self, pos):
        node = self.treeWidget.mapToGlobal(pos)
        self.popup_menu.exec_(self.treeWidget.mapToGlobal(pos))


    def textFilter(self):
        regExp = QtCore.QRegExp(self.ui.filedirsearch.text(), QtCore.Qt.CaseInsensitive)
        self.proxyModel.setFilterRegExp(regExp)


    def removeTab(self, index):
        if self.ui.tabWidget.tabText(index).startswith("*"):
            self.saveFileDialog()
        self.ui.tabWidget.removeTab(index)


    def onChange(self):
        index = self.ui.tabWidget.currentIndex()
        filename = self.ui.tabWidget.tabText(index)
        if not filename.startswith("*"):
            filename = "*" + filename
        self.ui.tabWidget.setTabText(index, filename)


    def aboutQt(self):
        QMessageBox.aboutQt(self)


def main():
    app = QtWidgets.QApplication(sys.argv)
    application = ApplicationWindow()
    application.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
