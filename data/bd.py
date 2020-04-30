from PyQt5 import QtSql, QtCore


class MyQSqlDatabase(QtSql.QSqlDatabase):
    def __init__(self, conn):
        QtSql.QSqlDatabase.__init__(self)
        if QtSql.QSqlDatabase.contains(conn):
            QtSql.QSqlDatabase.removeDatabase(conn)
        self.db = self.addDatabase('QODBC', conn)
        self.db.setDatabaseName(
            'DRIVER={SQL Server}; SERVER=HOMEDES001\SQLEXPRESS; DATABASE=autoexchange; UID=d.dikiy; PWD=Rhjyjc2910')

    #
    # Добавляем данные об операции в бд, enterprise_data_id , shared_mode, user_id
    #

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
        print('query ok')
        for name in enterprise_names:
            query.prepare('{CALL dbo.insert_suboperation(?, ?)}')
            query.bindValue(0, hash_key)
            query.bindValue(1, name)
            query.exec()
            query.finish()
        self.db.close()

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
        query = QtSql.QSqlQuery(self.db)
        query.prepare('SELECT * FROM dbo.operation_info')
        query.exec()
        model = QtSql.QSqlQueryModel()
        model.setQuery(query)
        # model.select()
        return model

# now = QDateTime.currentDateTime().toString(Qt.ISODate)
# shared_mode = 1
# username = 'dda'
# ip = '127.0.0.1'
# status = 0
# q.insert_data(shared_mode,username,ip,status,1)
