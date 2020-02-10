from enum import Enum
import os
import sys

from PyQt5 import QtCore, QtGui, QtWidgets

TXT_SYSTEM = "Master Data"
TXT_SECURITY = "Security Model"

TXT_CLIENT = "Clients"
TXT_STAKEHLD = "Stakeholders"
TXT_USER = "Users"

ICON_LVL_CLIENT = "img/icons8-bank-16.png"
ICON_LVL_STAKEHLD = "img/icons8-initiate-money-transfer-24.png"
ICON_LVL_USER = "img/icons8-checked-user-male-32.png"

TYPE_ROLE = QtCore.Qt.UserRole + 1000


class NodeRoles(Enum):
    ROOT_ROLE = 0
    CLIENT_ROLE = 1
    STAKEHOLD_ROLE = 2
    USER_ROLE = 3


CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))

SYSTEM_DATA = {
    TXT_USER: ["user_a", "user_b"],
    TXT_CLIENT: ["client_a", "client_b", "client_c", "client_d"],
    TXT_STAKEHLD: ["stakeholder_a", "stakeholder_b", "stakeholder_c", "stakeholder_d"],
}


SECURITY_DATA = {
    "client_a": {"stakeholder_b": ["user_a"]},
    "client_c": {"stakeholder_d": ["user_b"]},
}


class CustomModel(QtGui.QStandardItemModel):
    def __init__(self, system_data, security_data, parent=None):
        super().__init__(parent)
        self.create_system_node(system_data)
        #self.create_security_node(security_data)

    def create_system_node(self, system_data):
        root = QtGui.QStandardItem(TXT_SYSTEM)
        self.appendRow(root)

        for it in (root, self.invisibleRootItem()):
            it.setFlags(
                it.flags() & ~QtCore.Qt.ItemIsDragEnabled & ~QtCore.Qt.ItemIsDropEnabled
            )
            #it.setData(NodeRoles.ROOT_ROLE, TYPE_ROLE)

        for key, role in zip(
            (TXT_USER, TXT_CLIENT, TXT_STAKEHLD),
            (NodeRoles.USER_ROLE, NodeRoles.CLIENT_ROLE, NodeRoles.STAKEHOLD_ROLE),
        ):
            it = QtGui.QStandardItem(key)
            it.setFlags(
                it.flags() & ~QtCore.Qt.ItemIsDragEnabled & ~QtCore.Qt.ItemIsDropEnabled
            )

            #it.setData(NodeRoles.ROOT_ROLE, TYPE_ROLE)
            root.appendRow(it)
            #print(system_data[key])
            for value in system_data[key]:
                child = QtGui.QStandardItem(value)
                child.setFlags(child.flags() & ~QtCore.Qt.ItemIsDropEnabled)
                #child.setData(role, TYPE_ROLE)
                it.appendRow(child)

    # def create_security_node(self, security_data):
    #     root = QtGui.QStandardItem(TXT_SECURITY)
    #     root.setData(NodeRoles.ROOT_ROLE, TYPE_ROLE)
    #     self.appendRow(root)
    #     root.setFlags(root.flags() & ~QtCore.Qt.ItemIsDragEnabled)
    #
    #     self._fill_node(security_data, root, 0)
    #
    # def _fill_node(self, data, root, level):
    #     role = (NodeRoles.CLIENT_ROLE, NodeRoles.STAKEHOLD_ROLE, NodeRoles.USER_ROLE)[
    #         level
    #     ]
    #     icon_path = (ICON_LVL_CLIENT, ICON_LVL_STAKEHLD, ICON_LVL_USER)[level]
    #     icon = QtGui.QIcon(os.path.join(CURRENT_DIR, icon_path))
    #     if isinstance(data, dict):
    #         for key, value in data.items():
    #             it = QtGui.QStandardItem(key)
    #             it.setFlags(it.flags() & ~QtCore.Qt.ItemIsDropEnabled)
    #             it.setIcon(icon)
    #             it.setData(role, TYPE_ROLE)
    #             root.appendRow(it)
    #             self._fill_node(value, it, level + 1)
    #         return
    #     else:
    #         for d in data:
    #             it = QtGui.QStandardItem(d)
    #             it.setIcon(icon)
    #             it.setData(role, TYPE_ROLE)
    #             root.appendRow(it)


class TreeView(QtWidgets.QTreeView):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.initUI()

    def initUI(self):
        self.setHeaderHidden(True)
        self.setColumnHidden(1, True)
        self.setSelectionMode(self.SingleSelection)
        self.setDragDropMode(QtWidgets.QAbstractItemView.DragDrop)
        self.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

        self.resize(640, 480)

    def dragMoveEvent(self, event):
        if event.source() is not self:
            event.ignore()
            return
        fake_model = QtGui.QStandardItemModel()
        fake_model.dropMimeData(
            event.mimeData(), event.dropAction(), 0, 0, QtCore.QModelIndex()
        )
        it = fake_model.item(0)
        role = it.data(TYPE_ROLE)

        to_index = self.indexAt(event.pos())
        root = to_index
        print(self.model().item(0).index())
        while root.parent().isValid():
            root = root.parent()
        if root == self.model().item(0).index():
            event.ignore()
        else:
            super().dragMoveEvent(event)
            to_role = to_index.data(TYPE_ROLE)
            if (
                (to_role == NodeRoles.ROOT_ROLE and role == NodeRoles.CLIENT_ROLE)
                or (
                    to_role == NodeRoles.CLIENT_ROLE
                    and role == NodeRoles.STAKEHOLD_ROLE
                )
                or (to_role == NodeRoles.STAKEHOLD_ROLE and role == NodeRoles.USER_ROLE)
            ):
                to_item = self.model().itemFromIndex(to_index)
                for i in range(to_item.rowCount()):
                    child_it = to_item.child(i)
                    if child_it.text() == it.text():
                        event.ignore()
                        return
                self.setExpanded(to_index, True)
                super().dragMoveEvent(event)
            else:
                event.ignore()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    w = TreeView()
    model = CustomModel(system_data=SYSTEM_DATA, security_data=SECURITY_DATA)
    w.setModel(model)
    w.show()
    sys.exit(app.exec_())

# from PyQt5 import QtCore, QtWidgets, QtGui
# from PyQt5.QtCore import Qt
# from PyQt5.QtWidgets import QTreeWidgetItem
# import sys
#
# class Tree(QtWidgets.QTreeWidget):
#     def __init__(self, parent=None):
#         super().__init__(parent)
#
#         self.setDragDropMode(self.DragDrop)
#         self.setSelectionMode(self.ExtendedSelection)
#         self.setAcceptDrops(True)
#
#         for text in ['tree1','tree2','tree3']:
#             treeItem = QtWidgets.QTreeWidgetItem(self, [text])
#             treeItem.setFlags(treeItem.flags() & ~QtCore.Qt.ItemIsDropEnabled)
#             self.addTopLevelItem(treeItem)
#
#     def dropEvent(self, event):
#         if event.source() == self:
#             event.setDropAction(QtCore.Qt.MoveAction)
#             super().dropEvent(event)
#         elif isinstance(event.source(), QtWidgets.QListWidget):
#             item = self.itemAt(event.pos())
#             ix = self.indexAt(event.pos())
#             col = 0 if item is None else ix.column()
#             item = self.invisibleRootItem() if item is None else item
#             ba = event.mimeData().data('application/x-qabstractitemmodeldatalist')
#             data_items = decode_data(ba)
#             for data_item in data_items:
#                 it = QtWidgets.QTreeWidgetItem()
#                 item.addChild(it)
#                 for data in data_items:
#                     for r, v in data.items():
#                         it.setData(col, r, v)
#
#
# class List(QtWidgets.QListWidget):
#     def __init__(self, parent=None):
#         super().__init__(parent)
#
#         self.setDragDropMode(self.DragDrop)
#         self.setSelectionMode(self.ExtendedSelection)
#         self.setAcceptDrops(True)
#
#         for text in ['list1','list2','list3']:
#             self.addItem(text)
#
#     def dropEvent(self, event):
#         if event.source() == self:
#             event.setDropAction(QtCore.Qt.MoveAction)
#             QtWidgets.QListWidget.dropEvent(self, event)
#         elif isinstance(event.source(), QtWidgets.QTreeWidget):
#             item = self.itemAt(event.pos())
#             row = self.row(item) if item else self.count()
#             ba = event.mimeData().data('application/x-qabstractitemmodeldatalist')
#             data_items = decode_data(ba)
#             for i, data_item in enumerate(data_items):
#                 it = QtWidgets.QListWidgetItem()
#                 self.insertItem(row+i, it)
#                 for r, v in data_item.items():
#                     it.setData(r,v)
#
#
# def decode_data(bytearray):
#
#     data = []
#     item = {}
#
#     ds = QtCore.QDataStream(bytearray)
#     while not ds.atEnd():
#
#         row = ds.readInt32()
#         column = ds.readInt32()
#
#         map_items = ds.readInt32()
#         for i in range(map_items):
#             key = ds.readInt32()
#
#             value = QtCore.QVariant()
#             ds >> value
#             item[Qt.ItemDataRole(key)] = value
#
#         data.append(item)
#     return data
#
# if __name__=='__main__':
#
#     app = QtWidgets.QApplication(sys.argv)
#
#     layout = QtWidgets.QHBoxLayout()
#     layout.addWidget(Tree())
#     layout.addWidget(List())
#
#     container = QtWidgets.QWidget()
#     container.setLayout(layout)
#     container.show()
#
#     app.exec_()
