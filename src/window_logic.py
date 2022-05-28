from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import Qt
from enum import Enum

from PyQt5.QtWidgets import QDesktopWidget

import main_app
import csv
import math
import os
import json
import re
from config import *


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
    ERROR_NOT_PROPERTY = 16
    ERROR_NOT_MONEY = 17
    ERROR_POINT_NOT_LOADED = 18
    ERROR_EMPTY_PROPERTY = 19


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
        except ResearchCalcErrors:
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
        except ResearchCalcErrors:
            return exit_code


class ResearchSignals(QtCore.QObject):
    """ Сигналы для основного приложения """
    delete_rows = QtCore.pyqtSignal(int, int)


class ResearchApp(QtWidgets.QMainWindow, main_app.Ui_MainWindow):
    """ Класс-реализация окна исследования """

    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.setupUi(self)
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.filedialog_path = '../resources'

        # Обработчики кнопок.
        self.AddButton.clicked.connect(self.add_button_logic)
        self.AddButton.setGraphicsEffect(QtWidgets.QGraphicsDropShadowEffect(blurRadius=15, xOffset=-3, yOffset=3))
        self.DownloadButton.clicked.connect(self.load_button_logic)
        self.DownloadButton.setGraphicsEffect(QtWidgets.QGraphicsDropShadowEffect(blurRadius=15, xOffset=-3, yOffset=3))
        self.DeleteButton.clicked.connect(self.delete_button_logic)
        self.DeleteButton.setGraphicsEffect(QtWidgets.QGraphicsDropShadowEffect(blurRadius=15, xOffset=3, yOffset=3))
        self.SaveButton.clicked.connect(self.save_button_logic)
        self.SaveButton.setGraphicsEffect(QtWidgets.QGraphicsDropShadowEffect(blurRadius=15, xOffset=3, yOffset=3))
        self.PointButton.clicked.connect(self.calc_point_logic)
        self.PointButton.setGraphicsEffect(QtWidgets.QGraphicsDropShadowEffect(blurRadius=25, xOffset=3, yOffset=3))
        self.CloseButton.clicked.connect(self.close_logic)
        self.SavePointButton.clicked.connect(self.save_point_logic)
        self.SavePointButton.setGraphicsEffect(QtWidgets.QGraphicsDropShadowEffect(blurRadius=25, xOffset=3, yOffset=3))
        self.CalcPointButton.clicked.connect(self.calc_join_point_logic)
        self.CalcPointButton.setGraphicsEffect(QtWidgets.QGraphicsDropShadowEffect(blurRadius=15, xOffset=3, yOffset=3))
        self.SaveResultButton.clicked.connect(self.save_result_logic)
        self.SaveResultButton.setGraphicsEffect(QtWidgets.QGraphicsDropShadowEffect(blurRadius=15, xOffset=-3, yOffset=3))

        # Таблица.
        self.table_model = QtGui.QStandardItemModel()
        self.tableView.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.tableView.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.SingleSelection)
        self.tableView.setModel(self.table_model)

        # Объект управления сигналами.
        self.win_manager = ResearchSignals()
        self.win_manager.delete_rows.connect(self.delete_rows_logic)

        # Объект расчетов.
        self.calculator = ResearchCalc()

        # Словарь для свойств.
        self.properties_indexes = {}

        # Словарь для сохранения трехточки.
        self.pnt_list = []
        self.pnt_dict = {}

        # Флаги сохранения трехточки.
        self.point_flag = False
        self.join_point_flag = False

    @staticmethod
    def output_style_in_qlineedit(obj: QtWidgets.QLineEdit, text: str):
        """
        Создание единого стиля для вывода в QLineEdit.

        :param obj: Объект, куда выводить данные.
        :param text: Строка, которую необходимо вывести.
        :return: None
        """
        obj.setText(text)
        obj.setAlignment(Qt.AlignCenter)
        obj.setStyleSheet("border-radius: 20px;\n"
                          "background-color: rgba(255, 255, 255, 50);\n"
                          "font: 12pt \"Century Gothic\";\n"
                        )

    @staticmethod
    def threepoint_formatting_for_output(threepoint: list) -> str:
        """
        Создание единого стиля для вывода трехточек.

        :param threepoint: Данные после расчета функции трехточки.
        :return: str вида Min: [число, вероятность] Avg: [число, вероятность] Max: [число, вероятность]
        """
        float_precision_1 = '.0f'
        float_precision_2 = '.2f'

        avg_minimal = "[" + str(format(threepoint[0][0], float_precision_1)) + \
                      ", " + str(format(threepoint[0][1], float_precision_2)) + "]"
        avg_middle = "[" + str(format(threepoint[1][0], float_precision_1)) + \
                     ", " + str(format(threepoint[1][1], float_precision_2)) + "]"
        avg_maximal = "[" + str(format(threepoint[2][0], float_precision_1)) + \
                      ", " + str(format(threepoint[2][1], float_precision_2)) + "]"

        return "Min: " + avg_minimal + "\tAvg: " + avg_middle + "\tMax: " + avg_maximal

    @staticmethod
    def show_message_box(title: str, text: str):
        """
        Функция для вывода сообщений оператору.

        :param title: Заголовок сообщения.
        :param text: Текст сообщения.
        :return: None
        """
        msg_box = QtWidgets.QMessageBox()
        if title == "Ошибка":
            msg_box.setIcon(QtWidgets.QMessageBox.Critical)
            msg_box.setWindowFlags(QtCore.Qt.FramelessWindowHint)
            msg_box.setStyleSheet("border-radius: 20px;\n"
                                  "background-color: rgba(255, 255, 188, 255);\n"
                                  "font: 14pt \"Century Gothic\";\n")
        elif title == "Информация" or title == "Предупреждение":
            msg_box.setIcon(QtWidgets.QMessageBox.Critical)
            msg_box.setWindowFlags(QtCore.Qt.FramelessWindowHint)
            msg_box.setStyleSheet("border-radius: 10px;\n"
                                  "background-color: rgba(255, 255, 188, 255);\n"
                                  "font: 14pt \"Century Gothic\";\n")
        msg_box.setWindowTitle(title)
        msg_box.setText("<div align='top'>" + text)
        msg_box.exec()

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
        self.context_menu.setStyleSheet("background-color: rgba(235,193,255,255);"
                                        "font: 10pt \"Century Gothic\";\n")

        indexes = self.tableView.selectionModel().selectedIndexes()
        is_digit = False
        is_letter = False
        is_empty = False
        for idx in indexes:
            if not idx.data():
                is_empty = True
            else:
                if str(idx.data()).isdigit():
                    is_digit = True
                else:
                    is_letter = True

        if is_empty:
            lower_property.setEnabled(False)
            upper_property.setEnabled(False)
            equal_property.setEnabled(False)
            add_as_property.setEnabled(False)

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
        added_prop_view = str(headers[indexes[-1].column()]) + ": "
        added_prop = ""

        # Проверка на числовое значение.
        if str(item).isdigit():
            # Добавление символа перед свойством.
            if prop:
                added_prop += str(prop)
                added_prop_view += str(prop) + item
        else:
            added_prop += item
            added_prop_view += item

        # Отображение текста в поле.
        self.output_style_in_qlineedit(self.propertylineEdit, added_prop_view)

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
                    model.setData(index, data_help)
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
                self.show_message_box("Информация", "Таблица не загружена, добавление строк невозможно.")
                exit_code = ErrorCodes.ERROR_TABLE_NOT_LOADED
                raise ResearchAppErrors("Таблица не загружена, добавление строк невозможно.")
            self.tableView.model().insertRow(self.tableView.model().rowCount(QtCore.QModelIndex()))
        except ResearchAppErrors:
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
                return

            _, file_extension = os.path.splitext(filename)

            if file_extension != '.csv':
                self.show_message_box("Ошибка", "Загружен файл неверного формата.")
                exit_code = ErrorCodes.ERROR_INVALID_FILE_FORMAT
                raise ResearchAppErrors("Загружен файл неверного формата.")

            if os.stat(filename).st_size == 0:
                self.show_message_box("Информация", "Загружен пустой файл - работа с ним невозможна.")
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
                                         "background-color: rgba(255, 255, 255, 50);\n"
                                         "font: 10pt \"Century Gothic\";")
        except ResearchAppErrors:
            return exit_code

    def delete_button_logic(self):
        """
        Обработчик нажатия на кнопку "Удалить".

        :return: None
        """
        exit_code = None
        try:
            if not self.tableView.model().columnCount() > 0:
                self.show_message_box("Информация", "Таблица не загружена, удаление строк невозможно.")
                exit_code = ErrorCodes.ERROR_TABLE_NOT_LOADED
                raise ResearchAppErrors("Таблица не загружена, удаление строк невозможно.")

            rows = self.tableView.selectionModel().selectedIndexes()

            if not rows:
                self.show_message_box("Информация", "Не выбрана строка для удаления.")
                exit_code = ErrorCodes.ERROR_NO_LINE_SELECTED
                raise ResearchAppErrors("Не выбрана строка для удаления.")

            for row in rows:
                self.win_manager.delete_rows.emit(row.row(), len(rows))
        except ResearchAppErrors:
            return exit_code

    def save_button_logic(self):
        """
        Обработчик нажатия на кнопку "Сохранить".

        :return: None
        """
        exit_code = None
        try:
            if not self.tableView.model().columnCount() > 0:
                self.show_message_box("Информация", "Таблица не загружена и не создана - ее сохранение невозможно.")
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
        except ResearchAppErrors:
            return exit_code

    def calc_point_logic(self):
        """
        Обработчик нажатия на кнопку "Рассчитать трехточку".

        :return: None
        """
        exit_code = None
        try:
            if not self.properties_indexes:
                self.point_flag = False
                self.show_message_box("Информация", "Не выбрано свойство для расчета трехточки.")
                exit_code = ErrorCodes.ERROR_NOT_PROPERTY
                raise ResearchAppErrors("Не выбрано свойство для расчета трехточки.")

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

            if wage_col is None:
                self.point_flag = False
                self.output_style_in_qlineedit(self.ValuePointEdit, "Внимание! В таблице нет столбца \"Заработная плата\" - расчет невозможен.")
                exit_code = ErrorCodes.ERROR_NOT_MONEY
                raise ResearchAppErrors("Внимание! В таблице нет столбца ЗП(заработная плата).")

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

            # Вычисление трехточки.
            correct_len = 3
            if len(correct_rows) > correct_len and len(correct_wage) > correct_len:
                semi = self.calculator.calc_semi(correct_wage)
                three_points = self.calculator.calc_three_points(semi)

                if isinstance(three_points, ErrorCodes):
                    self.point_flag = False
                    return

                avg_minimal = "[" + str(three_points[0][0]) + \
                              ", " + str(three_points[0][1]) + "]"
                avg_middle = "[" + str(three_points[1][0]) + \
                             ", " + str(three_points[1][1]) + "]"
                avg_maximal = "[" + str(three_points[2][0]) + \
                              ", " + str(three_points[2][1]) + "]"

                self.pnt_dict = {"Min": avg_minimal,
                                  "Avg": avg_middle,
                                  "Max": avg_maximal}

                # Вывод информации в поля.
                self.output_style_in_qlineedit(self.ValuePointEdit, self.threepoint_formatting_for_output(three_points))
                self.point_flag = True
            else:
                self.output_style_in_qlineedit(self.ValuePointEdit, "Внимание! Расчёт не возможен.")
                self.point_flag = False
        except ResearchAppErrors:
            return exit_code

    def close_logic(self):
        """
        Обработчик нажатия на кнопку "Закрыть".

        :return: None
        """
        self.close()

    def save_point_logic(self):
        """
        Обработчик нажатия на кнопку "Сохранить трехточку".

        :return: None
        """
        exit_code = None
        try:
            if self.point_flag:
                str_point = self.ValuePointEdit.text()
                if not len(str_point) > 0:
                    self.output_style_in_qlineedit(self.ValuePointEdit, "Внимание! Расчетов нет - сохранение невозможно.")
                    exit_code = ErrorCodes.ERROR_POINT_NOT_LOADED
                    raise ResearchAppErrors("Расчетов нет - сохранение невозможно.")

                dialog_name = "Сохранение данных"
                options = QtWidgets.QFileDialog.Options()
                filename, _ = QtWidgets.QFileDialog.getSaveFileName(self, dialog_name, self.filedialog_path,
                                                                     "All types of docs (*.pnt)", options=options)

                if filename:
                    with open(filename, 'w', newline='') as File:
                        json_Data = json.dumps(self.pnt_dict)
                        File.write(json_Data)
            else:
                self.show_message_box("Информация", "Внимание! Расчетов нет - сохранение невозможно.")

        except ResearchAppErrors:
            return exit_code

    def _parse_pnt_values(self, value: str) -> list | ErrorCodes:
        """ Перевести строку со списком в список чисел """
        try:
            left = float(re.sub(r"\[([\d.].*), ([\d.].*)\]", r"\1", value))
            right = float(re.sub(r"\[([\d.].*), ([\d.].*)\]", r"\2", value))
            return [left, right]
        except ValueError:
            exit_code = ErrorCodes.ERROR_NOT_NUMERIC
            return exit_code

    def calc_join_point_logic(self):
        """
            Обработчик нажатия на кнопку "Рассчитать объединение трехточек".

            :return: None
        """
        exit_code = None
        self.pnt_list.clear()
        try:
            dialog_name = "Загрузка данных"
            options = QtWidgets.QFileDialog.Options()
            filenames, _ = QtWidgets.QFileDialog.getOpenFileNames(self, dialog_name, self.filedialog_path,
                                                                  "All types of docs (*.pnt)", options=options)

            if not filenames:
                self.join_point_flag = False
                self.output_style_in_qlineedit(self.ValueJoinPointEdit, "Файл не загружен.")
                exit_code = ErrorCodes.ERROR_FILE_NOT_LOADED
                raise ResearchAppErrors("Файл не загружен.")

            for filename in filenames:
                _, file_extension = os.path.splitext(filename)

                if file_extension != '.pnt':
                    self.join_point_flag = False
                    self.output_style_in_qlineedit(self.ValueJoinPointEdit, "Загружен файл неверного формата.")
                    exit_code = ErrorCodes.ERROR_INVALID_FILE_FORMAT
                    raise ResearchAppErrors("Загружен файл неверного формата.")

                if os.stat(filename).st_size == 0:
                    self.join_point_flag = False
                    self.output_style_in_qlineedit(self.ValueJoinPointEdit, "Загружен пустой файл - работа с ним невозможна.")
                    exit_code = ErrorCodes.ERROR_EMPTY_FILE
                    raise ResearchAppErrors("Загружен пустой файл - работа с ним невозможна.")

                with open(filename, newline='') as File:
                    try:
                        json_data = json.load(File)
                    except json.JSONDecodeError:
                        self.join_point_flag = False
                        exit_code = ErrorCodes.ERROR_INVALID_FILE_FORMAT
                        return exit_code

                for k in pnt_keys:
                    if k not in json_data:
                        self.join_point_flag = False
                        self.output_style_in_qlineedit(self.ValueJoinPointEdit, "Отсутствует ожидаемый ключ в загруженном файле.")
                        exit_code = ErrorCodes.ERROR_POINT_NOT_LOADED
                        raise ResearchAppErrors("Отсутствует ожидаемый ключ в загруженном файле.")

                    parsed_values = self._parse_pnt_values(json_data[k])
                    if isinstance(parsed_values, ErrorCodes):
                        self.join_point_flag = False
                        self.output_style_in_qlineedit(self.ValueJoinPointEdit,
                                                       "Ошибка в формате данных загруженной трёхточки.")
                        exit_code = ErrorCodes.ERROR_NOT_NUMERIC
                        raise ResearchAppErrors("Ошибка в формате данных загруженной трёхточки.")

                    self.pnt_list.append(parsed_values)

            if self.pnt_list:
                semi = self.calculator.calc_semi(self.pnt_list)
                point = self.calculator.calc_three_points(semi)

                if isinstance(point, ErrorCodes):
                    return

                self.output_style_in_qlineedit(self.ValueJoinPointEdit, self.threepoint_formatting_for_output(point))
                self.join_point_flag = True
            else:
                self.join_point_flag = False
        except ResearchAppErrors:
            return exit_code

    def save_result_logic(self):
        """
        Обработчик нажатия на кнопку "Сохранить результат".

        :return: None
        """
        exit_code = None
        try:
            if self.join_point_flag:
                str_point = self.ValueJoinPointEdit.text()
                if not len(str_point) > 0:
                    self.show_message_box("Информация", "Внимание! Расчетов нет - сохранение невозможно.")
                    exit_code = ErrorCodes.ERROR_POINT_NOT_LOADED
                    raise ResearchAppErrors("Расчетов нет - сохранение невозможно.")

                dialog_name = "Сохранение данных"
                options = QtWidgets.QFileDialog.Options()
                filename, _ = QtWidgets.QFileDialog.getSaveFileName(self, dialog_name, self.filedialog_path,
                                                                     "All types of docs (*.pnt)", options=options)

                if filename:
                    with open(filename, 'w', newline='') as File:
                        json_Data = json.dumps(self.pnt_dict)
                        File.write(json_Data)
            else:
                self.show_message_box("Информация", "Внимание! Расчетов нет - сохранение невозможно.")
        except ResearchAppErrors:
            return exit_code

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key.Key_Escape:
            self.close()
