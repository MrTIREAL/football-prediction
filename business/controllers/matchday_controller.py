import logging
from business.utils.constants import LEAGUE_PREFIX, SEASON_PREFIX
from infrastructure.league_data import LeagueData
from infrastructure.sqlite_connect import SQLiteConnection


class MatchdayController:
    def __init__(self):
        self.log = logging.getLogger(__name__)
        self.sql = SQLiteConnection()

    def get_matches_on_date(self, league, season, selected_date):
        try:
            _league = LEAGUE_PREFIX[league]
            _season = SEASON_PREFIX[season]
            league_data = LeagueData(_league, _season)
            data = league_data.get_matches_on_date(selected_date)
            return data
        except:
            self.log.error("Error while get_matches_on_date!")

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
