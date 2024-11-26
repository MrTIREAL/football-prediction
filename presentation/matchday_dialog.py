import pandas as pd
from PyQt6.QtWidgets import QDialog, QMessageBox
from PyQt6.uic import loadUi
from PyQt6.QtCore import Qt, QAbstractListModel

from business.controllers.poisson_controller import PoissonController


class MatchModel(QAbstractListModel):
    def __init__(self, *args, matches=None, **kwargs):
        super(MatchModel, self).__init__(*args, **kwargs)
        self.matches = matches or []

    def data(self, index, role):
        if role == Qt.ItemDataRole.DisplayRole:
            text = self.matches[index.row()]
            return text[0] + ' - ' + text[1]

    def rowCount(self, index):
        return len(self.matches)


class MatchdayDialog(QDialog):
    def __init__(self, parent, matches: pd.DataFrame, league, season, mode, selected_date):
        super().__init__(parent)
        loadUi("./presentation/ui/matchday_dialog.ui", self)
        self.controller = PoissonController()
        self.matches = matches
        self.league = league
        self.season = season
        self.mode = mode
        self.date = selected_date
        self.model = MatchModel()
        self.set_model()
        self.matchlistListView.setModel(self.model)

        self.analyseBtn.clicked.connect(self.on_analyseBtn_Clicked)
        self.allAnalyseBtn.clicked.connect(self.on_allAnalyseBtn_Clicked)

    def set_model(self):
        row_list = self.matches.loc[:, [
            'HomeTeam', 'AwayTeam']].values.tolist()
        for i, _ in enumerate(row_list):
            self.model.matches.append([row_list[i][0], row_list[i][1]])

    def on_analyseBtn_Clicked(self):
        indexes = self.matchlistListView.selectedIndexes()
        if indexes:
            index = indexes[0]
            home_team = self.model.matches[index.row()][0]
            away_team = self.model.matches[index.row()][1]
            self.controller.save_result_to_sql(
                self.date, home_team, away_team, self.league, self.season, self.mode)
            self.information_dialog()

    def on_allAnalyseBtn_Clicked(self):
        for team in self.model.matches:
            home_team = team[0]
            away_team = team[1]
            self.controller.save_result_to_sql(
                self.date, home_team, away_team, self.league, self.season, self.mode)
        self.information_dialog()

    def information_dialog(self):
        QMessageBox.information(
            self,
            "Információ dialog",
            "Az elemzés elkészűlt."
        )
