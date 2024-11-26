from PyQt6.QtWidgets import QDialog, QTableView, QHeaderView, QLabel, QVBoxLayout
from PyQt6.QtCore import Qt, QAbstractTableModel
from PyQt6.QtGui import QFont, QImage

tick = QImage('./presentation/assets/tick.png')
cross = QImage('./presentation/assets/cross.png')


class TableModel(QAbstractTableModel):
    def __init__(self, data):
        super().__init__()
        self._data = data or []
        self.header_labels = ["Dátum", "Hazai", "Vendég",
                              "Hazai gól", "Vendég gól", "E", "T", "P", "Mód"]

    def data(self, index, role):
        if role == Qt.ItemDataRole.DisplayRole:
            return self._data[index.row()][index.column()]

        if role == Qt.ItemDataRole.FontRole and (index.column() == 1 or index.column() == 2 or index.column() == 5):
            font = QFont()
            font.setBold(True)
            return font

        if role == Qt.ItemDataRole.DecorationRole:
            if index.column() == 6 and self._data[index.row()][5] == self._data[index.row()][6]:
                return tick
            elif index.column() == 6 and self._data[index.row()][5] != self._data[index.row()][6]:
                return cross

            if index.column() == 7 and self._data[index.row()][5] == self._data[index.row()][7]:
                return tick
            elif index.column() == 7 and self._data[index.row()][5] != self._data[index.row()][7]:
                return cross

    def rowCount(self, index):
        return len(self._data) if self._data else 0

    def columnCount(self, index):
        return len(self._data[0]) if self._data else 0

    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole and orientation == Qt.Orientation.Horizontal:
            return self.header_labels[section]
        return QAbstractTableModel.headerData(self, section, orientation, role)


class TotoResultDialog(QDialog):
    def __init__(self, parent, data):
        super().__init__(parent)
        self.data = data
        self.table_data = []

        self.setMinimumWidth(650)
        self.setMinimumHeight(400)
        for i in data:
            row = [i[5], i[6], i[7], i[8], i[9], i[10], i[11], i[12], i[4]]
            self.table_data.append(row)
        # Dialog ui
        self.setWindowTitle("Totó meccsei")
        layout = QVBoxLayout()

        title = QLabel("A kiválasztott mérkőzések:")
        title.setStyleSheet("font-weight: bold; font-size: 18px;")
        leagueLbl = QLabel("Liga: " + str(self.data[0][2]))
        seasonLbl = QLabel("Szezon: " + str(self.data[0][3]))
        layout.addWidget(title)
        layout.addWidget(leagueLbl)
        layout.addWidget(seasonLbl)

        self.table = QTableView()
        self.model = TableModel(self.table_data)
        self.table.setModel(self.model)
        # Resize table columns
        for i in range(0, len(self.model.header_labels)):
            self.table.horizontalHeader().setSectionResizeMode(
                i, QHeaderView.ResizeMode.ResizeToContents)
        layout.addWidget(self.table)
        self.setLayout(layout)
