from PyQt5 import QtWidgets, QtCore, QtGui

import main_app
import csv
import math
import re


class ResearchCalc:
    """ Вычисление трехточки """
    def __init__(self):
        super(ResearchCalc, self).__init__()

    @staticmethod
    def calc_semi(data_array: list) -> list:
        """
        Вычисление четырех первых семиинвариантов для массива данных.

        :param data_array: Входной массив данных.
        :return: Массив из 5-ти элементов.
        """
        m1, m2, m3, m4 = 0, 0, 0, 0
        size = 0
        for item in data_array:
            # Гистограмма
            if isinstance(item, list):
                if len(item) != 2:
                    return []

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

    @staticmethod
    def calc_three_points(semi_list: list) -> list:
        """
        Вычисление трехточки.

        :param semi_list: Массив с семиинвариантами.
        :return: Среднее минимальное, среднее максимальное, среднее среднее.
        """
        if len(semi_list) == 5:
            xs, dd, aa, ee = semi_list[0], semi_list[1], semi_list[2] / semi_list[1] / 2., semi_list[3]
            ss = math.sqrt(dd)
            first = ee / (dd ** 2)
            second = (3. * (aa ** 2)) / dd
            qq = math.sqrt(3 + first - second)
            x1, x2 = -ss * qq + xs + aa, ss * qq + xs + aa
            p1, p2 = ss / (2. * qq * (ss * qq - aa)), ss / (2. * qq * (ss * qq + aa))
            return [[x1, p1], [xs, 1 - p1 - p2], [x2, p2]]


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
        self.properties_indexes = []

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
        indexes = self.tableView.selectionModel().selectedIndexes()
        for idx in indexes:
            item = idx.data()
            # Проверка на числовое значение.
            if str(item).isdigit():
                # Добавление символа перед свойством.
                if prop:
                    self.propertylineEdit.insert(str(prop))

            # Добавление свойства.
            self.propertylineEdit.insert(idx.data())
            if indexes.index(idx) != len(indexes) - 1:
                self.propertylineEdit.insert(", ")

        self.properties_indexes = indexes

    @QtCore.pyqtSlot(int, int)
    def delete_rows_logic(self, row_number: int, rows_count: int):
        """
        Слот для удаления строк таблицы.

        :param row_number: Номер удаляемой строки.
        :param rows_count: Количество строк.
        :return: None
        """
        self.tableView.model().removeRows(row_number, rows_count)

    def add_button_logic(self):
        """
        Обработчик нажатия на кнопку "Добавить".

        :return: None
        """
        if self.tableView.model().columnCount() > 0:
            self.tableView.model().insertRow(self.tableView.model().rowCount(QtCore.QModelIndex()))

    def load_button_logic(self):
        """
        Обработчик нажатия на кнопку "Загрузить".

        :return: None
        """
        dialog_name = "Загрузка данных"
        options = QtWidgets.QFileDialog.Options()
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(self, dialog_name, self.filedialog_path,
                                                            "All types of docs (*.csv)", options=options)

        if filename:
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

    def delete_button_logic(self):
        """
        Обработчик нажатия на кнопку "Удалить".

        :return: None
        """
        rows = self.tableView.selectionModel().selectedIndexes()
        if rows:
            for row in rows:
                self.win_manager.delete_rows.emit(row.row(), len(rows))

    def save_button_logic(self):
        """
        Обработчик нажатия на кнопку "Сохранить".

        :return: None
        """
        dialog_name = "Сохранение данных"
        options = QtWidgets.QFileDialog.Options()
        filename, _ = QtWidgets.QFileDialog.getSaveFileName(self, dialog_name, self.filedialog_path,
                                                            "All types of docs (*.csv)", options=options)

        if filename:
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

    def parse_properties(self, properties: str):
        """
        Парсинг указанных свойств.

        :param properties: Свойства.
        :return: None
        """
        splitted = [x.strip() for x in properties.split(',')]
        for prop in splitted:
            operation = re.match(r"([<>=]*)(\d*)", prop)



    def calc_point_logic(self):
        """
        Обработчик нажатия на кнопку "Рассчитать".

        :return: None
        """
        # Анализ свойств.
        properties = self.propertylineEdit.text()
        self.parse_properties(properties)

        # three_points = self.calculator.calc_three_points([4.875, 14.859, 84.199, 246.678, 8])
        # float_precision = '.5f'
        # avg_minimal = "[" + str(format(three_points[0][0], float_precision)) + \
        #               ", " + str(format(three_points[0][1], float_precision)) + "]"
        # self.ValueMinEdit.setText(avg_minimal)
        #
        # avg_middle = "[" + str(format(three_points[1][0], float_precision)) + \
        #              ", " + str(format(three_points[1][1], float_precision)) + "]"
        # self.ValueAvgEdit.setText(avg_middle)
        #
        # avg_maximal = "[" + str(format(three_points[2][0], float_precision)) + \
        #               ", " + str(format(three_points[2][1], float_precision)) + "]"
        # self.ValueMaxEdit.setText(avg_maximal)

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key.Key_F11:
            if self.isMaximized():
                self.showNormal()
            else:
                self.showMaximized()

        if event.key() == QtCore.Qt.Key.Key_Escape:
            self.close()
