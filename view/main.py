
from PyQt5 import QtCore, QtGui, QtWidgets
import sys

class Button(QtWidgets.QPushButton):

    def __init__(self):
        super().__init__()

        self.setAcceptDrops(True)

    def dragEnterEvent(self, e):

        if e.mimeData().hasFormat('text/plain'):
            e.accept()
        else:
            e.ignore()

    def dropEvent(self, e):
        self.setText(e.mimeData().text())


class Ui_Form(QtWidgets.QWidget):
    def __init__(self):
        QtWidgets.QWidget.__init__(self, parent=None)
        self.resize(900, 600)
        self.treeView = QtWidgets.QTreeView()
        self.listView = QtWidgets.QListView()
        self.treeView.setProperty('showDropIndicator', True)
        self.treeView.setTabKeyNavigation(False)
        self.treeView.setDragEnabled(True)
        self.treeView.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.treeView.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.treeView.setUniformRowHeights(False)
        self.treeView.setAutoExpandDelay(0)
        self.treeView.setIndentation(20)
        self.treeView.setObjectName('treeView')
        self.treeView.header().setVisible(True)
        self.pushButton_1 = QtWidgets.QPushButton()
        self.pushButton_2 = QtWidgets.QPushButton()
        self.pushButton_3 = QtWidgets.QPushButton()
        self.pushButton_1.setText('Сделать Авто')
        self.pushButton_2.setText('>>')
        self.pushButton_3.setText('<<')
        self.vbox = QtWidgets.QGridLayout()
        self.vbox.setSpacing(10)
        self.vbox.setColumnStretch(1, 2)
        self.vbox.setColumnStretch(3, 2)
        self.vbox.addWidget(self.treeView, 1, 1, 4, 1)
        self.vbox.addWidget(self.listView, 1, 3, 4, 1)
        self.vbox.addWidget(self.pushButton_2, 1, 2, 2, 1)
        self.vbox.addWidget(self.pushButton_3,  2, 2, 2, 1)
        self.vbox.addWidget(self.pushButton_1, 4, 4)
        self.setLayout(self.vbox)
        self.setWindowTitle('Автообмен')


