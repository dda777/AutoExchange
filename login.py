from view.auth_view import Ui_Dialog as TableDialogObj
from PyQt5.QtWidgets import QDialog


class DialogWindowLogin(QDialog, TableDialogObj):
    '''
    Класс диалогового окна для авторизации пользователя
    '''
    def __init__(self):
        QDialog.__init__(self)
        self.setupUi(self)
        self.pushButton_auth.clicked.connect(self.auth)

    def auth(self):
        print(self.lineEdit_login.text(), self.lineEdit_password.text())
