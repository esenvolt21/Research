from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import Qt
from enum import Enum

import main_app
import csv
import math
import os


class ErrorCodes(Enum):
    ERROR_STR_ARRAY = 0,
    ERROR_TYPE_HISTOGRAM = 1,
    ERROR_STR_HISTOGRAM = 2,
    ERROR_ELEMENT_COUNT = 3,
    ERROR_NOT_NUMERIC = 4,
    ERROR_DISPERSION_ZERO = 5,
    ERROR_UNDER_ROOT_NEGATIVE = 6,
    ERROR_Q_ZERO = 7,
    ERROR_Q_ECCENTRICITY = 8,
    ERROR_PROBABILITY_NOT_1 = 9,
    ERROR_MULTIPLE_ELEMENTS = 10,
    ERROR_TABLE_NOT_LOADED = 11,
    ERROR_FILE_NOT_LOADED = 12,
    ERROR_INVALID_FILE_FORMAT = 13,
    ERROR_EMPTY_FILE = 14,
    ERROR_NO_LINE_SELECTED = 15


class ResearchCalcErrors(Exception):
    pass


class ResearchAppErrors(Exception):
    pass


class ResearchCalc:
    """ Вычисление трехточки """
    def __init__(self):
        super(ResearchCalc, self).__init__()

    @staticmethod
    def calc_semi(data_array: list):
        """
        Вычисление четырех первых семиинвариантов для массива данных.

        :param data_array: Входной массив данных.
        :return: Массив из 5-ти элементов.
        """
        exit_code = None
        try:
            if not all(isinstance(x, (int, float, list)) for x in data_array):
                exit_code = ErrorCodes.ERROR_STR_ARRAY
                raise ResearchCalcErrors("Среди элементов массива присутсвуют строки. "
                                         "Необходимо изменить входные данные на целые числа или числа с плавающей точкой.")

            m1, m2, m3, m4 = 0, 0, 0, 0
            size = 0
            for item in data_array:
                # Гистограмма
                if isinstance(item, list):
                    if len(item) != 2:
                        exit_code = ErrorCodes.ERROR_TYPE_HISTOGRAM
                        raise ResearchCalcErrors("Гистограмма задана неверно - ожидаемый вид [{число, кол-во}, ..., {число, кол-во}]")

                    if len(item) == 2:
                        for i in range(len(data_array)):
                            if not all(isinstance(x, (int, float)) for x in data_array[i]):
                                exit_code = ErrorCodes.ERROR_STR_HISTOGRAM
                                raise ResearchCalcErrors("Среди элементов списка присутсвуют строки. "
                                                         "Необходимо изменить входные данные на целые числа или числа с плавающей точкой.")

                    size += item[1]
                    m1 += item[1] * item[0]
                    m2 += item[1] * item[0] ** 2
                    m3 += item[1] * item[0] ** 3
                    m4 += item[1] * item[0] ** 4
                # Массив
                elif isinstance(item, float) or isinstance(item, int):
                    size = len(data_array)
                    m1 += item
                    m2 += item ** 2
                    m3 += item ** 3
                    m4 += item ** 4

            # Вычисление моментов.
            m1 /= size
            m2 /= size
            m3 /= size
            m4 /= size

            # Вычисление семиинвариантов.
            s1 = m1
            s2 = m2 - m1 ** 2
            s3 = m3 - 3 * m1 * m2 + 2 * m1 ** 3
            s4 = m4 - 4 * m1 * m3 - 3 * m2 ** 2 + 12 * m1 ** 2 * m2 - 6 * m1 ** 4
            return [s1, s2, s3, s4, size]
        except ResearchCalcErrors as e:
            print(e)
            return exit_code

    @staticmethod
    def calc_three_points(semi_list: list):
        """
        Вычисление трехточки.

        :param semi_list: Массив с семиинвариантами.
        :return: Среднее минимальное, среднее максимальное, среднее среднее.
        """
        exit_code = None
        try:
            if not len(semi_list) == 5:
                exit_code = ErrorCodes.ERROR_ELEMENT_COUNT
                raise ResearchCalcErrors("Количество элементов входного массива != 5.")

            if not all(isinstance(x, (int, float)) for x in semi_list):
                exit_code = ErrorCodes.ERROR_NOT_NUMERIC
                raise ResearchCalcErrors("В списке присутствуют не числа.")

            xs = semi_list[0]
            dd = semi_list[1]

            if dd == 0:
                exit_code = ErrorCodes.ERROR_DISPERSION_ZERO
                raise ResearchCalcErrors("Дисперсия равна 0 - дальнейшие вычисления невозможны.")

            aa = semi_list[2] / dd / 2.
            ee = semi_list[3]
            ss = math.sqrt(dd)

            first = ee / (dd ** 2)
            second = (3. * (aa ** 2)) / dd
            under_root = 3 + first - second

            if under_root < 0:
                exit_code = ErrorCodes.ERROR_UNDER_ROOT_NEGATIVE
                raise ResearchCalcErrors("Подкоренное значение для q отрицательно - дальнейшие вычисления невозможны.")

            qq = math.sqrt(under_root)

            if qq == 0:
                exit_code = ErrorCodes.ERROR_Q_ZERO
                raise ResearchCalcErrors("Вспомогательная величина q = 0 - дальнейшие вычисления невозможны.")
            if (qq - aa) == 0 or (qq + aa) == 0:
                exit_code = ErrorCodes.ERROR_Q_ECCENTRICITY
                raise ResearchCalcErrors("Вспомогательная величина (q ± A) = 0 - дальнейшие вычисления невозможны.")

            x1, x2 = -ss * qq + xs + aa, ss * qq + xs + aa
            p1, p2 = ss / (2. * qq * (ss * qq - aa)), ss / (2. * qq * (ss * qq + aa))
            p3 = 1 - p1 - p2

            if (p1 + p2 + p3) != 1:
                exit_code = ErrorCodes.ERROR_PROBABILITY_NOT_1
                raise ResearchCalcErrors("Сумма вероятностей не равна 1.")

            return [[x1, p1], [xs, p3], [x2, p2]]
        except ResearchCalcErrors as e:
            print(e)
            return exit_code


class ResearchSignals(QtCore.QObject):
    """ Сигналы для основного приложения """
    delete_rows = QtCore.pyqtSignal(int, int)


class ResearchApp(QtWidgets.QMainWindow, main_app.Ui_MainWindow):
    """ Класс-реализация окна исследования """

    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.setupUi(self)
        self.filedialog_path = '../resources'

        # Обработчики кнопок.
        self.AddButton.clicked.connect(self.add_button_logic)
        self.DownloadButton.clicked.connect(self.load_button_logic)
        self.DeleteButton.clicked.connect(self.delete_button_logic)
        self.SaveButton.clicked.connect(self.save_button_logic)
        self.PointButton.clicked.connect(self.calc_point_logic)
        self.CloseButton.clicked.connect(self.close_logic)

        # Поля.
        self.ValueAvgEdit.setPlaceholderText("Результат среднего")
        self.ValueMaxEdit.setPlaceholderText("Результат максимального")
        self.ValueMinEdit.setPlaceholderText("Результат минимального")
        self.propertylineEdit.setPlaceholderText("Выберите свойство для расчета")

        # Таблица.
        self.table_model = QtGui.QStandardItemModel()
        self.tableView.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        self.tableView.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.SingleSelection)
        self.tableView.setModel(self.table_model)

        # Объект управления сигналами.
        self.win_manager = ResearchSignals()
        self.win_manager.delete_rows.connect(self.delete_rows_logic)

        # Объект расчетов.
        self.calculator = ResearchCalc()

        # Словарь для свойств.
        self.properties_indexes = {}

    def contextMenuEvent(self, event):
        """
        Создание контекстного меню для QTableView.

        :param event: Событие.
        :return: None
        """
        self.context_menu = QtWidgets.QMenu(self)

        upper_property = QtWidgets.QAction('Больше или равно', self)
        upper_property.triggered.connect(self.upper_property)
        equal_property = QtWidgets.QAction('Равно', self)
        equal_property.triggered.connect(self.equal_property)
        lower_property = QtWidgets.QAction('Меньше или равно', self)
        lower_property.triggered.connect(self.lower_property)
        add_as_property = QtWidgets.QAction('Выбрать как свойство', self)
        add_as_property.triggered.connect(self.add_as_property)

        self.context_menu.addAction(upper_property)
        self.context_menu.addAction(equal_property)
        self.context_menu.addAction(lower_property)
        self.context_menu.addAction(add_as_property)

        indexes = self.tableView.selectionModel().selectedIndexes()
        is_digit = False
        is_letter = False
        for idx in indexes:
            if str(idx.data()).isdigit():
                is_digit = True
            else:
                is_letter = True

        if not is_digit:
            lower_property.setEnabled(False)
            upper_property.setEnabled(False)
            equal_property.setEnabled(False)

        if not is_letter:
            add_as_property.setEnabled(False)

        self.context_menu.popup(QtGui.QCursor.pos())

    def getting_headers(self):
        """
        Получение заголовков

        :return: list
        """
        # Получение заголовков.
        headers = []
        for clm in range(self.tableView.model().columnCount()):
            headers.append(self.tableView.model().headerData(clm, QtCore.Qt.Orientation.Horizontal))

        return headers

    def equal_property(self):
        """
        Рассчитать для значений "равно"...

        :return:
        """
        self.add_as_property("=")

    def upper_property(self):
        """
        Рассчитать для значений больше, чем...

        :return: None
        """
        self.add_as_property(">=")

    def lower_property(self):
        """
        Рассчитать для значений меньше, чем...

        :return: None
        """
        self.add_as_property("<=")

    def add_as_property(self, prop: str = ""):
        """
        Добавление элемента как свойство для расчета.

        :param prop: Свойство.
        :return: None
        """
        self.propertylineEdit.clear()
        self.properties_indexes.clear()

        indexes = self.tableView.selectionModel().selectedIndexes()
        if len(indexes) != 1:
            exit_code = ErrorCodes.ERROR_MULTIPLE_ELEMENTS
            raise ResearchAppErrors("Выделено несколько элементов...")

        # Получение заголовков.
        headers = self.getting_headers()

        # Выбранный элемент.
        item = indexes[-1].data()

        # Добавленное свойство.
        added_prop_view = str(headers[indexes[-1].column()])
        added_prop = ""
        # Проверка на числовое значение.
        if str(item).isdigit():
            # Добавление символа перед свойством.
            if prop:
                added_prop += str(prop)
                # Отображение текста в поле.
                self.propertylineEdit.insert(str(prop))
        else:
            added_prop += item

        # Отображение текста в поле.
        self.propertylineEdit.insert(item)
        self.propertylineEdit.setAlignment(Qt.AlignCenter)
        self.propertylineEdit.setStyleSheet("border-radius: 20px;\n"
                                            "background-color: rgba(255, 255, 255,0);\n"
                                            "font: 12pt \"Century Gothic\";\n"
                                            )
        # Добавление свойства в словарь: (Строка, Столбец): Свойство.
        self.properties_indexes[(indexes[-1].row(), indexes[-1].column())] = added_prop

    @QtCore.pyqtSlot(int, int)
    def delete_rows_logic(self, row_number: int, rows_count: int):
        """
        Слот для удаления строк таблицы.

        :param row_number: Номер удаляемой строки.
        :param rows_count: Количество строк.
        :return: None
        """
        self.tableView.model().removeRows(row_number, rows_count)

    def find_replace_comma(self) -> bool:
        """
        Функция поиска и замены запятых в ячейках таблицы.

        :return: Если есть запятые и произведена замена - true, иначе - false.
        """
        bool_flag = False
        model = self.tableView.model()
        for row in range(model.rowCount()):
            for column in range(model.columnCount()):
                index = model.index(row, column)
                datas = index.data()
                data_help = datas.replace(",", ";")

                if datas != data_help:
                    datas = data_help
                    bool_flag = True

        return bool_flag

    def add_button_logic(self):
        """
        Обработчик нажатия на кнопку "Добавить".

        :return: None
        """
        exit_code = None
        try:
            if not self.tableView.model().columnCount() > 0:
                exit_code = ErrorCodes.ERROR_TABLE_NOT_LOADED
                raise ResearchAppErrors("Таблица не загружена, добавление строк невозможно.")
            self.tableView.model().insertRow(self.tableView.model().rowCount(QtCore.QModelIndex()))
        except ResearchAppErrors as e:
            print(e)
            return exit_code

    def load_button_logic(self):
        """
        Обработчик нажатия на кнопку "Загрузить".

        :return: None
        """
        exit_code = None
        try:
            dialog_name = "Загрузка данных"
            options = QtWidgets.QFileDialog.Options()
            filename, _ = QtWidgets.QFileDialog.getOpenFileName(self, dialog_name, self.filedialog_path,
                                                                "All types of docs (*.csv)", options=options)

            if not filename:
                exit_code = ErrorCodes.ERROR_FILE_NOT_LOADED
                raise ResearchAppErrors("Файл не загружен.")

            _, file_extension = os.path.splitext(filename)

            if file_extension != '.csv':
                exit_code = ErrorCodes.ERROR_INVALID_FILE_FORMAT
                raise ResearchAppErrors("Загружен файл неверного формата.")

            if os.stat(filename).st_size == 0:
                exit_code = ErrorCodes.ERROR_EMPTY_FILE
                raise ResearchAppErrors("Загружен пустой файл - работа с ним невозможна.")

            self.table_model.clear()
            with open(filename, newline='') as File:
                reader = csv.reader(File)
                for i, row in enumerate(reader):
                    if i == 0:
                        # Добавление названий колонок.
                        self.table_model.setHorizontalHeaderLabels(row)
                    else:
                        # Добавление строк данных.
                        items = []
                        for field in row:
                            items.append(QtGui.QStandardItem(field.strip()))
                        self.table_model.appendRow(items)
                self.tableView.setModel(self.table_model)
            self.tableView.setStyleSheet("border-radius: 20px;\n"
                                         "background-color: rgb(255, 255, 255);\n"
                                         "font: 10pt \"Century Gothic\";")
        except ResearchAppErrors as e:
            print(e)
            return exit_code

    def delete_button_logic(self):
        """
        Обработчик нажатия на кнопку "Удалить".

        :return: None
        """
        exit_code = None
        try:
            if not self.tableView.model().columnCount() > 0:
                exit_code = ErrorCodes.ERROR_TABLE_NOT_LOADED
                raise ResearchAppErrors("Таблица не загружена, удаление строк невозможно.")

            rows = self.tableView.selectionModel().selectedIndexes()

            if not rows:
                exit_code = ErrorCodes.ERROR_NO_LINE_SELECTED
                raise ResearchAppErrors("Не выбрана строка для удаления.")

            for row in rows:
                self.win_manager.delete_rows.emit(row.row(), len(rows))
        except ResearchAppErrors as e:
            print(e)
            return exit_code

    def save_button_logic(self):
        """
        Обработчик нажатия на кнопку "Сохранить".

        :return: None
        """
        exit_code = None
        try:
            if not self.tableView.model().columnCount() > 0:
                exit_code = ErrorCodes.ERROR_TABLE_NOT_LOADED
                raise ResearchAppErrors("Таблица не загружена и не создана - ее сохранение невозможно.")

            dialog_name = "Сохранение данных"
            options = QtWidgets.QFileDialog.Options()
            filename, _ = QtWidgets.QFileDialog.getSaveFileName(self, dialog_name, self.filedialog_path,
                                                                "All types of docs (*.csv)", options=options)

            if filename:
                if self.find_replace_comma():
                    print('Произведена замена запятых при сохранении.')

                with open(filename, 'w', newline='') as File:
                    writer = csv.writer(File)
                    headers = []
                    for clm in range(self.tableView.model().columnCount()):
                        headers.append(self.tableView.model().headerData(clm, QtCore.Qt.Orientation.Horizontal))

                    # Запись заголовков.
                    writer.writerow(headers)

                    model = self.tableView.model()
                    for row in range(model.rowCount()):
                        row_data = []
                        for column in range(model.columnCount()):
                            index = model.index(row, column)
                            row_data.append(model.data(index))
                        writer.writerow(row_data)
        except ResearchAppErrors as e:
            print(e)
            return exit_code

    def calc_point_logic(self):
        """
        Обработчик нажатия на кнопку "Рассчитать".

        :return: None
        """
        # Нужные строки, подходящие под свойства.
        correct_rows = []
        correct_wage = []

        # Получение заголовков.
        headers = self.getting_headers()

        # Варианты названия колонки с ЗП.
        wage_column_names = ["ЗП", "Заработная плата", "Зарплата"]

        # Получения номера колонки с ЗП.
        wage_col = None
        for name in wage_column_names:
            if name in headers:
                wage_col = headers.index(name)

        # Анализ столбца, указанного в свойстве.
        prop_idx = list(self.properties_indexes.keys())[0]
        prop_item = self.tableView.model().data(self.tableView.model().index(prop_idx[0], prop_idx[1]))
        for row in range(self.tableView.model().rowCount()):
            item = self.tableView.model().data(self.tableView.model().index(row, prop_idx[1]))
            # Обработка числовых значений.
            if str(item).isdigit():
                operation = list(self.properties_indexes.values())[0]
                if operation == ">=":
                    if int(item) >= int(prop_item):
                        correct_rows.append(row)
                        wage = self.tableView.model().data(self.tableView.model().index(row, wage_col))
                        if str(wage).isdigit():
                            correct_wage.append(float(wage))
                elif operation == "<=":
                    if int(item) <= int(prop_item):
                        correct_rows.append(row)
                        wage = self.tableView.model().data(self.tableView.model().index(row, wage_col))
                        if str(wage).isdigit():
                            correct_wage.append(float(wage))
                else:
                    if int(item) == int(prop_item):
                        correct_rows.append(row)
                        wage = self.tableView.model().data(self.tableView.model().index(row, wage_col))
                        if str(wage).isdigit():
                            correct_wage.append(float(wage))
            else:
                if item == prop_item:
                    correct_rows.append(row)
                    wage = self.tableView.model().data(self.tableView.model().index(row, wage_col))
                    if str(wage).isdigit():
                        correct_wage.append(float(wage))

        correct_wage = [[2, 0], [3, 5], [4, 14], [5, 6]]

        # Вычисление трехточки.
        semi = self.calculator.calc_semi(correct_wage)
        three_points = self.calculator.calc_three_points(semi)

        # Вывод информации в поля.
        float_precision = '.2f'
        avg_minimal = "[" + str(format(three_points[0][0], float_precision)) + \
                      ", " + str(format(three_points[0][1], float_precision)) + "]"
        self.ValueMinEdit.setText(avg_minimal)

        avg_middle = "[" + str(format(three_points[1][0], float_precision)) + \
                     ", " + str(format(three_points[1][1], float_precision)) + "]"
        self.ValueAvgEdit.setText(avg_middle)

        avg_maximal = "[" + str(format(three_points[2][0], float_precision)) + \
                      ", " + str(format(three_points[2][1], float_precision)) + "]"
        self.ValueMaxEdit.setText(avg_maximal)
        self.ValueMinEdit.setAlignment(Qt.AlignCenter)
        self.ValueMinEdit.setStyleSheet("border-radius: 20px;\n"
                                            "background-color: rgba(255, 255, 255,0);\n"
                                            "font: 12pt \"Century Gothic\";\n"
                                        )
        self.ValueAvgEdit.setAlignment(Qt.AlignCenter)
        self.ValueAvgEdit.setStyleSheet("border-radius: 20px;\n"
                                            "background-color: rgba(255, 255, 255,0);\n"
                                            "font: 12pt \"Century Gothic\";\n"
                                        )

        self.ValueMaxEdit.setAlignment(Qt.AlignCenter)
        self.ValueMaxEdit.setStyleSheet("border-radius: 20px;\n"
                                            "background-color: rgba(255, 255, 255,0);\n"
                                            "font: 12pt \"Century Gothic\";\n"
                                        )

    def close_logic(self):
        self.close()

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key.Key_F11:
            if self.isMaximized():
                self.showNormal()
            else:
                self.showMaximized()

        if event.key() == QtCore.Qt.Key.Key_Escape:
            self.close()
