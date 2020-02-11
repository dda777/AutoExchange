# -*- coding: cp1251 -*-
import sys
from view.main import Ui_Form
from data.bd import MyQSqlDatabase
from PyQt5 import QtCore, QtWidgets, QtGui


class MainView(QtWidgets.QMainWindow, Ui_Form):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self, parent=None)
        self.setupUi()
        self.model = TreeModel()
        self.listView = MyListEvent()

        self.treeView.setModel(self.model.add_data())



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


class MyListEvent(QtWidgets.QListView):
    def __init__(self):
        QtWidgets.QListView.__init__(self)
        self.setAcceptDrops(True)

    def dragEnterEvent(self, e):

        if e.mimeData().hasFormat('text/plain'):
            e.accept()
        else:
            e.ignore()

    def dropEvent(self, e):

        self.setText(e.mimeData().text())




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
