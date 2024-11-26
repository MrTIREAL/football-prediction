import requests
from PyQt6.QtWidgets import QWidget, QMessageBox
from PyQt6.uic import loadUi
from PyQt6.QtCore import pyqtSignal, QDate

from business.utils.constants import ANALYSIS_MODES, LEAGUE_PREFIX, LEAGUES, SEASONS, WEBSITE_URL
from business.controllers.settings_controller import SettingsController


class SettingsWidget(QWidget):
    dateClicked = pyqtSignal(str)
    leagueSeasonClicked = pyqtSignal(list)
    modeClicked = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        loadUi("./presentation/ui/settings.ui", self)
        self.controller = SettingsController()
        self.set_current_date()
        self.set_comboboxes()
        self.selectedDateBtn.clicked.connect(self.onDateBtnClicked)
        self.leagueSeasonBtn.clicked.connect(self.onLeagueBtnClicked)
        self.modeButton.clicked.connect(self.onModeBtnClicked)
        self.leagueUpdateButton.clicked.connect(self.onUpdateBtnClicked)

    def set_current_date(self):
        selected_date = self.controller.get_selected_date()
        qdate = QDate.fromString(selected_date, "yyyy-MM-dd")
        self.dateEdit.setDate(qdate)

    def set_comboboxes(self):
        current_league = self.controller.get_current_league()
        current_season = self.controller.get_current_season()
        current_mode = self.controller.get_current_mode()

        self.leagueComboBox.addItems(LEAGUES)
        self.seasonComboBox.addItems(SEASONS)
        self.updateLeaguecomboBox.addItems(LEAGUES)
        self.modeComboBox.addItems(ANALYSIS_MODES)
        self.leagueComboBox.setCurrentIndex(LEAGUES.index(current_league))
        self.seasonComboBox.setCurrentIndex(SEASONS.index(current_season))
        self.updateLeaguecomboBox.setCurrentIndex(
            LEAGUES.index(current_league))
        self.modeComboBox.setCurrentIndex(ANALYSIS_MODES.index(current_mode))

    def onDateBtnClicked(self):
        selected_date = self.dateEdit.date()
        pydate = str(selected_date.toPyDate())
        self.controller.update_selected_date(pydate)
        self.dateClicked.emit(pydate)

    def onLeagueBtnClicked(self):
        league = self.leagueComboBox.currentText()
        season = self.seasonComboBox.currentText()
        self.controller.update_current_league(league)
        self.controller.update_current_season(season)
        self.leagueSeasonClicked.emit([league, season])

    def onModeBtnClicked(self):
        mode = self.modeComboBox.currentText()
        self.controller.update_current_mode(mode)
        self.modeClicked.emit(mode)

    def onUpdateBtnClicked(self):
        league = self.updateLeaguecomboBox.currentText()
        url = WEBSITE_URL + LEAGUE_PREFIX[league]
        self.download_file(url, LEAGUE_PREFIX[league])

    def download_file(self, url, league):
        file_url = f'./infrastructure/storage/league_data/{
            league}_2024_2025.csv'
        req = requests.get(url)
        if req.status_code == 200:
            content = req.content
            csv_file = open(file_url, 'wb')
            csv_file.write(content)
            csv_file.close()
            self.information_dialog(file_url)

    def information_dialog(self, url):
        QMessageBox.information(
            self,
            "Információ dialog",
            f"A file letöltve: \n {url}"
        )
