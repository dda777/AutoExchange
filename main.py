# -*- coding: cp1251 -*-
import sys
import socket
import uuid


from PyQt5 import QtCore, QtWidgets, Qt

from data.bd import MyQSqlDatabase
from view.main import Ui_MainWindow


class MainView(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.on_clicked)
        self.ui.pushButton_2.clicked.connect(self.on_clicked_add)
        self.ui.pushButton_3.clicked.connect(self.on_clicked_del)
        self.info_connect = MyQSqlDatabase('info_connect')
        self.ui.tableView.setModel(self.info_connect.select_data_model())
        self.timer = QtCore.QTimer()
        self.timer.start(5000)
        self.timer.timeout.connect(self.set_model)
        # self.thread = DbThread()
        # self.thread.start()

    def set_model(self):
        self.info_connect_update = MyQSqlDatabase('info_connect_update')
        model = self.info_connect_update.select_data_model()
        self.ui.tableView.setModel(model)


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
        HOST, PORT = "localhost", 8887
        hash_key = uuid.uuid4().hex
        names = []
        for index in range(self.ui.listWidget.count()):
            names.append(self.ui.listWidget.takeItem(0).text())
        if not names:
            print('ошибка')
            return
        db = MyQSqlDatabase('Conn1')
        db.insert_operations(names, hash_key)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            # Connect to server and send data
            sock.connect((HOST, PORT))
            sock.sendall(bytes(hash_key, "utf-8"))



class DbThread(Qt.QThread):
    def __init__(self):
        super().__init__()
        self.info_connect_update = MyQSqlDatabase('info_connect_update')

    def run(self, *args, **kwargs):
        while True:
            Qt.QThread.msleep(2000)
            model = self.info_connect_update.select_data_model()



app = QtWidgets.QApplication(sys.argv)
application = MainView()
application.show()
sys.exit(app.exec())
