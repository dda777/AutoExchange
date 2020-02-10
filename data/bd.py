import MySQLdb
from config import BDProperties


class DataBase(BDProperties):

    def __init__(self):
        BDProperties.__init__(self)
        try:
            self.conn = MySQLdb.connect(
                user=self.getUserName(),
                password=self.getPassword(),
                host=self.getHost(),
                database=self.getDataBase(),
                charset='utf8')
        except:
            print('Все плохо')

    def getObjName(self, param=''):
        data = []

        sql = "SELECT ExchangeData_ObjName FROM exchangedata WHERE objectclass_id = (SELECT objectclass_id FROM objectclass WHERE ObjectClass_Name = '" +param+"')"
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql)
            for row in cursor.fetchall():
                data.append(row[0])
            return data

        except:
            return print('Все плохо')

    def getObjClassName(self, param='ObjectClass_Name'):
        data = []

        sql = "SELECT " + param + " FROM ObjectClass"
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql)
            for row in cursor.fetchall():
                data.append(row[0])
            return data

        except:
            return print('Все плохо')
