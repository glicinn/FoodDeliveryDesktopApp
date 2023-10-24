from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QTableWidgetItem
from untitled import Ui_MainWindow
from config import host, user, password, db_name, port
import sys
import pymysql

class window(QtWidgets.QMainWindow):
    def __init__(self):
        super(window, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.saveUserButton.clicked.connect(self.addUsers)
        self.ui.tableWidget.doubleClicked.connect(self.doubleClick)

        self.loadUsers()

    # Функция вывода пользователей в TableWidget
    def loadUsers(self):

        users = [
            {'name': 'Ярослав', 'surname': 'Бебряков'},
            {'name': 'Дмитрий', 'surname': 'Ярило'},
            {'name': 'Александр', 'surname': 'Навозов'}
        ]

        # tableWidget - название поля
        self.ui.tableWidget.setRowCount(len(users))  # Кол-во строк
        self.ui.tableWidget.setColumnCount(2) # Кол-во столбцов

        self.ui.tableWidget.setHorizontalHeaderLabels(('Имя', 'Фамилия')) # Заголовки столбцов

        self.ui.tableWidget.setColumnWidth(0, 120) # Ширина столбцов (индекс, ширина)
        self.ui.tableWidget.setColumnWidth(1, 200)


        # # Заполнение ячеек (индекс строки, индекс столбца, значение)
        # self.ui.tableWidget.setItem(0, 0, QTableWidgetItem('Ярослав'))
        # self.ui.tableWidget.setItem(0, 1, QTableWidgetItem('Бебряков'))
        # self.ui.tableWidget.setItem(1, 0, QTableWidgetItem('Дмитрий'))
        # self.ui.tableWidget.setItem(1, 1, QTableWidgetItem('Ярило'))


        # Заполнение ячеек через цикл
        row_index = 0
        # try:
        #     with connection.cursor() as cursor:
        #         # SQL-запрос для подсчета количества столбцов в таблице
        #         sql_query = "SELECT COUNT(*) FROM information_schema.columns WHERE table_schema = %s AND table_name = %s"
        #         # Указание имени базы данных и таблицы
        #         database_name = 'Kursach'
        #         table_name = 'User'
        #         # Выполнение запроса с передачей параметров
        #         cursor.execute(sql_query, (database_name, table_name))
        #         # Получение результата запроса
        #         row_index = cursor.fetchone()
        #         row_index = row_index['COUNT(*)']
        # finally:
        #     # Закрытие соединения
        #     connection.close()

        print(row_index)
        for user in users:
            self.ui.tableWidget.setItem(row_index, 0, QTableWidgetItem(str(user['name'])))
            self.ui.tableWidget.setItem(row_index, 1, QTableWidgetItem(str(user['surname'])))
            row_index += 1




    # Функция добавления пользователей в TableWidget пр нажатии на кнопку
    def addUsers(self):
        # Получение данных с полей ввода
        name = self.ui.lineName.text()
        surname = self.ui.lineSurname.text()

        if name and surname is not None:
            rowCount = self.ui.tableWidget.rowCount()
            # Добавление новой строки
            self.ui.tableWidget.insertRow(rowCount)
            # Внос данных
            self.ui.tableWidget.setItem(rowCount, 0, QTableWidgetItem(name))
            self.ui.tableWidget.setItem(rowCount, 1, QTableWidgetItem(surname))



    # Функция вывода информации о ячейке при двойном нажатии на нее
    def doubleClick(self):
        for item in self.ui.tableWidget.selectedItems():
            print(item.row(), item.column(), item.text())





connection = pymysql.connect(
        host=host,
        port=port,
        user=user,
        password=password,
        database=db_name,
        cursorclass=pymysql.cursors.DictCursor)


def create_app():
    app = QtWidgets.QApplication(sys.argv)
    win = window()
    win.show()
    sys.exit(app.exec())

create_app()
