from PyQt6.QtWidgets import QWidget, QMessageBox
from PyQt6.uic import loadUi

from business.controllers.toto_controller import TotoController
from business.utils.common import CommonUtil
from presentation.toto_dialog import TotoDialog


class TotoWidget(QWidget):
    def __init__(self, league, season, mode):
        super().__init__()
        loadUi("./presentation/ui/toto.ui", self)
        self.controller = TotoController()
        self.set_current_date()
        self.league = league
        self.season = season
        self.mode = mode

        self.generateTotoBtn.clicked.connect(self.on_genereTotoBtn_Clicked)

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

    def on_genereTotoBtn_Clicked(self):
        selected_date = self.calendarWidget.selectedDate()
        pydate = str(selected_date.toPyDate())
        date = CommonUtil.calendar_date_to_datetime(pydate)
        week = CommonUtil.get_days_from_week(date)
        week_number = selected_date.weekNumber()[0]

        data = self.controller.get_toto_data(self.league, self.season)
        df = data.get_matches_on_week(week)
        if not df.empty:
            matches = df.to_dict('records')
            dlg = TotoDialog(self, matches, self.league,
                             self.season, self.mode, week_number)
            dlg.exec()
        else:
            self.error_dialog()

    def error_dialog(self):
        QMessageBox.critical(
            self,
            "Hiba",
            "Ezen a héten nincsenek mérkőzések!"
        )
