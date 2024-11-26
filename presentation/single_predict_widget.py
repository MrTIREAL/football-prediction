import os
import pathlib
from PyQt6.QtWidgets import QWidget, QMessageBox
from PyQt6.uic import loadUi

from business.controllers.single_predict_controller import SinglePredictController
from business.controllers.poisson_controller import PoissonController
from business.utils.common import CommonUtil
from business.utils.constants import ANALYSIS_MODE_PREFIX


class SinglePredictWidget(QWidget):
    def __init__(self, selected_date, league, season, mode):
        super().__init__()
        loadUi("./presentation/ui/single_predict.ui", self)
        self.controller = SinglePredictController()
        self.poisson = PoissonController()
        self.selected_date = selected_date
        self.league = league
        self.season = season
        self.mode = mode

        self.set_comboboxes()
        self.analyseButton.clicked.connect(self.on_analyseBtn_Clicked)
        self.excelButton.clicked.connect(self.on_excelBtn_Clicked)

    def set_comboboxes(self):
        self.homeTeamComboBox.clear()
        self.awayTeamComboBox.clear()
        teams_tuple = self.controller.select_teams()
        teams = [str(x[0]) for x in teams_tuple]
        self.homeTeamComboBox.addItems(teams)
        self.awayTeamComboBox.addItems(teams)

    def on_analyseBtn_Clicked(self):
        home_team = self.homeTeamComboBox.currentText()
        away_team = self.awayTeamComboBox.currentText()
        self.poisson.show_result_plot(home_team, away_team, self.mode)

    def on_excelBtn_Clicked(self):
        home_team = self.homeTeamComboBox.currentText()
        away_team = self.awayTeamComboBox.currentText()
        is_ok = self.poisson.save_to_excel(
            home_team, away_team, self.league, self.season, self.selected_date, self.mode)
        if is_ok:
            self.excel_dialog(home_team, away_team)
        else:
            self.error_dialog()

    def update_league(self, current_league, current_season):
        self.league = current_league
        self.season = current_season

    def update_date(self, date):
        self.selected_date = date

    def update_mode(self, mode):
        self.mode = mode

    def excel_dialog(self, home_team, away_team):
        excel_path = f"output/match_results/{home_team}-{away_team}_{
            CommonUtil.excel_datetime()}_{ANALYSIS_MODE_PREFIX[self.mode]}.xlsx"
        dlg = QMessageBox(self)
        dlg.setWindowTitle("Információ")
        dlg.setText(f"A mérkőzés sikeresen elmentésre került a következő néven: \n{
                    home_team}-{away_team}_{CommonUtil.excel_datetime()}_{ANALYSIS_MODE_PREFIX[self.mode]}.xlsx")
        dlg.setStandardButtons(
            QMessageBox.StandardButton.Open | QMessageBox.StandardButton.Cancel
        )
        dlg.setIcon(QMessageBox.Icon.Information)
        button = dlg.exec()

        if button == QMessageBox.StandardButton.Open:
            project_path = pathlib.Path().resolve()
            file_path = os.path.join(project_path, excel_path)
            os.startfile(file_path)

    def error_dialog(self):
        QMessageBox.critical(
            self,
            "Hiba",
            "Nem sikerült elmenti az eredményeket."
        )
