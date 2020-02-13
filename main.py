# -*- coding: cp1251 -*-
import sys
from view.main import Ui_Form
from data.bd import MyQSqlDatabase
from PyQt5 import QtCore, QtWidgets, QtGui


class MainView(QtWidgets.QWidget):
    def __init__(self):
        QtWidgets.QWidget.__init__(self, parent=None)
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
        self.pushButton_1.clicked.connect(self.on_clicked)

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

    def on_clicked(self):
        pass


class TreeModel(QtGui.QStandardItemModel, MyQSqlDatabase):
    def __init__(self):
        QtGui.QStandardItemModel.__init__(self)
        MyQSqlDatabase.__init__(self)

    def add_data(self):
        sti = QtGui.QStandardItemModel()
        for i in self.get_obj_class_name():
            root_item = QtGui.QStandardItem(i)
            root_item.setFlags(root_item.flags() & ~QtCore.Qt.ItemIsDragEnabled & ~QtCore.Qt.ItemIsDropEnabled)
            for q in self.get_obj_name(i):
                item = QtGui.QStandardItem(q)
                root_item.appendRow(item)
            sti.appendRow([root_item])
        return sti


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
