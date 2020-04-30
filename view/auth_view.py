from PyQt5 import QtCore, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(280, 280)
        self.verticalLayoutWidget = QtWidgets.QWidget(Dialog)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(40, 0, 200, 250))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.verticalLayout.setContentsMargins(10, 0, 10, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")

        self.label_login = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_login.setMaximumSize(QtCore.QSize(100, 12))
        self.label_login.setContentsMargins(0,0,0,0)
        self.label_login.setObjectName("label_login")
        self.verticalLayout.addWidget(self.label_login)

        self.lineEdit_login = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.lineEdit_login.setMaximumSize(QtCore.QSize(250, 20))
        self.lineEdit_login.setContentsMargins(0, 0, 0, 0)
        self.lineEdit_login.setPlaceholderText("Логин")
        self.lineEdit_login.setObjectName("lineEdit_login")
        self.verticalLayout.addWidget(self.lineEdit_login)

        self.label_password = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_password.setMaximumSize(QtCore.QSize(100, 20))
        self.label_password.setContentsMargins(0, 0, 0, 0)
        self.label_password.setObjectName("label_password")
        self.verticalLayout.addWidget(self.label_password)

        self.lineEdit_password = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.lineEdit_password.setMaximumSize(QtCore.QSize(250, 20))
        self.lineEdit_password.setContentsMargins(0, 0, 0, 0)
        self.lineEdit_password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineEdit_password.setPlaceholderText('Пароль')
        self.lineEdit_password.setObjectName("lineEdit_password")
        self.verticalLayout.addWidget(self.lineEdit_password)

        self.label_domen = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_domen.setMaximumSize(QtCore.QSize(100, 20))
        self.label_domen.setObjectName("label_domen")
        self.verticalLayout.addWidget(self.label_domen)

        self.comboBox_domen = QtWidgets.QComboBox(self.verticalLayoutWidget)
        self.comboBox_domen.setObjectName("comboBox_domen")
        self.comboBox_domen.addItem("")
        self.comboBox_domen.addItem("")
        self.verticalLayout.addWidget(self.comboBox_domen)

        self.pushButton_auth = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pushButton_auth.setMinimumSize(QtCore.QSize(0, 30))
        self.pushButton_auth.setObjectName("pushButton_auth")

        self.verticalLayout.addWidget(self.pushButton_auth)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label_login.setText(_translate("Dialog", "Ваш логин:"))
        self.label_password.setText(_translate("Dialog", "Ваш пароль:"))
        self.label_domen.setText(_translate("Dialog", "Домен?"))
        self.comboBox_domen.setItemText(0, _translate("Dialog", "Нет"))
        self.comboBox_domen.setItemText(1, _translate("Dialog", "Tavriav"))
        self.pushButton_auth.setText(_translate("Dialog", "Войти"))
