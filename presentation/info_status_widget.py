from PyQt6.QtWidgets import QWidget
from PyQt6.uic import loadUi


class InfoStatusWidget(QWidget):
    def __init__(self, display_league, league_date, current_mode=None):
        super().__init__()
        loadUi("./presentation/ui/info_statusbar.ui", self)
        self.currentDateLbl.setText(league_date)
        self.currentTableLbl.setText(display_league)
        self.modeLbl.setText(current_mode)
