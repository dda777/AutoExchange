# -*- coding: cp1251 -*-
from data.bd import MyQSqlDatabase
from PyQt5 import QtCore, QtWidgets, QtGui, QtSql
import socket
import pickle
import asyncio
from socket import *
import sys
import getpass


class MainView(QtWidgets.QWidget, MyQSqlDatabase):
    def __init__(self):
        QtWidgets.QWidget.__init__(self, parent=None)
        MyQSqlDatabase.__init__(self)
        self.resize(900, 600)

        self.listView = MyListWidget()

        self.treeView = QtWidgets.QTreeView()
        self.treeView.setDragEnabled(True)
        self.treeView.setUniformRowHeights(False)
        self.treeView.setAutoExpandDelay(0)
        self.treeView.setIndentation(20)
        self.treeView.header().setVisible(False)
        self.treeView.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)

        self.pushButton_1 = QtWidgets.QPushButton()
        self.pushButton_1.setText('Сделать Авто')
        # self.pushButton_1.clicked.connect(self.on_clicked)
        self.pushButton_1.clicked.connect(self.insert_data_to_database)

        self.pushButton_2 = QtWidgets.QPushButton()
        self.pushButton_2.setText('>>')
        self.pushButton_2.clicked.connect(self.on_clicked_add)

        self.pushButton_3 = QtWidgets.QPushButton()
        self.pushButton_3.setText('<<')
        self.pushButton_3.clicked.connect(self.on_clicked_del)

        self.vbox = QtWidgets.QGridLayout()
        self.vbox.setSpacing(10)
        self.vbox.setColumnStretch(1, 2)
        self.vbox.setColumnStretch(3, 2)
        self.vbox.addWidget(self.treeView, 1, 1, 4, 1)
        self.vbox.addWidget(self.listView, 1, 3, 4, 1)
        self.vbox.addWidget(self.pushButton_2, 1, 2, 2, 1)
        self.vbox.addWidget(self.pushButton_3, 2, 2, 2, 1)
        self.vbox.addWidget(self.pushButton_1, 4, 4)
        self.setLayout(self.vbox)
        self.setWindowTitle('Автообмен')
        self.model = TreeModel()
        self.treeView.setModel(self.model.add_data())

    def on_clicked_add(self):
        if self.treeView.selectedIndexes():
            for i in range(0, self.treeView.model().rowCount(self.treeView.rootIndex())):
                root = self.treeView.model().index(i, 0, QtCore.QModelIndex())
                if self.treeView.model().index(i, 0, QtCore.QModelIndex()) in self.treeView.selectedIndexes():
                    for j in range(0, self.treeView.model().rowCount(root)):
                        text = self.treeView.model().data(self.treeView.model().index(j, 0, root))
                        item = QtWidgets.QListWidgetItem(text)
                        if self.listView.findItems(text, QtCore.Qt.MatchContains):
                            print('эелемент уже есть в списке', text)  # Нужно сделать алерт!
                        else:
                            self.listView.addItem(item)
                else:
                    for j in range(0, self.treeView.model().rowCount(root)):
                        if self.treeView.model().index(j, 0, root) in self.treeView.selectedIndexes():
                            text = self.treeView.model().data(self.treeView.model().index(j, 0, root))
                            item = QtWidgets.QListWidgetItem(text)
                            if self.listView.findItems(text, QtCore.Qt.MatchContains):
                                print('эелемент уже есть в списке', text)  # Нужно сделать алерт!
                            else:
                                self.listView.addItem(item)

        else:
            for i in range(0, self.treeView.model().rowCount(self.treeView.rootIndex())):
                root = self.treeView.model().index(i, 0, QtCore.QModelIndex())
                for j in range(0, self.treeView.model().rowCount(root)):
                    text = self.treeView.model().data(self.treeView.model().index(j, 0, root))
                    item = QtWidgets.QListWidgetItem(text)
                    if self.listView.findItems(text, QtCore.Qt.MatchContains):
                        print('эелемент уже есть в списке', text)  # Нужно сделать алерт!
                    else:
                        self.listView.addItem(item)

    def on_clicked_del(self):
        listitems = self.listView.selectedItems()
        if not listitems: self.listView.clear()
        for item in listitems:
            self.listView.takeItem(self.listView.row(item))

    def insert_data_to_database(self):
        # ip = socket.gethostbyname_ex(socket.gethostname())[2]
        # print(ip)
        shared_mode = 1
        username = getpass.getuser()
        ip = '127.0.0.1'
        status = 0

        for index in range(self.listView.count()):
            object_id = self.get_data_for_auto(self.listView.item(index).text())[0]
            if self.check_dublicate(object_id):
                print('найден дубликат', self.listView.item(index).text())
            else:
                self.insert_data(shared_mode, username, ip, status, object_id)
        self.listView.clear()


    def on_clicked(self):
        ark = []
        for index in range(self.listView.count()):
            ark.append(self.listView.takeItem(0).text())
        self.send_data(ark)

    def send_data(self, message):
        self.tcp_socket = socket(AF_INET, SOCK_STREAM)
        self.tcp_socket.connect(('127.0.0.1', 8888))
        message = pickle.dumps(message)
        print(message)
        self.tcp_socket.send(message)
        print('сообщение отправлено')
        respons = self.tcp_socket.recv(1024)
        print(pickle.loads(respons))
        self.tcp_socket.close()

    async def tcp_echo_client(self, message):
        self.reader, self.writer = await asyncio.open_connection(
            '127.0.0.1', 8888)
        message = pickle.dumps(message)
        self.writer.write(message)
        await self.writer.drain()
        print(f'Send: {message!r}')

        data = await self.reader.read()
        print(f'Received: {pickle.loads(data)!r}')

        print('Close the connection')
        # self.writer.close()
        # await self.writer.wait_closed()


class TreeModel(QtGui.QStandardItemModel, QtSql.QSqlDatabase):
    def __init__(self):
        QtGui.QStandardItemModel.__init__(self)
        QtSql.QSqlDatabase.__init__(self)
        self.treedb = self.addDatabase('QMYSQL', 'TreeData')
        self.treedb.setHostName('localhost')
        self.treedb.setDatabaseName('autoexchange')
        self.treedb.setUserName('d.dikiy')
        self.treedb.setPassword('Rhjyjc2910')
        if not self.treedb.open():
            print('Нет подключения к бд')
        else:
            print('подключение для дерева успешно выполнено')

    def get_obj_name(self, param):
        query = QtSql.QSqlQuery()
        lst = []
        query.exec(
            f'SELECT ExchangeData_ObjName FROM exchangedata WHERE objectclass_id = (SELECT objectclass_id FROM objectclass WHERE ObjectClass_Name = "{param}")')
        if query.isActive():
            query.first()
            while query.isValid():
                lst.append(query.value('ExchangeData_ObjName'))
                query.next()
        else:
            print('Нет конекта')

        return lst

    def get_obj_class_name(self):
        query = QtSql.QSqlQuery()
        lst = []
        query.exec_('SELECT ObjectClass_Name FROM objectclass')
        if query.isActive():
            query.first()
            while query.isValid():
                lst.append(query.value('ObjectClass_Name'))
                query.next()
        return lst

    def add_data(self):
        sti = QtGui.QStandardItemModel()
        for i in self.get_obj_class_name():
            root_item = QtGui.QStandardItem(i)
            root_item.setFlags(root_item.flags() & ~QtCore.Qt.ItemIsDragEnabled & ~QtCore.Qt.ItemIsDropEnabled)
            for q in self.get_obj_name(i):
                item = QtGui.QStandardItem(q)
                root_item.appendRow(item)
            sti.appendRow([root_item])
        self.treedb.close()
        return sti

    def close(self):
        self.removeDatabase('TreeData')


class MyListWidget(QtWidgets.QListWidget):

    def __init__(self):
        super().__init__()
        self.setAcceptDrops(True)
        self.setAutoScroll(True)
        self.setProperty("showDropIndicator", True)
        self.setDragEnabled(True)
        self.setDragDropOverwriteMode(True)
        self.setDragDropMode(QtWidgets.QAbstractItemView.DragDrop)
        self.setSelectionMode(QtWidgets.QAbstractItemView.ContiguousSelection)
        self.setDefaultDropAction(QtCore.Qt.MoveAction)
        self.setTextElideMode(QtCore.Qt.ElideLeft)
        self.setFlow(QtWidgets.QListView.TopToBottom)
        self.setUniformItemSizes(False)
        self.setObjectName("listWidget")

    def dragMoveEvent(self, QDragMoveEvent):
        if QDragMoveEvent.mimeData().hasFormat('application/x-qabstractitemmodeldatalist'):
            QDragMoveEvent.setDropAction(QtCore.Qt.MoveAction)
            QDragMoveEvent.accept()
        else:
            QDragMoveEvent.ignore()

    def dropEvent(self, event):
        if self.viewport().rect().contains(event.pos()):
            fake_model = QtGui.QStandardItemModel()
            fake_model.dropMimeData(event.mimeData(), event.dropAction(), 0, 0, QtCore.QModelIndex())
            if self.count() > 0:
                if self.findItems(fake_model.item(0, 0).text(), QtCore.Qt.MatchContains):
                    return  # добавить алерт
        super(MyListWidget, self).dropEvent(event)

    def add_item_list(self):

        pass


app = QtWidgets.QApplication(sys.argv)
application = MainView()
application.show()
sys.exit(app.exec())

# with tempfile.NamedTemporaryFile(delete=False, encoding='utf-8', mode='w', dir=os.path.curdir, prefix='GLB_',
#                                  suffix='_.prm') as x:
#     x.write('[General]\n' + 'Output=' + os.path.abspath(
#         os.curdir) + '\\Log\\test.log' + '\n' + 'Quit=0 \n' + 'AutoExchange=1 \n \n' + '[AutoExchange] \n' + 'SharedMode=1 \n' + 'ReadFrom=REK \n' + 'WriteTo=REK')
#     os.system(
#         'start /low /d"\\\srvglobal\\User\\db.adm\\1cv77.adm\\BIN" 1cv7s.exe CONFIG /M /D\\\srvglobal\\user\\db.adm\\tr5 /Nadm /Padm /@' + x.name)
#     x.close()
#
# with tempfile.NamedTemporaryFile(delete=False, encoding='utf-8', mode='w', dir=os.path.curdir, prefix='GLB_',
#                                  suffix='_.bat') as t:
#     t.write(
#         'start /low /d"\\\srvglobal\\User\\db.adm\\1cv77.adm\\BIN" 1cv7s.exe CONFIG /M /D\\\srvglobal\\user\\db.adm\\tr5 /Nadm /Padm /@'+x.name)
#     t.close()
#     process = subprocess.Popen(t.name)
#     code = process.wait()
#     print(code)
