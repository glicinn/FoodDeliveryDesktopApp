import pymysql
from PyQt6.uic import loadUiType
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox
from config import host, user, password, db_name, port
from PyQt6.QtWidgets import QTableWidgetItem
# import testQWidget
# from PyQt6 import QtWidgets
# import sys



AuthForm, AuthWindow = loadUiType("Authorization.ui")
AdminForm, AdminWindow = loadUiType("AdminWindow.ui")


# testQWidget.Ui_MainWindow()


class MainWindow(QMainWindow, AuthForm):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.authButton.clicked.connect(self.authButtonClick)

    # Кнопка входа
    def authButtonClick(self):
        print(self.loginEnter.toPlainText())
        print(self.passEnter.toPlainText())
        auth = f"SELECT * FROM User WHERE User_Login = '{self.loginEnter.toPlainText()}' AND User_Password = '{self.passEnter.toPlainText()}';"
        usercursor = connection.cursor()
        usercursor.execute(auth)
        user = usercursor.fetchone()

        if user:
            print("Здравствуйте!")
            super().close()
            self.admin_window = AdWindow()
            self.admin_window.show()


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

    # Отслеживание нажатия на кнопку
    def popup_action(self, btn):
        if btn.text() == "Ok":
            print("Нажата кнопка Ok")


class AdWindow(QMainWindow, AdminForm):
    def __init__(self):

        super().__init__()
        self.setWindowTitle("Окно администратора")
        self.setupUi(self)

        # Пользователи
        self.usersAddButton.clicked.connect(self.addUsers)
        self.usersEditButton.clicked.connect(self.updateUsers)
        self.usersDeleteButton.clicked.connect(self.deleteUsers)
        # Подключение события выделения строки в таблице
        self.tableWidget.itemSelectionChanged.connect(self.onItemSelectionChangedUsers)
        self.loadUsers()

        # Категории
        self.loadCategorys()

        # Роли
        self.loadRoles()

        # Льготы
        self.loadBenefits()

        # Поставщики
        self.loadSuppliers()

        # Товары
        self.loadProducts()

        # Отзывы
        self.loadFeedbacks()

        # Заказы
        self.loadOrders()



#------------------------ Пользователи --------------------------------


    # Функция вывода пользователей в TableWidget
    def loadUsers(self):

        try:
            with connection.cursor() as cursor:
                # SQL-запрос для подсчета количества столбцов в таблице
                sql_query = "SELECT COUNT(*) FROM information_schema.columns WHERE table_schema = %s AND table_name = %s"
                connection.commit()
                # Указание имени базы данных и таблицы
                database_name = db_name
                table_name = 'User'
                # Выполнение запроса с передачей параметров
                cursor.execute(sql_query, (database_name, table_name))
                # Получение результата запроса
                row_index = cursor.fetchone()
                row_index = row_index['COUNT(*)']
                row_index -= 1
                print(row_index)
        finally:
            # Закрытие соединения
            None

        try:
            with connection.cursor() as cursor:
                # SQL-запрос для выборки всех записей из таблицы
                sql_query = "SELECT * FROM User"
                connection.commit()
                # Выполнение запроса
                cursor.execute(sql_query)
                # Извлечение всех записей из результата запроса в виде списка словарей
                users = []
                # Получение имен столбцов, начиная с первого столбца
                columns = [column[0] for column in cursor.description[1:]]
                print(columns)

                # SQL-запрос для подсчета всех записей из таблицы
                sql_query2 = "SELECT COUNT(*) FROM User;"
                connection.commit()
                # Выполнение запроса
                cursor.execute(sql_query2)
                str_num = cursor.fetchone()
                str_num = str_num['COUNT(*)']
                print(str_num)

                # Перебор записей и добавление их в список в виде словарей
                # for row in cursor.fetchall():
                #     user = {}
                #     for i in range(len(columns)):
                #         # Используйте .get() для избежания ошибки KeyError и обработки None значений
                #         column_name = columns[i]
                #         column_value = row[i]
                #         user[column_name] = column_value if column_value is not None else None
                #     users.append(user)

                for i in range(str_num):
                    user = {}
                    for column in columns:
                        sql_query3 = f"SELECT {column} FROM User WHERE ID_User = {i+1};"
                        cursor.execute(sql_query3)
                        result = cursor.fetchone()  # Получаем одну строку из результата запроса
                        if result:
                            print(result)
                            user[column] = result[column]  # Первый элемент кортежа - это значение столбца
                        else:
                            user[column] = None
                    users.append(user)


                # Теперь переменная entities содержит все сущности из вашей таблицы в виде списка словарей
                print(users)
        finally:
            # Закрытие соединения
            # connection.close()
            None


        # tableWidget - название поля
        self.tableWidget.setRowCount(str_num)  # Кол-во строк
        self.tableWidget.setColumnCount(row_index) # Кол-во столбцов

        # Заголовки столбцов
        self.tableWidget.setHorizontalHeaderLabels(['Логин', 'Пароль', 'Почта', 'Баланс', 'Роль', 'Льгота'])

        # Ширина столбцов (индекс, ширина)
        for i in range(row_index):
            self.tableWidget.setColumnWidth(i, 145)

        # Заполнение QtTableWidget
        for row_index, row_data in enumerate(users):
            for column_index, data in enumerate(row_data.values()):
                item = QTableWidgetItem(str(data))
                self.tableWidget.setItem(row_index, column_index, item)


    # Функция добавления пользователей в TableWidget
    def addUsers(self):
        try:
            with connection.cursor() as cursor:
                # SQL-запрос для подсчета всех записей из таблицы
                sql_query2 = "SELECT COUNT(*) FROM User;"
                connection.commit()
                # Выполнение запроса
                cursor.execute(sql_query2)
                str_num = cursor.fetchone()
                str_num = str_num['COUNT(*)']
                str_num += 1
                print(str_num)
                # cursor.execute("SELECT LAST_INSERT_ID()")
                # last_inserted_id = cursor.fetchone()[0]

                # Получение данных с полей ввода
                login = self.userLoginLineEdit.text()
                password = self.userPasswordLineEdit.text()
                email = self.userEmailLineEdit.text()
                balance = self.userBalanceLineEdit.text()
                role = self.userRoleComboBox.currentText()
                benefit = self.userBenefitComboBox.currentText()
                print(self.userRoleComboBox.currentText())
                lines = [login, password, email, balance, role, benefit]

                if login and password and email and balance and role and benefit is not None:
                    try:
                        # Внос данных
                        sql_query = f"insert into User(User_Login, User_Password, Email, Balance, Role, Benefit_ID)\nvalues ('{login}', '{password}', '{email}', '{balance}', '{role}', {benefit});"
                        cursor.execute(sql_query)
                        self.loadUsers()

                    except:
                        error = QMessageBox()  # Всплывающее окно
                        error.setWindowTitle(" ")  # Заголовок
                        error.setText("Добавление не удалось")  # Основной текст
                        error.setInformativeText("Ошибка формата данных")  # Дополнительный текст
                        error.exec()

                else:
                    error = QMessageBox()  # Всплывающее окно
                    error.setWindowTitle(" ")  # Заголовок
                    error.setText("Добавление не удалось")  # Основной текст
                    error.setInformativeText("Не все поля заполнены")  # Дополнительный текст
                    error.exec()

        finally:
            # connection.close()
            None


    # Функция изменения пользователей в TableWidget
    def updateUsers(self):
        try:
            with connection.cursor() as cursor:
                selected_items = self.tableWidget.selectedItems()
                if selected_items:
                    selected_row = selected_items[0].row()
                    selected_row += 1
                    print(f"Выбрана строка: {(selected_row)}")

                # Получение данных с полей ввода
                login = self.userLoginLineEdit.text()
                password = self.userPasswordLineEdit.text()
                email = self.userEmailLineEdit.text()
                balance = self.userBalanceLineEdit.text()
                role = self.userRoleComboBox.currentText()
                benefit = self.userBenefitComboBox.currentText()
                print(self.userRoleComboBox.currentText())
                lines = [login, password, email, balance, role]

                if login and password and email and balance and role is not None:
                    try:
                        # Внос данных
                        sql_query = f"UPDATE User\n" \
                                    f"SET User_Login = '{login}', User_Password = '{password}', Email = '{email}', Balance = '{balance}', Role = '{role}', Benefit_ID = {benefit}\n" \
                                    f"WHERE ID_User = {selected_row}"
                        cursor.execute(sql_query)
                        self.loadUsers()

                    except:
                        error = QMessageBox()  # Всплывающее окно
                        error.setWindowTitle(" ")  # Заголовок
                        error.setText("Обновление не удалось")  # Основной текст
                        error.setInformativeText("Ошибка формата данных")  # Дополнительный текст
                        error.exec()

                else:
                    error = QMessageBox()  # Всплывающее окно
                    error.setWindowTitle(" ")  # Заголовок
                    error.setText("Обновление не удалось")  # Основной текст
                    error.setInformativeText("Не все поля заполнены")  # Дополнительный текст
                    error.exec()

        finally:
            # connection.close()
            None


    # Функция удаления пользователей в TableWidget
    def deleteUsers(self):
        try:
            with connection.cursor() as cursor:
                selected_items = self.tableWidget.selectedItems()
                if selected_items:
                    selected_row = selected_items[0].row()
                    selected_row += 1
                    print(f"Выбрана строка: {(selected_row)}")

                    try:
                        # Внос данных
                        sql_query = f"DELETE FROM User WHERE ID_User = {selected_row};"
                        cursor.execute(sql_query)
                        self.loadUsers()

                    except:
                        error = QMessageBox()  # Всплывающее окно
                        error.setWindowTitle(" ")  # Заголовок
                        error.setText("Удаление не удалось")  # Основной текст
                        error.setInformativeText("Объект не выбран")  # Дополнительный текст
                        error.exec()

                else:
                    error = QMessageBox()  # Всплывающее окно
                    error.setWindowTitle(" ")  # Заголовок
                    error.setText("Удаление не удалось")  # Основной текст
                    error.setInformativeText("Объект не выбран")  # Дополнительный текст
                    error.exec()

        finally:
            # connection.close()
            None


    #Функция отслеживания выбора строки
    def onItemSelectionChangedUsers(self):
        selected_items = self.tableWidget.selectedItems()
        if selected_items:
            try:
                selected_row = selected_items[0].row()
                # selected_row += 1
                selected_item = self.tableWidget.item(selected_row, 0)
                print(f"Выбрана строка: {selected_row} \nВыбрана ячейка: '{selected_item.text()}'")

                # Получение данных с полей ввода
                # sql_query = f"SELECT User_Login FROM User WHERE ID_User = {selected_row};"
                sql_query = f"SELECT User_Login FROM User WHERE User_Login = '{selected_item.text()}';"
                cursor.execute(sql_query)
                login = cursor.fetchone()
                login = login['User_Login']
                print(login)
                sql_query = f"SELECT User_Password FROM User WHERE User_Login = '{selected_item.text()}';"
                cursor.execute(sql_query)
                password = cursor.fetchone()
                password = password['User_Password']
                print(password)
                sql_query = f"SELECT Email FROM User WHERE User_Login = '{selected_item.text()}';"
                cursor.execute(sql_query)
                email = cursor.fetchone()
                email = email['Email']
                print(email)
                sql_query = f"SELECT Balance FROM User WHERE User_Login = '{selected_item.text()}';"
                cursor.execute(sql_query)
                balance = cursor.fetchone()
                balance = balance['Balance']
                print(balance)
                sql_query = f"SELECT Role FROM User WHERE User_Login = '{selected_item.text()}';"
                cursor.execute(sql_query)
                role = cursor.fetchone()
                role = role['Role']
                print(role)
                sql_query = f"SELECT Benefit_ID FROM User WHERE User_Login = '{selected_item.text()}';"
                cursor.execute(sql_query)
                benefit = cursor.fetchone()
                benefit = benefit['Benefit_ID']
                print(benefit)

                # Вывод данных в поля ввода
                self.userLoginLineEdit.setText(login)
                self.userPasswordLineEdit.setText(password)
                self.userEmailLineEdit.setText(email)
                self.userBalanceLineEdit.setText(str(balance))
                self.userRoleComboBox.setCurrentText(role)
                self.userBenefitComboBox.setCurrentText(str(benefit))

            except:
                error = QMessageBox()  # Всплывающее окно
                error.setWindowTitle(" ")  # Заголовок
                error.setText("Выбор невозможен")  # Основной текст
                error.setInformativeText("У сущности присутствуют нулевые значения")  # Дополнительный текст
                error.exec()









#------------------------ Категории --------------------------------

    # Функция вывода категорий в TableWidget
    def loadCategorys(self):

        try:
            with connection.cursor() as cursor:
                # SQL-запрос для подсчета количества столбцов в таблице
                sql_query = "SELECT COUNT(*) FROM information_schema.columns WHERE table_schema = %s AND table_name = %s"
                connection.commit()
                # Указание имени базы данных и таблицы
                database_name = db_name
                table_name = 'Category'
                # Выполнение запроса с передачей параметров
                cursor.execute(sql_query, (database_name, table_name))
                # Получение результата запроса
                row_index = cursor.fetchone()
                row_index = row_index['COUNT(*)']
                row_index -= 1
                print(row_index)
        finally:
            # Закрытие соединения
            None

        try:
            with connection.cursor() as cursor:
                # SQL-запрос для выборки всех записей из таблицы
                sql_query = "SELECT * FROM Category"
                connection.commit()
                # Выполнение запроса
                cursor.execute(sql_query)
                # Извлечение всех записей из результата запроса в виде списка словарей
                categorys = []
                # Получение имен столбцов, начиная с первого столбца
                columns = [column[0] for column in cursor.description[1:]]
                print(columns)

                # SQL-запрос для подсчета всех записей из таблицы
                sql_query2 = "SELECT COUNT(*) FROM Category;"
                connection.commit()
                # Выполнение запроса
                cursor.execute(sql_query2)
                str_num = cursor.fetchone()
                str_num = str_num['COUNT(*)']
                print(str_num)

                # Перебор записей и добавление их в список в виде словарей
                # for row in cursor.fetchall():
                #     user = {}
                #     for i in range(len(columns)):
                #         # Используйте .get() для избежания ошибки KeyError и обработки None значений
                #         column_name = columns[i]
                #         column_value = row[i]
                #         user[column_name] = column_value if column_value is not None else None
                #     users.append(user)

                for i in range(str_num):
                    category = {}
                    for column in columns:
                        sql_query3 = f"SELECT {column} FROM Category WHERE ID_Category = {i + 1};"
                        cursor.execute(sql_query3)
                        result = cursor.fetchone()  # Получаем одну строку из результата запроса
                        if result:
                            print(result)
                            category[column] = result[column]  # Первый элемент кортежа - это значение столбца
                        else:
                            category[column] = None
                    categorys.append(category)

                # Теперь переменная entities содержит все сущности из вашей таблицы в виде списка словарей
                print(categorys)
        finally:
            # Закрытие соединения
            # connection.close()
            None

        # tableWidget - название поля
        self.categorysTableWidget.setRowCount(str_num)  # Кол-во строк
        self.categorysTableWidget.setColumnCount(row_index)  # Кол-во столбцов

        # Заголовки столбцов
        self.categorysTableWidget.setHorizontalHeaderLabels(['Название', 'Возрастное ограничение'])

        # Ширина столбцов (индекс, ширина)
        for i in range(row_index):
            self.categorysTableWidget.setColumnWidth(i, 350)

        # Заполнение QtTableWidget
        for row_index, row_data in enumerate(categorys):
            for column_index, data in enumerate(row_data.values()):
                item = QTableWidgetItem(str(data))
                self.categorysTableWidget.setItem(row_index, column_index, item)











#------------------------ Роли --------------------------------

    # Функция вывода ролей в TableWidget
    def loadRoles(self):

        try:
            with connection.cursor() as cursor:
                # SQL-запрос для подсчета количества столбцов в таблице
                sql_query = "SELECT COUNT(*) FROM information_schema.columns WHERE table_schema = %s AND table_name = %s"
                connection.commit()
                # Указание имени базы данных и таблицы
                database_name = db_name
                table_name = 'Role'
                # Выполнение запроса с передачей параметров
                cursor.execute(sql_query, (database_name, table_name))
                # Получение результата запроса
                row_index = cursor.fetchone()
                row_index = row_index['COUNT(*)']
                row_index -= 1
                print(row_index)
        finally:
            # Закрытие соединения
            None

        try:
            with connection.cursor() as cursor:
                # SQL-запрос для выборки всех записей из таблицы
                sql_query = "SELECT * FROM Role"
                connection.commit()
                # Выполнение запроса
                cursor.execute(sql_query)
                # Извлечение всех записей из результата запроса в виде списка словарей
                roles = []
                # Получение имен столбцов, начиная с первого столбца
                columns = [column[0] for column in cursor.description[1:]]
                print(columns)

                # SQL-запрос для подсчета всех записей из таблицы
                sql_query2 = "SELECT COUNT(*) FROM Role;"
                connection.commit()
                # Выполнение запроса
                cursor.execute(sql_query2)
                str_num = cursor.fetchone()
                str_num = str_num['COUNT(*)']
                print(str_num)



                for i in range(str_num):
                    role = {}
                    for column in columns:
                        sql_query3 = f"SELECT {column} FROM Role WHERE ID_Role = {i + 1};"
                        cursor.execute(sql_query3)
                        result = cursor.fetchone()  # Получаем одну строку из результата запроса
                        if result:
                            print(result)
                            role[column] = result[column]  # Первый элемент кортежа - это значение столбца
                        else:
                            role[column] = None
                    roles.append(role)

                # Теперь переменная entities содержит все сущности из вашей таблицы в виде списка словарей
                print(roles)
        finally:
            # Закрытие соединения
            # connection.close()
            None

        # tableWidget - название поля
        self.rolesTableWidget.setRowCount(str_num)  # Кол-во строк
        self.rolesTableWidget.setColumnCount(row_index)  # Кол-во столбцов

        # Заголовки столбцов
        self.rolesTableWidget.setHorizontalHeaderLabels(['Название'])

        # Ширина столбцов (индекс, ширина)
        for i in range(row_index):
            self.rolesTableWidget.setColumnWidth(i, 350)

        # Заполнение QtTableWidget
        for row_index, row_data in enumerate(roles):
            for column_index, data in enumerate(row_data.values()):
                item = QTableWidgetItem(str(data))
                self.rolesTableWidget.setItem(row_index, column_index, item)










#------------------------ Льготы --------------------------------

    # Функция вывода льгот в TableWidget
    def loadBenefits(self):

        try:
            with connection.cursor() as cursor:
                # SQL-запрос для подсчета количества столбцов в таблице
                sql_query = "SELECT COUNT(*) FROM information_schema.columns WHERE table_schema = %s AND table_name = %s"
                connection.commit()
                # Указание имени базы данных и таблицы
                database_name = db_name
                table_name = 'Benefit'
                # Выполнение запроса с передачей параметров
                cursor.execute(sql_query, (database_name, table_name))
                # Получение результата запроса
                row_index = cursor.fetchone()
                row_index = row_index['COUNT(*)']
                row_index -= 1
                print(row_index)
        finally:
            # Закрытие соединения
            None

        try:
            with connection.cursor() as cursor:
                # SQL-запрос для выборки всех записей из таблицы
                sql_query = "SELECT * FROM Benefit"
                connection.commit()
                # Выполнение запроса
                cursor.execute(sql_query)
                # Извлечение всех записей из результата запроса в виде списка словарей
                benefits = []
                # Получение имен столбцов, начиная с первого столбца
                columns = [column[0] for column in cursor.description[1:]]
                print(columns)

                # SQL-запрос для подсчета всех записей из таблицы
                sql_query2 = "SELECT COUNT(*) FROM Benefit;"
                connection.commit()
                # Выполнение запроса
                cursor.execute(sql_query2)
                str_num = cursor.fetchone()
                str_num = str_num['COUNT(*)']
                print(str_num)


                for i in range(str_num):
                    benefit = {}
                    for column in columns:
                        sql_query3 = f"SELECT {column} FROM Benefit WHERE ID_Benefit = {i + 1};"
                        cursor.execute(sql_query3)
                        result = cursor.fetchone()  # Получаем одну строку из результата запроса
                        if result:
                            print(result)
                            benefit[column] = result[column]  # Первый элемент кортежа - это значение столбца
                        else:
                            benefit[column] = None
                    benefits.append(benefit)

                # Теперь переменная entities содержит все сущности из вашей таблицы в виде списка словарей
                print(benefits)
        finally:
            # Закрытие соединения
            # connection.close()
            None

        # tableWidget - название поля
        self.benefitsTableWidget.setRowCount(str_num)  # Кол-во строк
        self.benefitsTableWidget.setColumnCount(row_index)  # Кол-во столбцов

        # Заголовки столбцов
        self.benefitsTableWidget.setHorizontalHeaderLabels(['Название', 'Размер скидки'])

        # Ширина столбцов (индекс, ширина)
        for i in range(row_index):
            self.benefitsTableWidget.setColumnWidth(i, 350)

        # Заполнение QtTableWidget
        for row_index, row_data in enumerate(benefits):
            for column_index, data in enumerate(row_data.values()):
                item = QTableWidgetItem(str(data))
                self.benefitsTableWidget.setItem(row_index, column_index, item)











#------------------------ Поставщики --------------------------------

    # Функция вывода поставщиков в TableWidget
    def loadSuppliers(self):

        try:
            with connection.cursor() as cursor:
                # SQL-запрос для подсчета количества столбцов в таблице
                sql_query = "SELECT COUNT(*) FROM information_schema.columns WHERE table_schema = %s AND table_name = %s"
                connection.commit()
                # Указание имени базы данных и таблицы
                database_name = db_name
                table_name = 'Supplier'
                # Выполнение запроса с передачей параметров
                cursor.execute(sql_query, (database_name, table_name))
                # Получение результата запроса
                row_index = cursor.fetchone()
                row_index = row_index['COUNT(*)']
                row_index -= 1
                print(row_index)
        finally:
            # Закрытие соединения
            None

        try:
            with connection.cursor() as cursor:
                # SQL-запрос для выборки всех записей из таблицы
                sql_query = "SELECT * FROM Supplier"
                connection.commit()
                # Выполнение запроса
                cursor.execute(sql_query)
                # Извлечение всех записей из результата запроса в виде списка словарей
                suppliers = []
                # Получение имен столбцов, начиная с первого столбца
                columns = [column[0] for column in cursor.description[1:]]
                print(columns)

                # SQL-запрос для подсчета всех записей из таблицы
                sql_query2 = "SELECT COUNT(*) FROM Supplier;"
                connection.commit()
                # Выполнение запроса
                cursor.execute(sql_query2)
                str_num = cursor.fetchone()
                str_num = str_num['COUNT(*)']
                print(str_num)


                for i in range(str_num):
                    supplier = {}
                    for column in columns:
                        sql_query3 = f"SELECT {column} FROM Supplier WHERE ID_Supplier = {i + 1};"
                        cursor.execute(sql_query3)
                        result = cursor.fetchone()  # Получаем одну строку из результата запроса
                        if result:
                            print(result)
                            supplier[column] = result[column]  # Первый элемент кортежа - это значение столбца
                        else:
                            supplier[column] = None
                    suppliers.append(supplier)

                # Теперь переменная entities содержит все сущности из вашей таблицы в виде списка словарей
                print(suppliers)
        finally:
            # Закрытие соединения
            # connection.close()
            None

        # tableWidget - название поля
        self.suppliersTableWidget.setRowCount(str_num)  # Кол-во строк
        self.suppliersTableWidget.setColumnCount(row_index)  # Кол-во столбцов

        # Заголовки столбцов
        self.suppliersTableWidget.setHorizontalHeaderLabels(['Название', 'Код пользователя'])

        # Ширина столбцов (индекс, ширина)
        for i in range(row_index):
            self.suppliersTableWidget.setColumnWidth(i, 350)

        # Заполнение QtTableWidget
        for row_index, row_data in enumerate(suppliers):
            for column_index, data in enumerate(row_data.values()):
                item = QTableWidgetItem(str(data))
                self.suppliersTableWidget.setItem(row_index, column_index, item)











#------------------------ Товары --------------------------------

    # Функция вывода поставщиков в TableWidget
    def loadProducts(self):

        try:
            with connection.cursor() as cursor:
                # SQL-запрос для подсчета количества столбцов в таблице
                sql_query = "SELECT COUNT(*) FROM information_schema.columns WHERE table_schema = %s AND table_name = %s"
                connection.commit()
                # Указание имени базы данных и таблицы
                database_name = db_name
                table_name = 'Product'
                # Выполнение запроса с передачей параметров
                cursor.execute(sql_query, (database_name, table_name))
                # Получение результата запроса
                row_index = cursor.fetchone()
                row_index = row_index['COUNT(*)']
                row_index -= 1
                print(row_index)
        finally:
            # Закрытие соединения
            None

        try:
            with connection.cursor() as cursor:
                # SQL-запрос для выборки всех записей из таблицы
                sql_query = "SELECT * FROM Product"
                connection.commit()
                # Выполнение запроса
                cursor.execute(sql_query)
                # Извлечение всех записей из результата запроса в виде списка словарей
                products = []
                # Получение имен столбцов, начиная с первого столбца
                columns = [column[0] for column in cursor.description[1:]]
                print(columns)

                # SQL-запрос для подсчета всех записей из таблицы
                sql_query2 = "SELECT COUNT(*) FROM Product;"
                connection.commit()
                # Выполнение запроса
                cursor.execute(sql_query2)
                str_num = cursor.fetchone()
                str_num = str_num['COUNT(*)']
                print(str_num)


                for i in range(str_num):
                    product = {}
                    for column in columns:
                        sql_query3 = f"SELECT {column} FROM Product WHERE ID_Product = {i + 1};"
                        cursor.execute(sql_query3)
                        result = cursor.fetchone()  # Получаем одну строку из результата запроса
                        if result:
                            print(result)
                            product[column] = result[column]  # Первый элемент кортежа - это значение столбца
                        else:
                            product[column] = None
                    products.append(product)

                # Теперь переменная entities содержит все сущности из вашей таблицы в виде списка словарей
                print(products)
        finally:
            # Закрытие соединения
            # connection.close()
            None

        # tableWidget - название поля
        self.productsTableWidget.setRowCount(str_num)  # Кол-во строк
        self.productsTableWidget.setColumnCount(row_index)  # Кол-во столбцов

        # Заголовки столбцов
        self.productsTableWidget.setHorizontalHeaderLabels(['Название', 'Описание', 'Код категории', 'Код поставщика'])

        # Ширина столбцов (индекс, ширина)
        for i in range(row_index):
            self.productsTableWidget.setColumnWidth(i, 180)

        # Заполнение QtTableWidget
        for row_index, row_data in enumerate(products):
            for column_index, data in enumerate(row_data.values()):
                item = QTableWidgetItem(str(data))
                self.productsTableWidget.setItem(row_index, column_index, item)










#------------------------ Отзывы --------------------------------

    # Функция вывода отзывов в TableWidget
    def loadFeedbacks(self):

        try:
            with connection.cursor() as cursor:
                # SQL-запрос для подсчета количества столбцов в таблице
                sql_query = "SELECT COUNT(*) FROM information_schema.columns WHERE table_schema = %s AND table_name = %s"
                connection.commit()
                # Указание имени базы данных и таблицы
                database_name = db_name
                table_name = 'Feedback'
                # Выполнение запроса с передачей параметров
                cursor.execute(sql_query, (database_name, table_name))
                # Получение результата запроса
                row_index = cursor.fetchone()
                row_index = row_index['COUNT(*)']
                row_index -= 1
                print(row_index)
        finally:
            # Закрытие соединения
            None

        try:
            with connection.cursor() as cursor:
                # SQL-запрос для выборки всех записей из таблицы
                sql_query = "SELECT * FROM Feedback"
                connection.commit()
                # Выполнение запроса
                cursor.execute(sql_query)
                # Извлечение всех записей из результата запроса в виде списка словарей
                feedbacks = []
                # Получение имен столбцов, начиная с первого столбца
                columns = [column[0] for column in cursor.description[1:]]
                print(columns)

                # SQL-запрос для подсчета всех записей из таблицы
                sql_query2 = "SELECT COUNT(*) FROM Feedback;"
                connection.commit()
                # Выполнение запроса
                cursor.execute(sql_query2)
                str_num = cursor.fetchone()
                str_num = str_num['COUNT(*)']
                print(str_num)


                for i in range(str_num):
                    feedback = {}
                    for column in columns:
                        sql_query3 = f"SELECT {column} FROM Feedback WHERE ID_Feedback = {i + 1};"
                        cursor.execute(sql_query3)
                        result = cursor.fetchone()  # Получаем одну строку из результата запроса
                        if result:
                            print(result)
                            feedback[column] = result[column]  # Первый элемент кортежа - это значение столбца
                        else:
                            feedback[column] = None
                    feedbacks.append(feedback)

                # Теперь переменная entities содержит все сущности из вашей таблицы в виде списка словарей
                print(feedbacks)
        finally:
            # Закрытие соединения
            # connection.close()
            None

        # tableWidget - название поля
        self.feedbacksTableWidget.setRowCount(str_num)  # Кол-во строк
        self.feedbacksTableWidget.setColumnCount(row_index)  # Кол-во столбцов

        # Заголовки столбцов
        self.feedbacksTableWidget.setHorizontalHeaderLabels(['Текст', 'Код пользователя', 'Код товара'])

        # Ширина столбцов (индекс, ширина)
        for i in range(row_index):
            self.feedbacksTableWidget.setColumnWidth(i, 230)

        # Заполнение QtTableWidget
        for row_index, row_data in enumerate(feedbacks):
            for column_index, data in enumerate(row_data.values()):
                item = QTableWidgetItem(str(data))
                self.feedbacksTableWidget.setItem(row_index, column_index, item)










#------------------------ Заказы --------------------------------

    # Функция вывода заказов в TableWidget
    def loadOrders(self):

        try:
            with connection.cursor() as cursor:
                # SQL-запрос для подсчета количества столбцов в таблице
                sql_query = "SELECT COUNT(*) FROM information_schema.columns WHERE table_schema = %s AND table_name = %s"
                connection.commit()
                # Указание имени базы данных и таблицы
                database_name = db_name
                table_name = 'Ordering'
                # Выполнение запроса с передачей параметров
                cursor.execute(sql_query, (database_name, table_name))
                # Получение результата запроса
                row_index = cursor.fetchone()
                row_index = row_index['COUNT(*)']
                row_index -= 1
                print(row_index)
        finally:
            # Закрытие соединения
            None

        try:
            with connection.cursor() as cursor:
                # SQL-запрос для выборки всех записей из таблицы
                sql_query = "SELECT * FROM Ordering"
                connection.commit()
                # Выполнение запроса
                cursor.execute(sql_query)
                # Извлечение всех записей из результата запроса в виде списка словарей
                orders = []
                # Получение имен столбцов, начиная с первого столбца
                columns = [column[0] for column in cursor.description[1:]]
                print(columns)

                # SQL-запрос для подсчета всех записей из таблицы
                sql_query2 = "SELECT COUNT(*) FROM Ordering;"
                connection.commit()
                # Выполнение запроса
                cursor.execute(sql_query2)
                str_num = cursor.fetchone()
                str_num = str_num['COUNT(*)']
                print(str_num)


                for i in range(str_num):
                    order = {}
                    for column in columns:
                        sql_query3 = f"SELECT {column} FROM Ordering WHERE ID_Ordering = {i + 1};"
                        cursor.execute(sql_query3)
                        result = cursor.fetchone()  # Получаем одну строку из результата запроса
                        if result:
                            print(result)
                            order[column] = result[column]  # Первый элемент кортежа - это значение столбца
                        else:
                            order[column] = None
                    orders.append(order)

                # Теперь переменная entities содержит все сущности из вашей таблицы в виде списка словарей
                print(orders)
        finally:
            # Закрытие соединения
            # connection.close()
            None

        # tableWidget - название поля
        self.ordersTableWidget.setRowCount(str_num)  # Кол-во строк
        self.ordersTableWidget.setColumnCount(row_index)  # Кол-во столбцов

        # Заголовки столбцов
        self.ordersTableWidget.setHorizontalHeaderLabels(['Номер', 'Итоговая стоимость', 'Код пользователя', 'Код товара'])

        # Ширина столбцов (индекс, ширина)
        for i in range(row_index):
            self.ordersTableWidget.setColumnWidth(i, 180)

        # Заполнение QtTableWidget
        for row_index, row_data in enumerate(orders):
            for column_index, data in enumerate(row_data.values()):
                item = QTableWidgetItem(str(data))
                self.ordersTableWidget.setItem(row_index, column_index, item)














if __name__ == "__main__":
    app = QApplication([])
    connection = pymysql.connect(
        host=host,
        user=user,
        password=password,
        database=db_name,
        cursorclass=pymysql.cursors.DictCursor
    )
    cursor = connection.cursor()
    cursor.execute("SET SESSION TRANSACTION ISOLATION LEVEL READ COMMITTED")
    window = MainWindow()
    window.show()
    app.exec()








#----------------------------------------------------




# class ExpenseTracker(QMainWindow):
#     def __init__(self):
#         super(ExpenseTracker, self).__init__()
#         self.ui = Ui_MainWindow()
#         self.ui.setupUi(self)
#
#
# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = ExpenseTracker()
#     window.show()
#     sys.exit(app.exec())















