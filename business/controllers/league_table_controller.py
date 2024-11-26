import logging
from business.utils.constants import LEAGUE_PREFIX, SEASON_PREFIX
from infrastructure.league_data import LeagueData
from infrastructure.sqlite_connect import SQLiteConnection


class LeagueTableController:
    def __init__(self):
        self.log = logging.getLogger(__name__)
        self.sql = SQLiteConnection()

    def calculate_table(self, league, season, league_date):
        try:
            _league = LEAGUE_PREFIX[league]
            _season = SEASON_PREFIX[season]
            data = LeagueData(_league, _season, league_date).calculate_table()
            return data
        except:
            self.log.error("Error while calculate_table!")

    def insert_league_standings(self, data):
        try:
            self.sql.insert_league_standings(data)
        except:
            self.log.error("Error while insert_league_standings!")

    def delete_all_teams(self):
        try:
            self.sql.delete_all_teams()
        except:
            self.log.error("Error while delete_all_teams!")
