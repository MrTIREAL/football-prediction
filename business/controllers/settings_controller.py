import logging
from infrastructure.sqlite_connect import SQLiteConnection


class SettingsController:
    def __init__(self):
        self.log = logging.getLogger(__name__)
        self.sql = SQLiteConnection()

    def update_selected_date(self, date: str):
        try:
            self.sql.update_selected_date(date)
        except:
            self.log.error("Error while updating selected date!")

    def get_selected_date(self):
        try:
            selected_date = self.sql.select_selected_date()
            return selected_date
        except:
            self.log.error("Error while getting selected date!")

    def get_selected_year(self):
        try:
            selected_year = self.sql.select_selected_date()
            return selected_year[:4]
        except:
            self.log.error("Error while getting selected year!")

    def get_selected_month(self):
        try:
            selected_month = self.sql.select_selected_date()
            return selected_month[5:7]
        except:
            self.log.error("Error while getting selected month!")

    def get_current_league(self):
        try:
            data = self.sql.select_current_league()
            return data
        except:
            self.log.error("Error while selecting current league!")

    def get_current_season(self):
        try:
            data = self.sql.select_current_season()
            return data
        except:
            self.log.error("Error while selecting current season!")

    def update_current_season(self, season: str):
        try:
            self.sql.update_current_season(season)
        except:
            self.log.error("Error while updating current season!")

    def update_current_league(self, league: str):
        try:
            self.sql.update_current_league(league)
        except:
            self.log.error("Error while updating current league!")

    def get_current_mode(self):
        try:
            data = self.sql.select_current_mode()
            return data
        except:
            self.log.error("Error while selecting current mode!")

    def update_current_mode(self, mode: str):
        try:
            self.sql.update_current_mode(mode)
        except:
            self.log.error("Error while updating current mode!")
