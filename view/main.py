# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtWidgets, QtGui, QtSql


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(950, 850)
        MainWindow.setMinimumSize(QtCore.QSize(950, 850))
        MainWindow.setMaximumSize(QtCore.QSize(950, 850))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(780, 240, 131, 41))
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(10, 10, 731, 541))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setSizeConstraint(QtWidgets.QLayout.SetMinAndMaxSize)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(20)
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.treeView = QtWidgets.QTreeView(self.horizontalLayoutWidget)
        self.treeView.setObjectName("treeView")
        self.treeView.setDragEnabled(True)
        self.treeView.setUniformRowHeights(False)
        self.treeView.setAutoExpandDelay(0)
        self.treeView.setIndentation(20)
        self.treeView.header().setVisible(False)
        self.treeView.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)

        self.model = TreeModel()
        self.treeView.setModel(self.model.add_data())

        self.horizontalLayout.addWidget(self.treeView)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setContentsMargins(-1, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.pushButton_2 = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.pushButton_2.setObjectName("pushButton_2")
        self.verticalLayout.addWidget(self.pushButton_2)
        self.pushButton_3 = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.pushButton_3.setObjectName("pushButton_3")
        self.verticalLayout.addWidget(self.pushButton_3)
        self.horizontalLayout.addLayout(self.verticalLayout)

        self.listWidget = MyListWidget()

        self.horizontalLayout.addWidget(self.listWidget)
        self.tableView = QtWidgets.QTableView(self.centralwidget)
        self.tableView.setGeometry(QtCore.QRect(10, 560, 931, 241))
        self.tableView.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.tableView.setObjectName("tableView")
        self.checkBox = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox.setGeometry(QtCore.QRect(780, 300, 121, 23))
        self.checkBox.setObjectName("checkBox")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 950, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        MainWindow.setWindowTitle('Автообмен')

        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "Сделать Авто"))
        self.pushButton_3.setText(_translate("MainWindow", "<<"))
        self.pushButton_2.setText(_translate("MainWindow", ">>"))
        self.checkBox.setText(_translate("MainWindow", "Монопольно?"))

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
