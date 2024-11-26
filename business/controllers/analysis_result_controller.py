import logging
from infrastructure.sqlite_connect import SQLiteConnection


class AnalysisResultController:
    def __init__(self):
        self.log = logging.getLogger(__name__)
        self.sql = SQLiteConnection()

    def select_poisson_result_for_view(self):
        try:
            data = self.sql.select_poisson_result_for_view()
            return data
        except:
            self.log.error(
                "Error while selecting poisson_result_for_view!")

    def delete_poisson_result(self, model_id):
        try:
            data = self.sql.delete_poisson_result(model_id)
            return data
        except:
            self.log.error("Error while deleting poisson result!")
