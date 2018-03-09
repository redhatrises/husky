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
        self.ui.tabWidget.addTab(self.ui.tabRule, os.path.basename(path))
#        self.ui.tabWidget.setTabText(self.ui.tabWidget.indexOf(self.ui.tab), "Tab 1")
#        self.ui.tabWidget.addTab(self.ui.tab, ".rule2")
#        self.tab_2 = QtWidgets.QWidget()
#       self.tab_2.setObjectName("tab_2")
#        self.ui.tabWidget.addTab(self.tab_2, "")
        rule = open_yaml(path)
#        print rule
        self.ui.txtRuleTitle.setText(rule['title'])
        self.ui.txtRuleDesc.setPlainText(rule['description'])
        self.ui.severityComboBox.setCurrentText(rule['severity'].title())
        self.ui.txtOCILclause.setText(rule['ocil_clause'])
        self.ui.txtOCIL.setPlainText(rule['ocil'])
        self.ui.txtRationale.setPlainText(rule['rationale'])
 
        self.ui.txtRuleDesc.textChanged.connect(self.onChange)
        self.ui.txtRuleTitle.textChanged.connect(self.onChange)
        self.ui.severityComboBox.activated.connect(self.onChange)
        self.ui.txtOCIL.textChanged.connect(self.onChange)
        self.ui.txtOCIL.textChanged.connect(self.onChange)
        self.ui.txtRationale.textChanged.connect(self.onChange)

    if path.endswith(".group"):
        self.ui.tabWidget.addTab(self.ui.tabGroup, os.path.basename(path))
        group = open_yaml(path)
        self.ui.txtGroupTitle.setText(group['title'])
        self.ui.txtGroupDesc.setPlainText(group['description'])
#        self.ui.txtGroupDesc.textChanged.connect(self.onChange)
#        self.ui.txtGroupTitle.textChanged.connect(self.onChange)


def setDirectory(self, directory):
    self.ui.treeView.setModel(self.proxyModel)
    self.ui.treeView.setRootIndex(self.model.index(directory))


class ApplicationWindow(QtWidgets. QMainWindow):
    def __init__(self):
        super(ApplicationWindow, self).__init__()
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.retranslateUi(self) 

        self.ui.tabWidget.clear()
        [self.ui.severityComboBox.addItem(sevs) for sevs in severity]


        self.model = QFileSystemModel()
        self.model.setRootPath(QtCore.QDir().rootPath())
        self.model.setReadOnly(False)
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
        self.ui.treeView.clicked.connect(self.onClick)
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

        self.ui.txtGroupDesc.textChanged.connect(self.onChange)
        self.ui.txtGroupTitle.textChanged.connect(self.onChange)


    def openDirDialog(self):
        dirname = QFileDialog()
        dirname.setFileMode(QFileDialog.Directory)
        dirname = QFileDialog.getExistingDirectory(self, "Open Folder", 
        options=QFileDialog.DontUseNativeDialog|QFileDialog.HideNameFilterDetails)

        if dirname != "":
            setDirectory(self, dirname)
        else:
            setDirectory(self, user_home())


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
        self.ui.tabWidget.removeTab(index)


    def onChange(self):
        print "text changed"


    def aboutQt(self):
        QMessageBox.aboutQt(self)


def main():
    app = QtWidgets.QApplication(sys.argv)
    application = ApplicationWindow()
    application.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()