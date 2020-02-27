# -*- coding: cp1251 -*-
from data.bd import MyQSqlDatabase
from PyQt5 import QtCore, QtWidgets
from view.main import Ui_MainWindow
import sys
import getpass, socket


class MainView(MyQSqlDatabase, QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        MyQSqlDatabase.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.on_clicked)
        #self.ui.pushButton.clicked.connect(self.insert_data_to_database)
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

    def insert_data_to_database(self):

        shared_mode = 1
        username = getpass.getuser()
        ip = '127.0.0.1'
        status = 0

        for index in range(self.ui.listWidget.count()):
            object_id = self.get_data_for_auto(self.ui.listWidget.item(index).text())[0]
            if self.check_dublicate(object_id):
                print('найден дубликат', self.ui.listWidget.item(index).text())
            else:
                self.insert_data(shared_mode, username, ip, status, object_id)
        self.ui.listWidget.clear()

    def on_clicked(self):
        ip = socket.gethostbyname_ex(socket.gethostname())[2]
        print(ip)
        # ark = []
        # for index in range(self.ui.listWidget.count()):
        #     ark.append(self.ui.listWidget.takeItem(0).text())
        # self.send_data(ark)


app = QtWidgets.QApplication(sys.argv)
application = MainView()
application.show()
sys.exit(app.exec())
