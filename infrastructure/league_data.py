import pandas as pd


class LeagueData:
    def __init__(self, league, season, date_time=None):
        self.load(league, season)
        if date_time:
            self.masking(date_time)

    def load(self, league, season):
        df = pd.read_csv(
            f'./infrastructure/storage/league_data/{league}_{season}.csv')
        df = df.iloc[:, 1:8]
        df['Date'] = pd.to_datetime(
            df['Date'], dayfirst=True).dt.strftime('%m-%d-%Y')
        col = pd.to_datetime(df['Date'].astype(
            str) + ' ' + df['Time'].astype(str))
        df.insert(loc=0, column='Datetime', value=col)
        df.drop(['Date'], axis=1, inplace=True)
        df.drop(['Time'], axis=1, inplace=True)
        self.teams = df['HomeTeam'].unique()
        self.df = df

    def calculate_table(self):
        table_data = {}

        for i in range(len(self.teams)):
            table_data["team_"+str(i)+"_played"] = 0
            table_data["team_"+str(i)+"_pts"] = 0
            table_data["team_"+str(i)+"_won"] = 0
            table_data["team_"+str(i)+"_drawn"] = 0
            table_data["team_"+str(i)+"_lost"] = 0
            table_data["team_"+str(i)+"_scored_goals"] = 0
            table_data["team_"+str(i)+"_conceded_goals"] = 0
            table_data["team_"+str(i)+"_goals_difference"] = 0
            table_data["team_"+str(i)+"_avg_goals"] = 0
            table_data["team_"+str(i)+"_avg_goals_5"] = 0
            table_data["team_"+str(i)+"_avg_goals_10"] = 0

        for _, row in self.df.iterrows():
            for i in range(len(self.teams)):
                table_data["team_"+str(i)+"_played"] += 1 if (row['HomeTeam']
                                                              == self.teams[i]) or (row['AwayTeam'] == self.teams[i]) else 0
                table_data["team_"+str(i)+"_pts"] += 3 if ((row['HomeTeam'] == self.teams[i] and row['FTR'] == 'H') or (row['AwayTeam'] == self.teams[i] and row['FTR']
                                                                                                                        == 'A')) else 1 if (row['HomeTeam'] == self.teams[i] and row['FTR'] == 'D' or row['AwayTeam'] == self.teams[i] and row['FTR'] == 'D') else 0
                table_data["team_"+str(i)+"_won"] += 1 if ((row['HomeTeam'] == self.teams[i] and row['FTR']
                                                            == 'H') or (row['AwayTeam'] == self.teams[i] and row['FTR'] == 'A')) else 0
                table_data["team_"+str(i)+"_drawn"] += 1 if (row['HomeTeam'] == self.teams[i] and row['FTR']
                                                             == 'D' or row['AwayTeam'] == self.teams[i] and row['FTR'] == 'D') else 0
                table_data["team_"+str(i)+"_lost"] += 1 if ((row['HomeTeam'] == self.teams[i] and row['FTR']
                                                             == 'A') or (row['AwayTeam'] == self.teams[i] and row['FTR'] == 'H')) else 0
                table_data["team_"+str(
                    i)+"_scored_goals"] += row['FTHG'] if row['HomeTeam'] == self.teams[i] else row['FTAG'] if row['AwayTeam'] == self.teams[i] else 0
                table_data["team_"+str(
                    i)+"_conceded_goals"] += row['FTAG'] if row['HomeTeam'] == self.teams[i] else row['FTHG'] if row['AwayTeam'] == self.teams[i] else 0
                table_data["team_"+str(i)+"_goals_difference"] = table_data["team_"+str(
                    i)+"_scored_goals"] - table_data["team_"+str(i)+"_conceded_goals"]
                if table_data["team_"+str(i)+"_scored_goals"] != 0:
                    table_data["team_"+str(i)+"_avg_goals"] = round(table_data["team_"+str(
                        i)+"_scored_goals"] / table_data["team_"+str(i)+"_played"], 2)

        for i in range(len(self.teams)):
            team_df = self.df[(self.df['HomeTeam'] == self.teams[i]) | (
                self.df['AwayTeam'] == self.teams[i])].tail(5)
            if len(team_df.index) >= 5:
                team_goal = 0
                for _, row in team_df.iterrows():
                    team_goal += row['FTHG'] if row['HomeTeam'] == self.teams[i] else row['FTAG'] if row['AwayTeam'] == self.teams[i] else 0
                table_data["team_" +
                           str(i)+"_avg_goals_5"] = round(team_goal / 5, 2)
            else:
                table_data["team_"+str(i)+"_avg_goals_5"] = 0

        for i in range(len(self.teams)):
            team_df = self.df[(self.df['HomeTeam'] == self.teams[i]) | (
                self.df['AwayTeam'] == self.teams[i])].tail(10)
            if len(team_df.index) >= 10:
                team_goal = 0
                for _, row in team_df.iterrows():
                    team_goal += row['FTHG'] if row['HomeTeam'] == self.teams[i] else row['FTAG'] if row['AwayTeam'] == self.teams[i] else 0
                table_data["team_" +
                           str(i)+"_avg_goals_10"] = round(team_goal / 10, 2)
            else:
                table_data["team_"+str(i)+"_avg_goals_10"] = 0

        data = []
        for i in range(len(self.teams)):
            data.append([
                self.teams[i],
                table_data["team_"+str(i)+"_played"],
                table_data["team_"+str(i)+"_pts"],
                table_data["team_"+str(i)+"_won"],
                table_data["team_"+str(i)+"_drawn"],
                table_data["team_"+str(i)+"_lost"],
                table_data["team_"+str(i)+"_scored_goals"],
                table_data["team_"+str(i)+"_conceded_goals"],
                table_data["team_"+str(i)+"_goals_difference"],
                table_data["team_"+str(i)+"_avg_goals"],
                table_data["team_"+str(i)+"_avg_goals_5"],
                table_data["team_"+str(i)+"_avg_goals_10"]
            ])

        # Sorting by points
        sorted_by_points = sorted(
            data, key=lambda i: (i[2], i[6]), reverse=True)
        return sorted_by_points

    def masking(self, given_date):
        start_date = self.df['Datetime'][0]
        end_date = pd.to_datetime(given_date + " 23:59", dayfirst=False)
        mask = (self.df['Datetime'] >= start_date) & (
            self.df['Datetime'] < end_date)
        self.df = self.df.loc[mask]

    def get_matches_on_date(self, given_date):
        start_date = pd.to_datetime(given_date + " 00:00", dayfirst=False)
        end_date = pd.to_datetime(given_date + " 23:59", dayfirst=False)
        mask = (self.df['Datetime'] >= start_date) & (
            self.df['Datetime'] <= end_date)
        matches = self.df.loc[mask]
        return matches


class TotoData:
    def __init__(self, league, season):
        self.load(league, season)

    def load(self, league, season):
        df = pd.read_csv(
            f'./infrastructure/storage/league_data/{league}_{season}.csv')
        df = df.iloc[:, 1:8]
        df['Date'] = pd.to_datetime(
            df['Date'], dayfirst=True).dt.strftime('%m-%d-%Y')
        col = pd.to_datetime(df['Date'].astype(
            str) + ' ' + df['Time'].astype(str))
        df.insert(loc=0, column='Datetime', value=col)
        df.drop(['Date'], axis=1, inplace=True)
        df.drop(['Time'], axis=1, inplace=True)
        self.teams = df['HomeTeam'].unique()
        self.df = df

    def get_matches_on_date(self, given_date):
        start_date = pd.to_datetime(given_date + " 00:00", dayfirst=False)
        end_date = pd.to_datetime(given_date + " 23:59", dayfirst=False)
        mask = (self.df['Datetime'] >= start_date) & (
            self.df['Datetime'] <= end_date)
        matches = self.df.loc[mask]
        return matches

    def get_matches_on_week(self, week):
        matches = []
        for day in week:
            x = self.get_matches_on_date(day)
            if not x.empty:
                matches.append(x)
        if matches:
            result = pd.concat(matches)
        else:
            result = pd.DataFrame()
        return result
