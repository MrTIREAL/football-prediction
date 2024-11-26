from PyQt6.QtWidgets import (
    QDialog, QMessageBox, QLabel,
    QHBoxLayout, QButtonGroup, QRadioButton,
    QVBoxLayout, QPushButton
)

from business.controllers.poisson_controller import PoissonController
from business.controllers.toto_controller import TotoController


class TotoDialog(QDialog):
    def __init__(self, parent, matches, league, season, mode, week_number):
        super().__init__(parent)
        self.poisson = PoissonController()
        self.controller = TotoController()
        self.matches = matches
        self.league = league
        self.season = season
        self.mode = mode
        self.week_number = week_number
        self.radio_buttons = []
        self.radio_buttons_data = []
        self.toto_result = []

        # Dialog ui
        self.setWindowTitle("Heti totó")
        layout = QVBoxLayout()

        title = QLabel("A kiválasztott mérkőzések:")
        title.setStyleSheet("font-weight: bold; font-size: 18px;")
        leagueLbl = QLabel("Liga: " + self.league)
        seasonLbl = QLabel("Szezon: " + self.season)

        layout.addWidget(title)
        layout.addWidget(leagueLbl)
        layout.addWidget(seasonLbl)

        for m in matches:
            inner_layout = QHBoxLayout()
            button_group = QButtonGroup(self)
            elso = QLabel(m['HomeTeam'] + ' - ' + m['AwayTeam'])
            elso.setMinimumWidth(150)
            radio_h = QRadioButton("Hazai")
            button_group.addButton(radio_h)
            radio_d = QRadioButton("Döntetlen")
            button_group.addButton(radio_d)
            radio_v = QRadioButton("Vendég")
            button_group.addButton(radio_v)

            self.radio_buttons.append(radio_h)
            self.radio_buttons.append(radio_d)
            self.radio_buttons.append(radio_v)
            inner_layout.addWidget(elso)
            inner_layout.addWidget(radio_h)
            inner_layout.addWidget(radio_d)
            inner_layout.addWidget(radio_v)
            layout.addLayout(inner_layout)

        button_layout = QHBoxLayout()
        self.saveButton = QPushButton("Mentés")
        self.saveButton.resize(150, 50)
        cancelButton = QPushButton("Mégse")
        cancelButton.resize(150, 50)
        button_layout.addWidget(self.saveButton)
        button_layout.addWidget(cancelButton)
        layout.addLayout(button_layout)
        self.setLayout(layout)
        self.saveButton.clicked.connect(self.on_saveBtn_Clicked)
        cancelButton.clicked.connect(self.close)

    def on_saveBtn_Clicked(self):
        self.get_radio_buttons_data()

        if len(self.radio_buttons_data) != int(len(self.radio_buttons)/3):
            self.radiobutton_error()
        else:
            for i, m in enumerate(self.matches):
                match_for_toto = []
                self.matches[i]["Bet"] = 'H' if self.radio_buttons_data[
                    i] == 'Hazai' else 'D' if self.radio_buttons_data[i] == 'Döntetlen' else 'A'
                result = self.poisson.calculate_poisson(
                    m['HomeTeam'], m['AwayTeam'], self.mode)
                poisson = 'H' if result.home_winner_percents > result.draw_percents and result.home_winner_percents > result.away_winner_percents else 'D' if result.draw_percents > result.home_winner_percents and result.draw_percents > result.away_winner_percents else 'A'
                self.matches[i]['Mode'] = self.mode
                self.matches[i]["Poisson"] = poisson
                match_for_toto.append(self.week_number)
                match_for_toto.append(self.league)
                match_for_toto.append(self.season)
                match_for_toto.append(self.mode)
                match_datetime = m['Datetime'].strftime("%Y-%m-%d %H:%M:%S")
                match_for_toto.append(match_datetime)
                match_for_toto.append(m['HomeTeam'])
                match_for_toto.append(m['AwayTeam'])
                match_for_toto.append(m['FTHG'])
                match_for_toto.append(m['FTAG'])
                match_for_toto.append(m['FTR'])
                match_for_toto.append(m['Bet'])
                match_for_toto.append(m['Poisson'])
                self.toto_result.append(match_for_toto)

            is_ok = self.controller.insert_toto_result(self.toto_result)
            if is_ok:
                self.information_dialog()
            else:
                self.multiple_toto_error()

        self.radio_buttons_data = []

    def get_radio_buttons_data(self):
        for btn in self.radio_buttons:
            if btn.isChecked():
                self.radio_buttons_data.append(btn.text())

    def information_dialog(self):
        QMessageBox.information(
            self,
            "Információ dialog",
            "A szelvény sikeresen mentve."
        )

    def radiobutton_error(self):
        QMessageBox.critical(
            self,
            "Hiba",
            "Az összes eseményt ki kell választani."
        )

    def multiple_toto_error(self):
        QMessageBox.critical(
            self,
            "Hiba",
            "Ez a szelvény már létezik az adatbázisban."
        )
