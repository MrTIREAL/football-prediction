from PyQt6.QtWidgets import QWidget, QHeaderView
from PyQt6.uic import loadUi
from PyQt6.QtCore import Qt, QAbstractTableModel
from PyQt6.QtGui import QFont

from business.controllers.toto_controller import TotoController
from presentation.toto_result_dialog import TotoResultDialog


class TableModel(QAbstractTableModel):
    def __init__(self, data=None):
        super(TableModel, self).__init__()
        self.header_labels = ["Hét", "Liga", "Szezon", "Mód", "Dátum"]
        self._data = data or []

    def data(self, index, role):
        if role == Qt.ItemDataRole.DisplayRole:
            value = self._data[index.row()][index.column()]
            if index.column() == 4:
                value = value[:10]
            return value

        if role == Qt.ItemDataRole.FontRole and index.column() == 0:
            font = QFont()
            font.setBold(True)
            return font

    def rowCount(self, index):
        return len(self._data) if self._data else 0

    def columnCount(self, index):
        return len(self._data[0]) if self._data else 0

    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole and orientation == Qt.Orientation.Horizontal:
            return self.header_labels[section]
        return QAbstractTableModel.headerData(self, section, orientation, role)

    def data_for_list(self, row):
        return self._data[row]


class TotoResultWidget(QWidget):
    def __init__(self):
        super().__init__()
        loadUi("./presentation/ui/analysis_result.ui", self)
        self.controller = TotoController()

        self.analysisOpenBtn.clicked.connect(self.on_openBtn_Clicked)
        self.analysisDeleteBtn.clicked.connect(self.on_deleteBtn_Clicked)

    def update_model(self):
        data = self.controller.select_toto_result_for_view()
        if data:
            self.model = TableModel(data)
            self.resultTableView.setModel(self.model)
            for i in range(0, len(self.model.header_labels)):
                self.resultTableView.horizontalHeader().setSectionResizeMode(
                    i, QHeaderView.ResizeMode.ResizeToContents)

    def on_openBtn_Clicked(self):
        index = self.resultTableView.selectionModel().selectedRows()[0]
        selected_data = self.model.data_for_list(index.row())
        data = self.controller.select_toto_result_for_week(
            selected_data[0], selected_data[1], selected_data[2], selected_data[3])
        if len(data) != 0:
            dlg = TotoResultDialog(self, data)
            dlg.exec()

    def on_deleteBtn_Clicked(self):
        index = self.resultTableView.selectionModel().selectedRows()[0]
        model = self.resultTableView.model()
        model_data = model.data_for_list(index.row())
        self.controller.delete_toto_result(model_data)
        self.update_model()
