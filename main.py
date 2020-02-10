# -*- coding: cp1251 -*-
import tempfile, os, sys
from view.main import Ui_MainWindow
from data.bd import DataBase
from PyQt5 import QtCore, QtWidgets, QtGui, uic


class UserData(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self, parent=None)
        self.db = DataBase()
        self.model = TreeModel()
        self.setupUi(self)
        self.cbo = self.listWidget
        self.pushButton.clicked.connect(self.on_clicked)

        self.treeWidget.setModel(self.model.add_data())



    def on_clicked(self, index: QtCore.QModelIndex):
        c = QtCore.QModelIndex()
        return print(c.data())


class TreeModel(QtGui.QStandardItemModel):
    def __init__(self):
        self.db = DataBase()
        QtGui.QStandardItemModel.__init__(self)
    def add_data(self):
        sti = QtGui.QStandardItemModel()
        for i in self.db.getObjClassName():
            root_item = QtGui.QStandardItem(i)
            root_item.setFlags(root_item.flags() & ~QtCore.Qt.ItemIsDragEnabled & ~QtCore.Qt.ItemIsDropEnabled)
            for q in self.db.getObjName(i):
                item = QtGui.QStandardItem(q)
                root_item.appendRow(item)
            sti.appendRow([root_item])
        return sti




app = QtWidgets.QApplication(sys.argv)
application = UserData()
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
