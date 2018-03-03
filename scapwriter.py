from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QFileSystemModel, QTreeView, QWidget, QVBoxLayout, QFileDialog, QMessageBox, QApplication
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
#        print rule
        self.ui.txtProfileTitle.setText(rule['title'])
        self.ui.txtProfileDesc.setPlainText(rule['description'])
        self.ui.severityComboBox.setCurrentText(rule['severity'].title())
        self.ui.txtOCILclause.setText(rule['ocil_clause'])
        self.ui.txtOCIL.setPlainText(rule['ocil'])
        self.ui.txtRationale.setPlainText(rule['rationale'])


def setDirectory(self, directory):
    self.ui.treeView.setModel(self.proxyModel)
    self.ui.treeView.setRootIndex(self.model.index(directory))


class ApplicationWindow(QtWidgets. QMainWindow):
    def __init__(self):
        super(ApplicationWindow, self).__init__()
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.model = QFileSystemModel()
        self.proxyModel = QtCore.QSortFilterProxyModel(self.ui.treeView)

        self.model.setRootPath("")
        self.ui.treeView.setModel(self.model)
        self.ui.treeView.setRootIndex(self.model.index(user_home()))
        self.proxyModel.setSourceModel(self.model)
        self.proxyModel.setDynamicSortFilter(True)
        #self.ui.treeView.setModel(self.proxyModel)
        self.ui.treeView.setRootIndex(self.model.index(user_home()))
        self.ui.treeView.setModel(self.model)

        self.ui.treeView.setColumnHidden(1, True)
        self.ui.treeView.setColumnHidden(2, True)
        self.ui.treeView.setColumnHidden(3, True)
        self.ui.actionQuit.triggered.connect(self.close)
        self.ui.treeView.clicked.connect(self.onClick)
        self.ui.filedirsearch.textChanged.connect(self.textFilter)
        [self.ui.severityComboBox.addItem(sevs) for sevs in severity]
        self.ui.actionOpen.triggered.connect(self.openDirDialog)
        self.ui.actionAbout_Qt.triggered.connect(self.aboutQt)
        self.textFilter()

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


    def textFilter(self):
        regExp = QtCore.QRegExp(self.ui.filedirsearch.text(), QtCore.Qt.CaseInsensitive)
        self.proxyModel.setFilterRegExp(regExp)

    def aboutQt(self):
        QMessageBox.aboutQt(self)

def main():
    app = QtWidgets.QApplication(sys.argv)
    application = ApplicationWindow()
    application.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
