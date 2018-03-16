from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QFileSystemModel, QTreeView, QWidget, QVBoxLayout, QFileDialog, QMessageBox, QApplication
from PyQt5.QtGui import QIcon
from ui.MainWindow import Ui_MainWindow
import sys
import os
import yaml
from collections import OrderedDict
import codecs

severity = ("High", "Medium", "Low", "Unknown")
filters = ["*.rule", "*.group", "*.profile"]


class UnsortableList(list):
    def sort(self, *args, **kwargs):
        pass

class UnsortableOrderedDict(OrderedDict):
    def items(self, *args, **kwargs):
        return UnsortableList(OrderedDict.items(self, *args, **kwargs))


def open_yaml(yaml_file):
    with codecs.open(yaml_file, "r", "utf8") as stream:
        yaml_contents = yaml.load(stream)
        if "documentation_complete" in yaml_contents and \
                yaml_contents["documentation_complete"] == "false":
            return None

        return yaml_contents


def pyaml_dump(data):
    yaml.add_representer(UnsortableOrderedDict, yaml.representer.SafeRepresenter.represent_dict)

    return yaml.dump(data, indent=4, width=1000, default_flow_style=False, encoding="utf-8", line_break=True, tags=False)


def write_yaml(yaml_content, yaml_file):
    with codecs.open(yaml_file, "w", "utf8") as f:
        f.write(pyaml_dump(yaml_content))


class ApplicationWindow(QtWidgets. QMainWindow):
    def __init__(self):
        super(ApplicationWindow, self).__init__()
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self._translate = self.ui.retranslateUi(self)

        self.ui.tabWidget.clear()

        self.model = QFileSystemModel()
        self.model.setRootPath(QtCore.QDir().rootPath())
#        self.model.setFilter(QtCore.QDir().AllDirs|QtCore.QDir().NoDot)
        self.model.setNameFilters(filters)
        source = self.model.index(QtCore.QDir().homePath())


        self.proxyModel = QtCore.QSortFilterProxyModel(self)
        self.proxyModel.setSourceModel(self.model)
        self.proxyModel.setDynamicSortFilter(True)
        index = self.proxyModel.mapFromSource(source)
        
        self.ui.treeView.setModel(self.model)
        self.ui.treeView.setRootIndex(source)

#        self.ui.treeView.setModel(self.proxyModel)
#        self.ui.treeView.setRootIndex(index)

#        self.ui.treeView.setRootIndex(self.model.index(user_home()))
#        self.ui.treeView.setModel(self.proxyModel)
#        self.ui.treeView.setRootIndex(self.proxyModel)

        [self.ui.treeView.setColumnHidden(cols, True) for cols in range(1,4)]
        self.ui.treeView.doubleClicked.connect(self.onClick)
        self.ui.treeView.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.ui.treeView.customContextMenuRequested.connect(self.create_popup_menu)

        self.ui.filedirsearch.textChanged.connect(self.textFilter)
        self.ui.actionOpenProject.triggered.connect(self.openProjDialog)
        self.ui.actionOpenFile.triggered.connect(self.openFileDialog)
        self.ui.actionAbout_Qt.triggered.connect(self.aboutQt)
        self.ui.actionQuit.triggered.connect(self.close)
        self.ui.action_Save.triggered.connect(self.save)

        self.ui.tabWidget.tabCloseRequested.connect(self.removeTab)
        self.textFilter()


    def add_cb(self):
        print "add callback"


    def new_file(self):
        pass


    def load_yaml_to_gui(self, path):
        self.ui.tabWidget.addTab(self.addXCCDFTab(path), os.path.basename(path))
        data = open_yaml(path)

        self.ui.txtTitle.setText(data['title'])
        self.ui.txtDesc.setPlainText(data['description'])

        if path.endswith(".rule"):
            self.ui.severityComboBox.setCurrentText(data['severity'].title())
            self.ui.txtOCILclause.setText(data['ocil_clause'])
            self.ui.txtOCIL.setPlainText(data['ocil'])
            self.ui.txtRationale.setPlainText(data['rationale'])

            self.ui.severityComboBox.activated.connect(self.onChange)
            self.ui.txtOCIL.textChanged.connect(self.onChange)
            self.ui.txtOCILclause.textChanged.connect(self.onChange)
            self.ui.txtRationale.textChanged.connect(self.onChange)

#        if path.endswith(".profile"):
#            tv = self.ui.tableView
#            header = ['rule_selection']
#        tm = MyTableModel(self.tabledata, header, self)
#        tv.setModel(tm)
#
#        # hide grid
##            tv.setShowGrid(True)
#
#        # set the font
#        font = QFont("Courier New", 8)
#        tv.setFont(font)
#
#        # hide vertical header
#            vh = tv.verticalHeader()
#            vh.setVisible(False)
#
#        # set horizontal header properties
#            hh = tv.horizontalHeader()
#            hh.setStretchLastSection(True)
#
#        # set column width to fit contents
#            tv.resizeColumnsToContents()
#
#        # set row height
#        nrows = len(self.tabledata)
#        for row in xrange(nrows):
#            tv.setRowHeight(row, 18)
#
##        # enable sorting
#            tv.setSortingEnabled(True)
#
#        self.model = QtGui.QStandardItemModel(parent=self)
#        self.model.setHorizontalHeaderLabels(['Source', 'Destination', 'Protoco', 'Info'])
#        self.setModel(self.model)
#        self.setColumnWidth(0, 120)
#        self.setColumnWidth(1, 120)
#        self.setColumnWidth(2, 100)
#        self.setColumnWidth(3, 350)
#        self.setAlternatingRowColors(True)
#        self.setAutoScroll(True)
#        self.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
#        self.setEditTriggers(QtGui.QTableView.NoEditTriggers)
#        self.setSelectionMode(QtGui.QTableView.SingleSelection)
#            for selection in data["selections"]:
#                tv.setItem(selection)
#
#
#
        self.ui.txtDesc.textChanged.connect(self.onChange)
        self.ui.txtTitle.textChanged.connect(self.onChange)


    def addXCCDFTab(self, path):
        self.ui.tab = QtWidgets.QWidget()
        _translate = QtCore.QCoreApplication.translate
        self.ui.tab.setObjectName("tab")
        self.ui.formLayoutWidget = QtWidgets.QWidget(self.ui.tab)
        self.ui.formLayoutWidget.setGeometry(QtCore.QRect(10, 10, 501, 541))
        self.ui.formLayoutWidget.setObjectName("formLayoutWidget")
        self.ui.scap = QtWidgets.QFormLayout(self.ui.formLayoutWidget)
        self.ui.scap.setContentsMargins(1, 1, 1, 1)
        self.ui.scap.setObjectName("scap")
        self.ui.lblscap = QtWidgets.QLabel(self.ui.formLayoutWidget)
        self.ui.lblscap.setObjectName("lblscap")
        self.ui.scap.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.ui.lblscap)
        self.ui.txtTitle = QtWidgets.QLineEdit(self.ui.formLayoutWidget)
        self.ui.txtTitle.setObjectName("txtTitle")
        self.ui.scap.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.ui.txtTitle)
        self.ui.lbldesc = QtWidgets.QLabel(self.ui.formLayoutWidget)
        self.ui.lbldesc.setObjectName("lbldesc")
        self.ui.scap.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.ui.lbldesc)
        self.ui.txtDesc = QtWidgets.QPlainTextEdit(self.ui.formLayoutWidget)
        self.ui.txtDesc.setObjectName("txtDesc")
        self.ui.scap.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.ui.txtDesc)

        self.ui.lblscap.setText(_translate("MainWindow", "Title"))
        self.ui.lbldesc.setText(_translate("MainWindow", "Description"))

        if path.endswith(".rule"):
            self.ui.severityLabel = QtWidgets.QLabel(self.ui.formLayoutWidget)
            self.ui.severityLabel.setObjectName("severityLabel")
            self.ui.scap.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.ui.severityLabel)
            self.ui.severityComboBox = QtWidgets.QComboBox(self.ui.formLayoutWidget)
            self.ui.severityComboBox.setObjectName("severityComboBox")
            self.ui.scap.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.ui.severityComboBox)
            self.ui.oCILClauseLabel = QtWidgets.QLabel(self.ui.formLayoutWidget)
            self.ui.oCILClauseLabel.setObjectName("oCILClauseLabel")
            self.ui.scap.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.ui.oCILClauseLabel)
            self.ui.txtOCILclause = QtWidgets.QLineEdit(self.ui.formLayoutWidget)
            self.ui.txtOCILclause.setObjectName("txtOCILclause")
            self.ui.scap.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.ui.txtOCILclause)
            self.ui.oCILLabel = QtWidgets.QLabel(self.ui.formLayoutWidget)
            self.ui.oCILLabel.setObjectName("oCILLabel")
            self.ui.scap.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.ui.oCILLabel)
            self.ui.txtOCIL = QtWidgets.QPlainTextEdit(self.ui.formLayoutWidget)
            self.ui.txtOCIL.setObjectName("txtOCIL")
            self.ui.scap.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.ui.txtOCIL)
            self.ui.oRationaleLabel = QtWidgets.QLabel(self.ui.formLayoutWidget)
            self.ui.oRationaleLabel.setFrameShape(QtWidgets.QFrame.NoFrame)
            self.ui.oRationaleLabel.setObjectName("oRationaleLabel")
            self.ui.scap.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.ui.oRationaleLabel)
            self.ui.txtRationale = QtWidgets.QPlainTextEdit(self.ui.formLayoutWidget)
            self.ui.txtRationale.setObjectName("txtRationale")
            self.ui.scap.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.ui.txtRationale)

            self.ui.severityLabel.setText(_translate("MainWindow", "Severity"))
            self.ui.oCILClauseLabel.setText(_translate("MainWindow", "OCIL Clause"))
            self.ui.oCILLabel.setText(_translate("MainWindow", "OCIL"))
            self.ui.oRationaleLabel.setText(_translate("MainWindow", "Rationale"))

            [self.ui.severityComboBox.addItem(sevs) for sevs in severity]
        if path.endswith(".profile"):
            self.ui.selectionLabel = QtWidgets.QLabel(self.ui.formLayoutWidget)
            self.ui.selectionLabel.setObjectName("selectionLabel")
            self.ui.scap.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.ui.selectionLabel)

            self.ui.selectionLabel.setText(_translate("MainWindow", "Rule Selection"))

        return self.ui.tab

    def onClick(self, index):
        path = self.sender().model().filePath(index)
        if not self.sender().model().isDir(index):
            self.load_yaml_to_gui(path)
        else:
#            if path.endswith(".."):
#                path = path.rsplit("/", 2)[0]
#                print index
            self.ui.treeView.setRootIndex(index)


    def openProjDialog(self):
        dirname = QFileDialog()
        dirname.setFileMode(QFileDialog.Directory)
        dirname = QFileDialog.getExistingDirectory(self, "Open Project Folder",
        options=QFileDialog.DontUseNativeDialog|QFileDialog.HideNameFilterDetails|QFileDialog.ShowDirsOnly)

        if dirname != "":
            self.setDirectory(dirname)
        else:
            self.setDirectory(QtCore.QDir().homePath())


    def openFileDialog(self):
        fname = QFileDialog()
        fname.setFileMode(QFileDialog.Directory)
        fname = QFileDialog.getOpenFileNames(self, "Select File to Open", QtCore.QDir().homePath(),
                "All (*.rule *.group *.profile);;Rules ( *.rule);;Groups (*.group);;Profiles (*.profile)",
                options=QFileDialog.DontUseNativeDialog)
        path = "".join(fname[0])
        if path:
            self.load_yaml_to_gui(path)


    def saveFileDialog(self, path):
        quit_msg = "Save changes before closing?"
        reply = QtWidgets.QMessageBox.question(self, 'Message',
                quit_msg, QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.No)

        if reply == QtWidgets.QMessageBox.Yes:
            yaml_dict = UnsortableOrderedDict([
                ("documentation_complete", "true"),
                ])
            yaml_dict["title"] = self.ui.txtTitle.text()
            yaml_dict["description"] = self.ui.txtDesc.toPlainText()
            yaml_dict["severity"] = self.ui.severityComboBox.currentText().lower()
            yaml_dict["ocil_clause"] = self.ui.txtOCILclause.text()
            yaml_dict["ocil"] = self.ui.txtOCIL.toPlainText()
            yaml_dict["rationale"] = self.ui.txtRationale.toPlainText()

            write_yaml(yaml_dict, path.strip("*"))

    def save(self, index):

        yaml_dict = UnsortableOrderedDict([
                ("documentation_complete", "true"),
                ])
        yaml_dict["title"] = self.ui.txtTitle.text()
        yaml_dict["description"] = self.ui.txtDesc.toPlainText()
        yaml_dict["severity"] = self.ui.severityComboBox.currentText().lower()
        yaml_dict["ocil_clause"] = self.ui.txtOCILclause.text()
        yaml_dict["ocil"] = self.ui.txtOCIL.toPlainText()
        yaml_dict["rationale"] = self.ui.txtRationale.toPlainText()

        write_yaml(yaml_dict, self.ui.tabWidget.tabText(index).strip("*"))
        index = self.ui.tabWidget.currentIndex()
        filename = self.ui.tabWidget.tabText(index)
        self.ui.tabWidget.setTabText(index, filename.strip("*"))


    def setDirectory(self, directory):
        self.ui.treeView.setModel(self.model)
        self.ui.treeView.setRootIndex(self.model.index(directory))


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
            self.saveFileDialog(self.ui.tabWidget.tabText(index))
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
