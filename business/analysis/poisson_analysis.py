import numpy as np
from scipy.stats import poisson
from business.utils.constants import CONSTS


class PoissonAnalysis:

    def __init__(self, home_goals: float, away_goals: float):
        self.home_goals = home_goals
        self.away_goals = away_goals
        self.all_goals = home_goals + away_goals
        self.home_goals_percents = []
        self.away_goals_percents = []
        self.goals_under_percents = []
        self.goals_over_percents = []
        self.both_score = []
        self.home_without_goals_received = []
        self.away_without_goals_received = []
        self.goal_matrix = []
        self.home_winner_percents = None
        self.draw_percents = None
        self.away_winner_percents = None
        self._calculate()

    def _calculate(self):
        self._calculate_goal_numbers()
        self._calculate_over_under_goals()
        self._calculate_both_score()
        self._calculate_without_goals_received()
        self._calculate_goal_matrix()

    def _calculate_goal_numbers(self):
        for i in range(CONSTS['GOAL_NUMBERS']):
            x = poisson.pmf(k=i, mu=self.home_goals)
            y = poisson.pmf(k=i, mu=self.away_goals)
            self.home_goals_percents.append(float(x))
            self.away_goals_percents.append(float(y))

    def _calculate_over_under_goals(self):
        for i in range(CONSTS['GOAL_OVER_UNDER']):
            x = poisson.cdf(k=i, mu=self.all_goals)
            y = 1 - x
            self.goals_under_percents.append(float(x))
            self.goals_over_percents.append(float(y))

    def _calculate_both_score(self):
        both_score_goal_positive = float(
            (1-self.home_goals_percents[0])
            * (1-self.away_goals_percents[0]))
        self.both_score.extend(
            [both_score_goal_positive,
             (1-both_score_goal_positive)])

    def _calculate_without_goals_received(self):
        self.home_without_goals_received.append(
            self.away_goals_percents[0])
        self.home_without_goals_received.append(
            float(1 - self.away_goals_percents[0]))

        self.away_without_goals_received.append(
            self.home_goals_percents[0])
        self.away_without_goals_received.append(
            float(1 - self.home_goals_percents[0]))

    def _calculate_goal_matrix(self):
        self.goal_matrix = [[float(i * j) for j in self.away_goals_percents]
                            for i in self.home_goals_percents]
        self.home_winner_percents = float(
            np.tril(self.goal_matrix).sum()-np.trace(self.goal_matrix))
        self.draw_percents = float(np.trace(self.goal_matrix))
        self.away_winner_percents = float(
            np.triu(self.goal_matrix).sum()-np.trace(self.goal_matrix))
