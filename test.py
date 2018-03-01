#!/usr/bin/env python

from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QFileSystemModel, QTreeView, QWidget, QVBoxLayout, QFileDialog
from PyQt5.QtGui import QIcon
from MainWindow import Ui_MainWindow
import sys
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
        rule = open_yaml(path)
        print rule
        self.ui.txtProfileTitle.setText(rule['title'])
        self.ui.txtProfileDesc.setPlainText(rule['description'])
        self.ui.severityComboBox.setCurrentText(rule['severity'].title())
        self.ui.txtOCILclause.setText(rule['ocil_clause'])
        self.ui.txtOCIL.setPlainText(rule['ocil'])
        self.ui.txtRationale.setPlainText(rule['rationale'])


class ApplicationWindow(QtWidgets. QMainWindow):
    def __init__(self):
        super(ApplicationWindow, self).__init__()
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.model = QFileSystemModel()
        self.model.setRootPath("")
        self.ui.treeView.setModel(self.model)
        self.ui.treeView.setRootIndex(self.model.index(user_home()))
        self.ui.treeView.setColumnHidden(1, True)
        self.ui.treeView.setColumnHidden(2, True)
        self.ui.treeView.setColumnHidden(3, True)
        self.ui.actionQuit.triggered.connect(self.close)
        self.ui.treeView.clicked.connect(self.onClick)
        [self.ui.severityComboBox.addItem(sevs) for sevs in severity]
        self.ui.actionOpen.triggered.connect(self.openDirDialog)

    def onClick(self, index):
        path = self.sender().model().filePath(index)

        load_yaml_to_gui(self, path)


    def openDirDialog(self):
        dirname = QFileDialog()
        dirname.setFileMode(QFileDialog.Directory)
        dirname = QFileDialog.getExistingDirectory(self, "Open Folder", 
        options=QFileDialog.DontUseNativeDialog|QFileDialog.HideNameFilterDetails)
        self.ui.treeView.setModel(self.model)

        if dirname != "":
            self.ui.treeView.setRootIndex(self.model.index(dirname))
        else:
            self.ui.treeView.setRootIndex(self.model.index(user_home()))


def main():
    app = QtWidgets.QApplication(sys.argv)
    application = ApplicationWindow()
    application.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
