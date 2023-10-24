# Form implementation generated from reading ui file 'Authorization.ui'
#
# Created by: PyQt6 UI code generator 6.5.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.

import pymysql

from config import host, user, password, db_name

from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QMessageBox


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(680, 635)
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayoutWidget = QtWidgets.QWidget(parent=self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(130, 20, 431, 511))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.auth_label = QtWidgets.QLabel(parent=self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Avenir")
        font.setPointSize(40)
        font.setBold(True)
        font.setWeight(75)
        self.auth_label.setFont(font)
        self.auth_label.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.auth_label.setTextFormat(QtCore.Qt.TextFormat.RichText)
        self.auth_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.auth_label.setWordWrap(False)
        self.auth_label.setObjectName("auth_label")
        self.verticalLayout.addWidget(self.auth_label)
        spacerItem = QtWidgets.QSpacerItem(18, 100, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.login_label = QtWidgets.QLabel(parent=self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Avenir")
        font.setPointSize(33)
        font.setBold(True)
        font.setWeight(75)
        self.login_label.setFont(font)
        self.login_label.setTextFormat(QtCore.Qt.TextFormat.RichText)
        self.login_label.setWordWrap(False)
        self.login_label.setObjectName("login_label")
        self.verticalLayout.addWidget(self.login_label)
        self.loginEnter = QtWidgets.QTextEdit(parent=self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Avenir")
        font.setPointSize(33)
        font.setBold(True)
        font.setWeight(75)
        self.loginEnter.setFont(font)
        self.loginEnter.setMouseTracking(False)
        self.loginEnter.setObjectName("loginEnter")
        self.verticalLayout.addWidget(self.loginEnter)
        self.pass_label = QtWidgets.QLabel(parent=self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Avenir")
        font.setPointSize(33)
        font.setBold(True)
        font.setWeight(75)
        self.pass_label.setFont(font)
        self.pass_label.setTextFormat(QtCore.Qt.TextFormat.RichText)
        self.pass_label.setWordWrap(False)
        self.pass_label.setObjectName("pass_label")
        self.verticalLayout.addWidget(self.pass_label)
        self.passEnter = QtWidgets.QTextEdit(parent=self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Avenir")
        font.setPointSize(33)
        font.setBold(True)
        font.setWeight(75)
        self.passEnter.setFont(font)
        self.passEnter.setObjectName("passEnter")
        self.verticalLayout.addWidget(self.passEnter)
        spacerItem1 = QtWidgets.QSpacerItem(18, 98, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.authButton = QtWidgets.QPushButton(parent=self.verticalLayoutWidget)
        self.authButton.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.authButton.sizePolicy().hasHeightForWidth())
        self.authButton.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Avenir")
        font.setPointSize(33)
        font.setBold(True)
        font.setWeight(75)
        self.authButton.setFont(font)
        self.authButton.setAutoDefault(False)
        self.authButton.setDefault(False)
        self.authButton.setFlat(False)
        self.authButton.setObjectName("authButton")
        self.verticalLayout.addWidget(self.authButton)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 680, 24))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(parent=MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.add_functions()


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.auth_label.setText(_translate("MainWindow", "Авторизация"))
        self.login_label.setText(_translate("MainWindow", "Логин:"))
        self.pass_label.setText(_translate("MainWindow", "Пароль:"))
        self.authButton.setText(_translate("MainWindow", "Войти"))

    def add_functions(self):
        self.authButton.clicked.connect(self.authButtonClick)

    def authButtonClick(self): # Кнопка входа
        print(self.loginEnter.toPlainText())
        print(self.passEnter.toPlainText())
        auth = f"SELECT * FROM User WHERE User_Login = '{self.loginEnter.toPlainText()}' AND User_Password = '{self.passEnter.toPlainText()}';"
        usercursor = connection.cursor()
        usercursor.execute(auth)
        user = usercursor.fetchone()

        if user:
            print("Здравствуйте!")
        else:
            print("Пользователь не найденъ")
            error = QMessageBox() # Всплывающее окно
            error.setWindowTitle("Пользователь не найден") # Заголовок
            error.setText("Ошибка в логине или пароле!") # Основной текст
            error.setInformativeText("Попробуйте снова") # Дополнительный текст

            # error.setIcon(QMessageBox.Warning) # Изменение иконки
            # error.setStandardButtons(QMessageBox.StandardButton.Ok|QMessageBox.StandardButton.Cancel) # Добавление кнопок

            error.buttonClicked.connect(self.popup_action)

            error.exec()

    def popup_action(self, btn): # Отслеживание нажатия на кнопку
        if btn.text() == "OK":
            print("Нажата кнопка Ok")



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())

connection = pymysql.connect(
        host=host,
        port=3306,
        user=user,
        password=password,
        database=db_name,
        cursorclass=pymysql.cursors.DictCursor)





