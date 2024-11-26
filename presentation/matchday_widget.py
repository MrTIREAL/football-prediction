from PyQt6.QtWidgets import QWidget, QMessageBox
from PyQt6.uic import loadUi

from business.controllers.matchday_controller import MatchdayController
from presentation.matchday_dialog import MatchdayDialog


class MatchdayWidget(QWidget):
    def __init__(self, league, season, mode):
        super().__init__()
        loadUi("./presentation/ui/matchday.ui", self)
        self.controller = MatchdayController()
        self.set_current_date()
        self.league = league
        self.season = season
        self.mode = mode
        self.calendarDateBtn.clicked.connect(self.on_dateBtn_Clicked)

    def set_current_date(self):
        selected_year = self.controller.get_selected_year()
        selected_month = self.controller.get_selected_month()
        self.calendarWidget.setCurrentPage(
            int(selected_year), int(selected_month))

    def update_league(self, current_league, current_season):
        self.league = current_league
        self.season = current_season

    def update_mode(self, mode):
        self.mode = mode

    def on_dateBtn_Clicked(self):
        selected_date = self.calendarWidget.selectedDate()
        pydate = str(selected_date.toPyDate())
        matches = self.controller.get_matches_on_date(
            self.league, self.season, pydate)
        if len(matches) != 0:
            dlg = MatchdayDialog(self, matches, self.league,
                                 self.season, self.mode, pydate)
            dlg.exec()
        else:
            self.error_dialog()

    def error_dialog(self):
        QMessageBox.critical(
            self,
            "Mérkőzések",
            "A mai napon nincsen mérkőzés!"
        )
