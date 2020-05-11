from PyQt5 import QtSql, QtCore
from PyQt5.QtSql import QSqlQuery, QSqlTableModel


class MyQSqlDatabase(QtSql.QSqlDatabase):
    def __init__(self, conn):
        QtSql.QSqlDatabase.__init__(self)
        if QtSql.QSqlDatabase.contains(conn):
            QtSql.QSqlDatabase.removeDatabase(conn)
        self.db = self.addDatabase('QODBC', conn)
        self.db.setDatabaseName(
            'DRIVER={SQL Server};SERVER=srvprintinfo;DATABASE=autoexchange;UID=admsuppdb;PWD=nhfycajhvfnjh')

    def connect(self):
        return self.db

    def insert_operations(self, enterprise_names, hash_key, operation_shared_mode=1, user_id=1):
        if not self.db.open():
            return print('Нет подключения к бд')

        query = QtSql.QSqlQuery(self.db)
        query.prepare('{CALL dbo.insert_operations(?, ?, ?)}')
        query.bindValue(0, operation_shared_mode)
        query.bindValue(1, user_id)
        query.bindValue(2, hash_key)
        query.exec()
        query.finish()
        for name in enterprise_names:
            query.prepare('{CALL dbo.insert_suboperation(?, ?)}')
            query.bindValue(0, hash_key)
            query.bindValue(1, name)
            query.exec()
            query.finish()
        self.db.close()

    def add_user(self, name, surname, login, ip):
        if not self.db.open():
            return print('Нет подключения к бд')

        query = QtSql.QSqlQuery(self.db)
        query.prepare('{CALL dbo.add_user(?, ?, ?, ?)}')
        query.bindValue(0, name)
        query.bindValue(1, surname)
        query.bindValue(2, login)
        query.bindValue(3, ip)
        query.exec()
        query.finish()
        self.db.close()

    def user_log(self, user_id, ip, text_log='Login'):
        if not self.db.open():
            return print('Нет подключения к бд')

        query = QtSql.QSqlQuery(self.db)
        query.prepare('{CALL dbo.user_log(?, ?, ?)}')
        query.bindValue(0, user_id)
        query.bindValue(1, ip)
        query.bindValue(2, text_log)
        query.exec()
        query.finish()
        self.db.close()

    def check_user_exists(self, login):
        if not self.db.open():
            return print('Нет подключения к бд')

        query = QtSql.QSqlQuery(self.db)
        query.prepare('{CALL dbo.check_user_exists(?)}')
        query.bindValue(0, login)
        query.exec()
        if query.isActive():
            query.first()
            chk = query.value(0)
        else:
            chk = 0
        self.db.close()
        return int(chk)

    def get_user_id(self, login):
        if not self.db.open():
            return print('Нет подключения к бд')

        query = QtSql.QSqlQuery(self.db)
        query.prepare('{CALL dbo.get_user_id(?, ?)}')
        query.bindValue(0, login)
        query.bindValue(1, 0, QtSql.QSql.Out)
        query.exec_()
        chk = query.boundValue(1)
        self.db.close()
        return chk

    #
    # Получаем имя магазина и id региона из view get_enterprise_name, все отсортировано по Region_ID
    #

    def get_enterprise_name(self):
        if not self.db.open():
            return print('Нет подключения к бд')

        query = QtSql.QSqlQuery(self.db)
        lst = []
        query.exec('SELECT * FROM dbo.get_enterprise_name')
        if query.isActive():
            query.first()
            while query.isValid():
                lst.append([query.value('Name'), query.value('ID')])
                query.next()
        self.db.close()
        return lst

    #
    # Получаем имя региона и id региона из view get_region_name, все отсортировано по Region_ID
    #

    def get_region_name(self):
        if not self.db.open():
            print('Нет подключения к бд')

        query = QtSql.QSqlQuery(self.db)
        lst = []
        query.exec_('SELECT * FROM dbo.get_region_name')
        if query.isActive():
            query.first()
            while query.isValid():
                lst.append([query.value('Name'), query.value('ID')])
                query.next()
        self.db.close()
        return lst

    def select_data_model(self):
        if not self.db.open():
            return print('Нет подключения к бд')

        # query = QtSql.QSqlQuery(self.db)
        # query.prepare('SELECT * FROM dbo.operation_info')
        # query.exec()
        query = QSqlQuery('SELECT * FROM dbo.operation_info', self.db)
        model = QSqlTableModel()
        model.setEditStrategy(QSqlTableModel.OnFieldChange)
        model.setQuery(query)
        model.setHeaderData(0, QtCore.Qt.Horizontal, "Пользователь")
        model.setHeaderData(1, QtCore.Qt.Horizontal, "IP")
        model.setHeaderData(2, QtCore.Qt.Horizontal, "Дата операции")
        model.setHeaderData(3, QtCore.Qt.Horizontal, "В ожидании")
        model.setHeaderData(4, QtCore.Qt.Horizontal, "В работе")
        model.setHeaderData(5, QtCore.Qt.Horizontal, "Выполнено")
        model.setHeaderData(6, QtCore.Qt.Horizontal, "Выполнено с ошибкой")
        model.submitAll()

        # model.select()
        return model

# now = QDateTime.currentDateTime().toString(Qt.ISODate)
# shared_mode = 1
# username = 'dda'
# ip = '127.0.0.1'
# status = 0
# q.insert_data(shared_mode,username,ip,status,1)

