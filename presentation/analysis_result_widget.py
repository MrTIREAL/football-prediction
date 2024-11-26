from PyQt6.QtWidgets import QWidget, QHeaderView
from PyQt6.uic import loadUi
from PyQt6.QtCore import Qt, QAbstractTableModel
from PyQt6.QtGui import QFont

from business.controllers.analysis_result_controller import AnalysisResultController
from presentation.selected_result_dialog import SelectedResultDialog


class TableModel(QAbstractTableModel):
    def __init__(self, data=None):
        super(TableModel, self).__init__()
        self.header_labels = ["Id", "Dátum", "Liga", "Szezon", "Hazai",
                              "Vendég", "Hazai gól", "Vendég gól", "H", "D", "V", "Mód"]
        self._data = data or []

    def data(self, index, role):
        if role == Qt.ItemDataRole.DisplayRole:
            value = self._data[index.row()][index.column()]
            return value

        if role == Qt.ItemDataRole.FontRole and index.column() == 3:
            font = QFont()
            font.setBold(True)
            return font

    def rowCount(self, index):
        return len(self._data) if self._data else 0

    def columnCount(self, index):
        return len(self._data[0]) if self._data else 0

    def convert_league_data(self, data):
        return [list(x) for x in data]

    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole and orientation == Qt.Orientation.Horizontal:
            return self.header_labels[section]
        return QAbstractTableModel.headerData(self, section, orientation, role)

    def return_teams(self, row):
        return [self._data[row][2], self._data[row][3]]

    def return_id(self, row):
        return self._data[row][0]


class AnalysisResultWidget(QWidget):
    def __init__(self):
        super().__init__()
        loadUi("./presentation/ui/analysis_result.ui", self)
        self.controller = AnalysisResultController()

        self.analysisOpenBtn.clicked.connect(self.on_openBtn_Clicked)
        self.analysisDeleteBtn.clicked.connect(self.on_deleteBtn_Clicked)

    def update_model(self):
        data = self.controller.select_poisson_result_for_view()
        self.model = TableModel(data)
        self.resultTableView.setModel(self.model)
        if data:
            # Resize table columns
            for i in range(0, len(self.model.header_labels)):
                self.resultTableView.horizontalHeader().setSectionResizeMode(
                    i, QHeaderView.ResizeMode.ResizeToContents)

    def on_openBtn_Clicked(self):
        index = self.resultTableView.selectionModel().selectedRows()[0]
        model = self.resultTableView.model()
        poisson_id = model.return_id(index.row())
        dlg = SelectedResultDialog(self, poisson_id)
        dlg.exec()

    def on_deleteBtn_Clicked(self):
        index = self.resultTableView.selectionModel().selectedRows()[0]
        model = self.resultTableView.model()
        model_id = model.return_id(index.row())
        self.controller.delete_poisson_result(model_id)
        self.update_model()
