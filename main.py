# -*- coding: cp1251 -*-
import pickle
import socket
import sys

from PyQt5 import QtCore, QtWidgets

from data.bd import MyQSqlDatabase
from view.main import Ui_MainWindow


class MainView(MyQSqlDatabase, QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        MyQSqlDatabase.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.on_clicked)
        self.ui.pushButton_2.clicked.connect(self.on_clicked_add)
        self.ui.pushButton_3.clicked.connect(self.on_clicked_del)

    def on_clicked_add(self):
        if self.ui.treeView.selectedIndexes():
            for i in range(0, self.ui.treeView.model().rowCount(self.ui.treeView.rootIndex())):
                root = self.ui.treeView.model().index(i, 0, QtCore.QModelIndex())
                if self.ui.treeView.model().index(i, 0, QtCore.QModelIndex()) in self.ui.treeView.selectedIndexes():
                    for j in range(0, self.ui.treeView.model().rowCount(root)):
                        text = self.ui.treeView.model().data(self.ui.treeView.model().index(j, 0, root))
                        item = QtWidgets.QListWidgetItem(text)
                        if self.ui.listWidget.findItems(text, QtCore.Qt.MatchContains):
                            print('эелемент уже есть в списке', text)  # Нужно сделать алерт!
                        else:
                            self.ui.listWidget.addItem(item)
                else:
                    for j in range(0, self.ui.treeView.model().rowCount(root)):
                        if self.ui.treeView.model().index(j, 0, root) in self.ui.treeView.selectedIndexes():
                            text = self.ui.treeView.model().data(self.ui.treeView.model().index(j, 0, root))
                            item = QtWidgets.QListWidgetItem(text)
                            if self.ui.listWidget.findItems(text, QtCore.Qt.MatchContains):
                                print('эелемент уже есть в списке', text)  # Нужно сделать алерт!
                            else:
                                self.ui.listWidget.addItem(item)

        else:
            for i in range(0, self.ui.treeView.model().rowCount(self.ui.treeView.rootIndex())):
                root = self.ui.treeView.model().index(i, 0, QtCore.QModelIndex())
                for j in range(0, self.ui.treeView.model().rowCount(root)):
                    text = self.ui.treeView.model().data(self.ui.treeView.model().index(j, 0, root))
                    item = QtWidgets.QListWidgetItem(text)
                    if self.ui.listWidget.findItems(text, QtCore.Qt.MatchContains):
                        print('эелемент уже есть в списке', text)  # Нужно сделать алерт!
                    else:
                        self.ui.listWidget.addItem(item)

    def on_clicked_del(self):
        listitems = self.ui.listWidget.selectedItems()
        if not listitems: self.ui.listWidget.clear()
        for item in listitems:
            self.ui.listWidget.takeItem(self.ui.listWidget.row(item))

    def on_clicked(self):
        ark = []
        for index in range(self.ui.listWidget.count()):
            ark.append(self.ui.listWidget.takeItem(0).text())
        self.send_data(ark)

    def send_data(self, message):
        try:
            self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.tcp_socket.connect(('10.88.2.54', 8888))
            message = pickle.dumps(message)
            self.tcp_socket.send(message)
            if self.tcp_socket.recv(1024):
                print('is str')
                self.tcp_socket.close()
        except ConnectionRefusedError:
            print('ошибка подключения')
            return



app = QtWidgets.QApplication(sys.argv)
application = MainView()
application.show()
sys.exit(app.exec())
