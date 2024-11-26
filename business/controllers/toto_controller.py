import logging
from business.utils.constants import LEAGUE_PREFIX, SEASON_PREFIX
from infrastructure.league_data import TotoData
from infrastructure.sqlite_connect import SQLiteConnection


class TotoController:
    def __init__(self):
        self.log = logging.getLogger(__name__)
        self.sql = SQLiteConnection()

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
            self.log.error("Error while getting selected date!")

    def get_toto_data(self, league, season):
        try:
            data = TotoData(LEAGUE_PREFIX[league], SEASON_PREFIX[season])
            return data
        except:
            self.log.error("Error while getting toto data!")

    def select_toto_result_for_view(self):
        try:
            data = self.sql.select_toto_result_for_view()
            return data
        except:
            self.log.error("Error while select_toto_result_for_view!")

    def select_toto_result_for_week(self, week, league, season, mode):
        try:
            data = self.sql.select_toto_result_for_week(
                week, league, season, mode)
            return data
        except:
            self.log.error("Error while select_toto_result_for_week!")

    def insert_toto_result(self, data):
        try:
            data = self.sql.insert_toto_result(data)
            return data
        except:
            self.log.error("Error while inserting toto result!")

    def delete_toto_result(self, model_data):
        try:
            data = self.sql.delete_toto_result(model_data)
            return data
        except:
            self.log.error("Error while deleting toto result!")
