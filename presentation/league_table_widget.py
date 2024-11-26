from PyQt6.QtWidgets import QWidget, QHeaderView
from PyQt6.uic import loadUi
from PyQt6.QtCore import Qt, QAbstractTableModel
from PyQt6.QtGui import QFont

from business.controllers.league_table_controller import LeagueTableController


class TableModel(QAbstractTableModel):
    def __init__(self, data=None):
        super(TableModel, self).__init__()
        self.header_labels = ["Csapat", "M", "Pt", "Gy",
                              "D", "V", "R", "K", "GK", "AVG", "AVG 5", "AVG 10"]
        self._data = data

    def data(self, index, role):
        if role == Qt.ItemDataRole.DisplayRole:
            value = self._data[index.row()][index.column()]
            return value

        if role == Qt.ItemDataRole.FontRole and index.column() == 2:
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


class LeagueTableWidget(QWidget):
    def __init__(self):
        super().__init__()
        loadUi("./presentation/ui/league_table.ui", self)
        self.controller = LeagueTableController()

    def update_model(self, league, season, league_date):
        self.controller.delete_all_teams()
        data = self.controller.calculate_table(league, season, league_date)
        self.controller.insert_league_standings(data)
        self.model = TableModel(data)
        self.leagueTableView.setModel(self.model)
        # Resize table columns
        for i in range(0, len(self.model.header_labels)):
            self.leagueTableView.horizontalHeader().setSectionResizeMode(
                i, QHeaderView.ResizeMode.ResizeToContents)
