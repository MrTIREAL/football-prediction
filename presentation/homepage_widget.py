from PyQt6.QtWidgets import QWidget
from PyQt6.uic import loadUi


class HomepageWidget(QWidget):
    def __init__(self, display_league, league_date):
        super().__init__()
        loadUi("./presentation/ui/homepage.ui", self)
        self.homepageDateLbl.setText(league_date)
        self.selectedTablelbl.setText(display_league)

    def update_date(self, league_date):
        self.homepageDateLbl.setText(league_date)

    def update_display_league(self, display_league):
        self.selectedTablelbl.setText(display_league)
