import logging
from infrastructure.sqlite_connect import SQLiteConnection


class SinglePredictController:
    def __init__(self):
        self.log = logging.getLogger(__name__)
        self.sql = SQLiteConnection()

    def select_teams(self):
        try:
            data = self.sql.select_teams()
            return data
        except:
            self.log.error("Error while selecting all teams!")
