import logging
import pandas as pd
from business.utils.constants import ANALYSIS_MODE_PREFIX
from business.utils.common import CommonUtil


class ExcelMatchResult:
    def __init__(self, home_team, away_team, home_goals, away_goals, home_team_rank, away_team_rank,
                 home_team_points, away_team_points, date, league, season, mode, poisson: any):
        self.log = logging.getLogger(__name__)
        self.home_team = home_team
        self.away_team = away_team
        self.home_goals = home_goals
        self.away_goals = away_goals
        self.home_team_rank = home_team_rank
        self.away_team_rank = away_team_rank
        self.home_team_points = home_team_points
        self.away_team_points = away_team_points
        self.date = date
        self.league = league
        self.season = season
        self.mode = mode
        self.poisson = poisson

    def write_to_excel(self) -> bool:
        try:
            with pd.ExcelWriter(f"./output/match_results/{self.home_team}-{self.away_team}_{CommonUtil.excel_datetime()}_{ANALYSIS_MODE_PREFIX[self.mode]}.xlsx", engine="xlsxwriter") as writer:
                # Configure data to excel
                league_data = pd.DataFrame({
                    f"{self.league} {self.season}": [self.home_team, self.away_team],
                    "Helyezés": [self.home_team_rank, self.away_team_rank],
                    "Pont": [self.home_team_points, self.away_team_points],
                    "Gól/meccs": [self.home_goals, self.away_goals]
                })

                mode_data = pd.DataFrame({
                    "Elemzési dátum": [self.date],
                    "Elemzési mód": [self.mode]
                })

                goal_numbers_data = pd.DataFrame({
                    self.home_team: self.poisson.home_goals_percents,
                    self.away_team: self.poisson.away_goals_percents
                }).rename_axis('Gólok száma', axis=1)

                over_under_data = pd.DataFrame({
                    'Over': self.poisson.goals_over_percents,
                    'Under': self.poisson.goals_under_percents
                }, index=(['0.5', '1.5', '2.5', '3.5', '4.5']))

                both_score_data = pd.DataFrame({
                    'Mindkét csapat szerez gólt': self.poisson.both_score
                }, index=['Igen', 'Nem'])

                without_goals_received_data = pd.DataFrame({
                    self.home_team: self.poisson.home_without_goals_received,
                    self.away_team: self.poisson.away_without_goals_received
                }, index=['Igen', 'Nem']).rename_axis('Kapott gól nélkül', axis=1)

                goal_matrix_away_team_name = pd.DataFrame({
                    self.away_team: [self.away_team]
                })

                goal_matrix_data = pd.DataFrame({
                    0: self.poisson.goal_matrix[0],
                    1: self.poisson.goal_matrix[1],
                    2: self.poisson.goal_matrix[2],
                    3: self.poisson.goal_matrix[3],
                    4: self.poisson.goal_matrix[4],
                    5: self.poisson.goal_matrix[5],
                }).rename_axis(self.home_team, axis=1)

                winning_chance_data = pd.DataFrame({
                    f'{self.home_team} győz': [self.poisson.home_winner_percents],
                    'Döntetlen': [self.poisson.draw_percents],
                    f'{self.away_team} győz': [self.poisson.away_winner_percents]
                })

                # Write data to excel
                league_data.to_excel(
                    writer, sheet_name="Meccs elemzés", index=False)

                goal_numbers_data.T.to_excel(
                    writer, sheet_name="Meccs elemzés", startcol=4)
                mode_data.T.to_excel(
                    writer, sheet_name="Meccs elemzés", startrow=4, header=False)
                over_under_data.T.to_excel(
                    writer, sheet_name="Meccs elemzés", startcol=4, startrow=4)
                both_score_data.T.to_excel(
                    writer, sheet_name="Meccs elemzés", startcol=4, startrow=8)
                without_goals_received_data.T.to_excel(
                    writer, sheet_name="Meccs elemzés", startcol=4, startrow=11)
                goal_matrix_away_team_name.to_excel(
                    writer, sheet_name="Meccs elemzés", startcol=4, startrow=15)
                goal_matrix_data.T.to_excel(
                    writer, sheet_name="Meccs elemzés", startcol=4, startrow=16)
                winning_chance_data.T.to_excel(
                    writer, sheet_name="Meccs elemzés", startcol=4, startrow=24, header=False)

                # Format excel
                workbook = writer.book
                worksheet = writer.sheets["Meccs elemzés"]
                percent_format = workbook.add_format({"num_format": "0.00%"})
                worksheet.set_column(5, 10, None, percent_format)
                worksheet.conditional_format(
                    1, 5, 2, 10, {"type": "3_color_scale"})
                worksheet.conditional_format(
                    5, 5, 6, 9, {"type": "3_color_scale"})
                worksheet.conditional_format(
                    9, 5, 9, 6, {"type": "3_color_scale"})
                worksheet.conditional_format(
                    12, 5, 13, 6, {"type": "3_color_scale"})
                worksheet.conditional_format(
                    17, 5, 22, 10, {"type": "3_color_scale"})
                worksheet.conditional_format(24, 5, 27, 5,
                                             {"type": "data_bar",
                                              "bar_color": "#63C384"})

            return True
        except:
            self.log.error("Error while writing Match result to Excel")
            return False
