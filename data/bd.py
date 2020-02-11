from PyQt5 import QtSql


class MyQSqlDatabase(QtSql.QSqlDatabase):
    def __init__(self):
        QtSql.QSqlDatabase.__init__(self)
        self.conn = self.addDatabase('QSQLITE')
        self.conn.setDatabaseName('data/autoexchange')
        if not self.conn.open():
            print('Нет подключения к бд')
        else: print('Подключение установлено')
        self.query = QtSql.QSqlQuery()

    def __del__(self):
        self.conn.close()

    def get_obj_name(self, param):
        lst = []
        self.query.exec(
            f'SELECT ExchangeData_ObjName FROM exchangedata WHERE objectclass_id = (SELECT objectclass_id FROM objectclass WHERE ObjectClass_Name = "{param}")')
        if self.query.isActive():
            self.query.first()
            while self.query.isValid():
                lst.append(self.query.value('ExchangeData_ObjName'))
                self.query.next()
        else:
            print('Нет конекта')
        return lst

    def get_obj_class_name(self):
        lst = []
        self.query.exec('SELECT ObjectClass_Name FROM ObjectClass')
        if self.query.isActive():
            self.query.first()
            while self.query.isValid():
                lst.append(self.query.value('ObjectClass_Name'))
                self.query.next()
        return lst
