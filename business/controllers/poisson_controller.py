import logging
from business.controllers.plot_controller import ShowPlot
from infrastructure.sqlite_connect import SQLiteConnection
from business.analysis.poisson_analysis import PoissonAnalysis
from business.controllers.excel_controller import ExcelMatchResult


class PoissonController:
    def __init__(self):
        super().__init__()
        self.log = logging.getLogger(__name__)
        self.sql = SQLiteConnection()

    def calculate_poisson(self, home_team, away_team, mode) -> list:
        team_goals = self.get_team_goals(home_team, away_team, mode)
        result = PoissonAnalysis(team_goals[0], team_goals[1])
        return result

    def calculate_poisson_given_goals(self, home_goals, away_goals) -> list:
        result = PoissonAnalysis(home_goals, away_goals)
        return result

    def save_result_to_sql(self, date: str, home_team_name, away_team_name, league, season, mode):
        home_team = self.sql.select_team(home_team_name)
        away_team = self.sql.select_team(away_team_name)
        match mode:
            case "Szezon átlag":
                result = PoissonAnalysis(
                    home_team.avg_goals, away_team.avg_goals)
                h_goals = home_team.avg_goals
                a_goals = away_team.avg_goals
            case "Utolsó 5":
                result = PoissonAnalysis(home_team.avg_5, away_team.avg_5)
                h_goals = home_team.avg_5
                a_goals = away_team.avg_5
            case "Utolsó 10":
                result = PoissonAnalysis(home_team.avg_10, away_team.avg_10)
                h_goals = home_team.avg_10
                a_goals = away_team.avg_10
            case _:
                result = 0
                h_goals = 0
                a_goals = 0

        data = (
            tuple([
                date,
                league,
                season,
                home_team.name,
                away_team.name,
                h_goals,
                a_goals,
                home_team.rank,
                away_team.rank,
                home_team.pts,
                away_team.pts,
            ])
            + tuple([
                round(result.home_winner_percents, 2),
                round(result.draw_percents, 2),
                round(result.away_winner_percents, 2),
                mode
            ])
        )
        self.sql.insert_poisson_result(data)

    def save_to_excel(self, home_team, away_team, league, season, date, mode):
        home_team = self.sql.select_team(home_team)
        away_team = self.sql.select_team(away_team)
        team_goals = self.get_team_goals(home_team.name, away_team.name, mode)
        home_goals = team_goals[0]
        away_goals = team_goals[1]
        poisson_result = self.calculate_poisson_given_goals(
            home_goals, away_goals)

        is_excel_ok = ExcelMatchResult(
            home_team.name,
            away_team.name,
            home_goals,
            away_goals,
            home_team.rank,
            away_team.rank,
            home_team.pts,
            away_team.pts,
            date,
            league,
            season,
            mode,
            poisson_result).write_to_excel()

        return is_excel_ok

    def save_to_excel_from_result(self, data):
        poisson_result = self.calculate_poisson_given_goals(data[6], data[7])

        is_excel_ok = ExcelMatchResult(
            data[4],
            data[5],
            data[6],
            data[7],
            data[8],
            data[9],
            data[10],
            data[11],
            data[1],
            data[2],
            data[3],
            data[15],
            poisson_result).write_to_excel()

        return is_excel_ok

    def show_result_plot(self, home_team, away_team, mode):
        poisson_result = self.calculate_poisson(home_team, away_team, mode)
        ShowPlot(home_team, away_team, poisson_result)

    def show_result_plot_goal_given(self, home_team, away_team, home_goal, away_goal):
        poisson_result = PoissonAnalysis(home_goal, away_goal)
        ShowPlot(home_team, away_team, poisson_result)

    def get_data_for_dialog(self, poisson_id):
        data = self.sql.select_poisson_result_for_dialog(poisson_id)
        return data

    def get_team_goals(self, home_team, away_team, mode):
        match mode:
            case "Szezon átlag":
                home_goals = self.sql.select_avg_goals_per_game(home_team)[0]
                away_goals = self.sql.select_avg_goals_per_game(away_team)[0]
            case "Utolsó 5":
                home_goals = self.sql.select_avg_5_goals_per_game(home_team)[0]
                away_goals = self.sql.select_avg_5_goals_per_game(away_team)[0]
            case "Utolsó 10":
                home_goals = self.sql.select_avg_10_goals_per_game(home_team)[
                    0]
                away_goals = self.sql.select_avg_10_goals_per_game(away_team)[
                    0]
            case _:
                home_goals = 0
                away_goals = 0

        return [home_goals, away_goals]
