# -*- coding: cp1251 -*-
import sys, time
import socket
import uuid

# from PyQt5 import QtCore, QtWidgets, Qt
from PyQt5.QtSql import QSqlQuery, QSqlQueryModel

from data.bd import MyQSqlDatabase as mainDataBase
from view.main_view import Ui_MainWindow

from PyQt5.QtWidgets import QMainWindow, QListWidgetItem, QMessageBox, QApplication, QSplashScreen
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QTimer, QModelIndex, QThread, pyqtSignal

import getpass
from ldap3 import Server, Connection

user_id = None
# ������� ���������� ��� Splash Screen ��������
splash_i = 100  # ��������� �������� ����� SplashScreen
splash_stop = 0  # ��������� ��������� SplashScreen
max_i = 180  # ����. ���� SplashScreen


def updateSplashScreen():
    global splash_i, splash_stop

    # ���� ������� ���� ����� ������������� �� �������� ������ ��������
    if splash_i == 270:
        splash_i = 0
        splash_stop = 1
    else:  # ����� ��������� ���� �� ���������
        if splash_i < max_i:
            splash_i = splash_i + 1
    pixmap = QPixmap('data/splash/splash_' + str(splash_i) + '.png')
    splashScreen.setPixmap(pixmap)


class MainView(QMainWindow):
    def __init__(self):
        global user_id
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.db = mainDataBase('info_connect_update')

        # self.DialogWindowLogin = DialogWindowLogin()
        # self.DialogWindowLogin.show()
        # self.DialogWindowLogin.exec()

        self.ui.pushButton.clicked.connect(self.on_clicked)
        self.ui.pushButton_2.clicked.connect(self.on_clicked_add)
        self.ui.pushButton_3.clicked.connect(self.on_clicked_del)

        self.set_model()
        self.timer = QTimer()
        self.timer.timeout.connect(self.set_model)
        self.timer.start(5000)

    def set_model(self):
        if user_id is None:
            return
        if not self.db.connect().open():
            return print('��� ����������� � ��')

        sql = '{CALL dbo.operation_info_for_current_user(' + str(user_id) + ')}'

        query = QSqlQuery(sql, self.db.connect())
        model = QSqlQueryModel()

        model.setQuery(query)
        model.setHeaderData(0, Qt.Horizontal, "������������")
        model.setHeaderData(1, Qt.Horizontal, "IP")
        model.setHeaderData(2, Qt.Horizontal, "���� ��������")
        model.setHeaderData(3, Qt.Horizontal, "� ��������")
        model.setHeaderData(4, Qt.Horizontal, "� ������")
        model.setHeaderData(5, Qt.Horizontal, "���������")
        model.setHeaderData(6, Qt.Horizontal, "��������� � �������")

        self.ui.tableView.setModel(model)
        self.ui.tableView.show()

    def on_clicked_add(self):
        duplicate = ''
        if self.ui.treeView.selectedIndexes():
            for i in range(self.ui.treeView.model().rowCount(self.ui.treeView.rootIndex())):

                root = self.ui.treeView.model().index(i, 0, QModelIndex())
                if self.ui.treeView.model().index(i, 0, QModelIndex()) in self.ui.treeView.selectedIndexes():
                    for j in range(self.ui.treeView.model().rowCount(root)):
                        text = self.ui.treeView.model().data(self.ui.treeView.model().index(j, 0, root))
                        if self.ui.listWidget.findItems(text, Qt.MatchRecursive):
                            # duplicate += f'{}'
                            print('�������� ��� ���� � ������', duplicate)  # ����� ������� �����!
                        else:
                            self.ui.listWidget.addItem(QListWidgetItem(text))
                else:
                    for j in range(self.ui.treeView.model().rowCount(root)):
                        if self.ui.treeView.model().index(j, 0, root) in self.ui.treeView.selectedIndexes():
                            text = self.ui.treeView.model().data(self.ui.treeView.model().index(j, 0, root))
                            if self.ui.listWidget.findItems(text, Qt.MatchRecursive):
                                duplicate += text
                                print('�������� ��� ���� � ������', duplicate)  # ����� ������� �����!
                            else:
                                self.ui.listWidget.addItem(QListWidgetItem(text))

        else:
            for i in range(self.ui.treeView.model().rowCount(self.ui.treeView.rootIndex())):
                root = self.ui.treeView.model().index(i, 0, QModelIndex())
                for j in range(self.ui.treeView.model().rowCount(root)):
                    text = self.ui.treeView.model().data(self.ui.treeView.model().index(j, 0, root))
                    q = self.ui.treeView.model()
                    print(q)
                    item = QListWidgetItem(text)

                    if self.ui.listWidget.findItems(text, Qt.MatchRecursive):
                        print('�������� ��� ���� � ������', text)  # ����� ������� �����!
                    else:
                        self.ui.listWidget.addItem(item)

    def on_clicked_del(self):
        listitems = self.ui.listWidget.selectedItems()
        if not listitems: self.ui.listWidget.clear()
        for item in listitems:
            self.ui.listWidget.takeItem(self.ui.listWidget.row(item))

    def message_box(self, title, text):
        return QMessageBox.about(self, f'{title}', f'{text}')

    def on_clicked(self):
        global user_id
        HOST, PORT = "10.88.2.54", 8887
        hash_key = uuid.uuid4().hex
        names = []

        for index in range(self.ui.listWidget.count()):
            names.append(self.ui.listWidget.takeItem(0).text())

        if not names:
            return self.message_box('������', '�� �� ������� ������ ��� ����������')

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            # Connect to server and send data
            try:
                sock.connect((HOST, PORT))
                mainDataBase('insert_operation').insert_operations(names, hash_key, user_id=user_id)
                sock.sendall(bytes(hash_key, "utf-8"))
            except socket.error as err:
                return self.message_box('������', err.__reduce__()[1][1])
            except:
                return self.message_box('������', '����������� ������')


class UserData:
    def __init__(self, user_login):
        super().__init__()
        self.conn = Connection(Server('dc00.tavriav.local'), 'tavriav\d.dikiy', 'Rhjyjc2910')
        self.userLogin = user_login
        self.db_user_conn = mainDataBase('user_insert')

    def getName(self):
        self.conn.bind()
        self.conn.search('dc=tavriav,dc=local', f'(&(objectClass=user)(sAMAccountName={self.userLogin}))',
                         attributes=['CN'])
        for name in self.conn.entries[0]:
            self.conn.unbind()
            return str(name).split()

    def getIp(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(('172.16.7.40', 1))  # connect() for UDP doesn't send packets
            return s.getsockname()[0]
        except socket.error:
            return '127.0.0.1'

    def run(self):
        global user_id

        ip = self.getIp()

        if self.db_user_conn.check_user_exists(self.userLogin):
            user_id = self.db_user_conn.get_user_id(self.userLogin)
            self.db_user_conn.user_log(user_id, ip, '���� � ���������')
        else:
            self.db_user_conn.add_user(self.getName()[1], self.getName()[0], self.userLogin, ip)
            user_id = self.db_user_conn.get_user_id(self.userLogin)
            self.db_user_conn.user_log(user_id, ip, '������������ ������')


# ����� ��� ����������� ���������� SplashScreen
class SplashThread(QThread):
    mysignal = pyqtSignal(int)  # ������� ������, ������� ����� ������������� �� ��������� �������

    def __init__(self, parent=None):
        QThread.__init__(self, parent)
        self.user_login = getpass.getuser()
        self.process = UserData(self.user_login)

    def run(self):
        global splash_i, splash_stop, max_i  # ���������� ����������

        start_time = time.time()
        self.process.run()
        t = round(time.time() - start_time)
        if t < 3:
            max_i = 180
        elif t >= 3:
            max_i = max_i + 90

        print('loading widgets done')

        start_time = time.time()
        # time.sleep(2)  # 3 �������
        t = round(time.time() - start_time)
        if t < 3:
            max_i = 270
        elif t >= 3:
            max_i = max_i + 90

        print('loading data done')

        # ������� ���������� ���� ��������
        while splash_stop == 0:
            app.processEvents()
        if splash_stop == 1:
            self.mysignal.emit(1)  # ���������� ������ �� ������ � ���, ��� ���� ���������� SplashScreen


# ������� ��������� ������� � �������� SplashScreen ����
def stopTimer(signal):
    if signal == 1:
        timer.stop()  # ������������� ������
        application.show()  # ���������� �����
        splashScreen.finish(application)  # ��������� SplashScreen
    else:
        pass


app = QApplication(sys.argv)

# ����� ��� SplashScreen
SplashThread = SplashThread()

# ������� splashScreen
splashScreen = QSplashScreen()
splashPixmap = QPixmap('data/splash/splash_100.png')
splashScreen.setPixmap(splashPixmap)
splashScreen.show()

# ������� ����� ����������
application = MainView()

# ������� ������ ��� splashScreen
timer = QTimer()
timer.setInterval(33.33)
timer.setSingleShot(False)
timer.timeout.connect(updateSplashScreen)
timer.start()

# ����������� � ������
SplashThread.mysignal.connect(stopTimer)
# ��������� �����
SplashThread.start()

sys.exit(app.exec_())
