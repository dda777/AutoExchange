from PyQt5 import QtSql, QtCore
from PyQt5.QtCore import QDateTime, Qt


class MyQSqlDatabase(QtSql.QSqlDatabase):
    def __init__(self):
        QtSql.QSqlDatabase.__init__(self)
        self.conn = self.addDatabase('QMYSQL')
        self.conn.setHostName('localhost')
        self.conn.setDatabaseName('autoexchange')
        self.conn.setUserName('d.dikiy')
        self.conn.setPassword('Rhjyjc2910')
        if not self.conn.open():
            print('Нет подключения к бд')
        else:
            print('Подключение установлено')

    def get_data_for_auto(self, magname):
        self.query = QtSql.QSqlQuery()
        lst = []
        self.query.exec(
            f'SELECT ExchangeData_ID FROM exchangedata Where ExchangeData_ObjName IN ("{magname}")')
        if self.query.isActive():
            self.query.first()
            while self.query.isValid():
                lst.append(self.query.value('ExchangeData_ID'))
                self.query.next()

        return lst

    def check_dublicate(self, id):
        self.query = QtSql.QSqlQuery()
        self.query.exec(f'SELECT EXISTS(SELECT ExchangeOperation_Id FROM exchangeoperation WHERE ExchangeOperation_Status = 0 AND ExchangeData_ID = {id})')
        self.query.first()
        if self.query.value(0) == 0:
            return False
        else:
            return True


    def insert_data(self, shared_mode, username, ip, status, object_id):
        self.query = QtSql.QSqlQuery()
        now = QDateTime.currentDateTime().toString(Qt.ISODate)
        self.query.prepare(
            f'insert into exchangeoperation (ExchangeOperation_SharedMode, ExchangeOperation_UserName, ExchangeOperation_Ip, ExchangeOperation_Status, ExchangeData_ID, ExchangeOperation_DateTimeCreate) '
            f'values({shared_mode},"{username}", "{ip}", {status}, {object_id}, "{now}")')
        if not self.query.exec_():
            print('инсерт не прошел')
        else:
            print('инсерт выполнен')



# now = QDateTime.currentDateTime().toString(Qt.ISODate)
# shared_mode = 1
# username = 'dda'
# ip = '127.0.0.1'
# status = 0
# q.insert_data(shared_mode,username,ip,status,1)
