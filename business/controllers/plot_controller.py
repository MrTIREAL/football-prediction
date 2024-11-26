from matplotlib.ticker import PercentFormatter
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


class ShowPlot:

    def __init__(self, home_team, away_team, poisson: any):
        self.home_team = home_team
        self.away_team = away_team
        self.poisson = poisson
        fig, axs = None, None
        self._initialize()

    def _initialize(self):
        self.fig, self.axs = plt.subplot_mosaic([['ax1', 'ax1', 'ax6', 'ax6'],
                                                 ['ax2', 'ax2', 'ax5', 'ax5'],
                                                 ['ax3', 'ax4', 'ax5', 'ax5']], figsize=(12, 10))
        self.show_resuls_plot()

    def create_goal_scoring_plot(self):
        matrix = pd.DataFrame.from_dict({
            self.home_team: self.poisson.home_goals_percents,
            self.away_team: self.poisson.away_goals_percents
        },
            orient='index', columns=["0", "1", "2", "3", "4", "5"])

        sns.heatmap(matrix, cmap="rocket", vmin=0, vmax=1, annot=True,
                    fmt=".2%", square=True, linewidths=.5, ax=self.axs['ax1'])

    def create_over_under_plot(self):
        matrix = pd.DataFrame.from_dict({
            "Over": self.poisson.goals_over_percents,
            "Under": self.poisson.goals_under_percents
        },
            orient='index', columns=["0.5", "1.5", "2.5", "3.5", "4.5"])

        sns.heatmap(matrix, cmap="mako", vmin=0, vmax=1, annot=True,
                    fmt=".2%", square=True, linewidths=.5, ax=self.axs['ax2'])

    def create_both_scoring(self):
        matrix = pd.DataFrame.from_dict({
            "Both": self.poisson.both_score
        }, orient="index", columns=["Yes", "No"])

        sns.heatmap(matrix, cmap="mako", vmin=0, vmax=1, annot=True,
                    fmt=".2%", square=True, linewidths=.5, ax=self.axs['ax3'])

    def create_without_goal_conceded(self):
        matrix = pd.DataFrame.from_dict({
            self.home_team: self.poisson.home_without_goals_received,
            self.away_team: self.poisson.away_without_goals_received
        },
            orient='index', columns=["Yes", "No"])

        sns.heatmap(matrix, cmap="mako", vmin=0, vmax=1, annot=True,
                    fmt=".2%", square=True, linewidths=.5, ax=self.axs['ax4'])

    def create_goal_matrix(self):
        matrix = pd.DataFrame.from_dict({
            "0": self.poisson.goal_matrix[0],
            "1": self.poisson.goal_matrix[1],
            "2": self.poisson.goal_matrix[2],
            "3": self.poisson.goal_matrix[3],
            "4": self.poisson.goal_matrix[4],
            "5": self.poisson.goal_matrix[5]
        },
            orient='index', columns=["0", "1", "2", "3", "4", "5"])

        sns.heatmap(matrix, cmap="rocket", vmin=0, vmax=0.25,
                    annot=True, fmt=".2%", square=True, ax=self.axs['ax5'])

    def create_winner_plot(self):
        result_dict = {
            self.home_team: self.poisson.home_winner_percents,
            "Draw": self.poisson.draw_percents,
            self.away_team: self.poisson.away_winner_percents
        }

        for r in result_dict:
            result_dict[r] = float(result_dict[r])

        total = sum(result_dict.values())
        self.axs['ax6'].bar(result_dict.keys(), [
                            v/total for v in result_dict.values()])
        self.axs['ax6'].yaxis.set_major_formatter(
            PercentFormatter(xmax=1, decimals=0))

    def show_resuls_plot(self):
        self.fig.tight_layout(pad=1.2)
        self.create_goal_scoring_plot()
        self.create_over_under_plot()
        self.create_both_scoring()
        self.create_without_goal_conceded()
        self.create_goal_matrix()
        self.create_winner_plot()
        self.axs['ax1'].title.set_text('Number of Goals')
        self.axs['ax2'].title.set_text('Over/Under of Goals')
        self.axs['ax3'].title.set_text('Both Team Scoring')
        self.axs['ax4'].title.set_text('Without Goals conceded')
        self.axs['ax5'].title.set_text('Goal matrix')
        self.axs['ax5'].set_ylabel(self.home_team, fontsize=15)
        self.axs['ax5'].set_xlabel(self.away_team, fontsize=15)
        plt.show()
