import sqlite3
import logging
import logging.config
from infrastructure.entities import team


class SQLiteConnection:

    def __init__(self):
        self.connection = sqlite3.connect(
            "infrastructure/storage/football.db",
            check_same_thread=False
        )
        self.log = logging.getLogger(__name__)

    def create_league_standings_table(self):
        cursor = self.connection.cursor()
        try:
            cursor.execute(f"""CREATE TABLE league_standings (
                           team_name TEXT, played INTEGER, points INTEGER,
                           won INTEGER, draw INTEGER, lost INTEGER, gf INTEGER, ga INTEGER, gd INTEGER,
                           avg REAL, avg_5 REAL, avg_10 REAL,
                           UNIQUE (team_name)
                           )""")
            self.log.info(f"league_standings table created.")
        except sqlite3.Error as err:
            self.log.error(err)
        finally:
            cursor.close()

    def create_user_data_table(self):
        cursor = self.connection.cursor()
        try:
            cursor.execute(f"""CREATE TABLE user_data (
                           user_id INTEGER PRIMARY KEY, current_league TEXT, current_season TEXT, current_mode TEXT, selected_date TEXT,
                           UNIQUE (user_id)
                           )""")
            self.log.info(f"user_data table created.")
        except sqlite3.Error as err:
            self.log.error(err)
        finally:
            cursor.close()

    def create_toto_table(self):
        cursor = self.connection.cursor()
        try:
            cursor.execute(f"""CREATE TABLE toto_table (
                           toto_id INTEGER PRIMARY KEY, week INTEGER, current_league TEXT, current_season TEXT, current_mode TEXT, datetime TEXT,
                           home_team TEXT, away_team TEXT, home_goals INTEGER, away_goals INTEGER, result TEXT, bet TEXT, poisson TEXT,
                           UNIQUE (toto_id),
                           CONSTRAINT unq UNIQUE (week, current_league, current_season, current_mode, home_team, away_team)
                           )""")
            self.log.info(f"toto_table created.")
        except sqlite3.Error as err:
            self.log.error(err)
        finally:
            cursor.close()

    def create_poisson_results_table(self):
        cursor = self.connection.cursor()
        try:
            cursor.execute(f"""CREATE TABLE poisson_results (
                            pr_id INTEGER PRIMARY KEY,
                            date TEXT, league TEXT, season TEXT,
                            home_team TEXT, away_team TEXT, home_goals REAL, away_goals REAL,
                            home_team_rank TEXT, away_team_rank TEXT,
                            home_team_points INTEGER, away_team_points INTEGER,
                            home_winner REAL, draw REAL, away_winner REAL, mode TEXT,
                            UNIQUE (pr_id)
                            )""")
            self.log.info(f"poisson_results table created.")
        except sqlite3.Error as err:
            self.log.error(err)
        finally:
            cursor.close()

    def insert_user_data(self, current_league, current_season, current_mode, selected_date):
        cursor = self.connection.cursor()
        data = [1, current_league, current_season, current_mode, selected_date]
        try:
            sql = """INSERT INTO user_data
                     VALUES (?, ?, ?, ?, ?)"""
            cursor.execute(sql, data)
            self.connection.commit()
            self.log.info(f"Inserting User data executed.")
        except sqlite3.Error as err:
            self.log.error(err)
        finally:
            cursor.close()

    def update_selected_date(self, data: str):
        cursor = self.connection.cursor()
        try:
            sql = """UPDATE user_data SET
            selected_date = ? WHERE user_id = 1"""
            cursor.execute(sql, [data])
            self.connection.commit()
            self.log.info(f"Updating user_data executed.")
        except sqlite3.Error as err:
            self.log.error(err)
            self.connection.rollback()
        finally:
            cursor.close()

    def select_selected_date(self):
        cursor = self.connection.cursor()
        try:
            cursor.execute(f"SELECT selected_date from user_data")
            data = cursor.fetchall()
            return data[0][0]
        except sqlite3.Error as err:
            self.log.error(err)
        finally:
            cursor.close()

    def update_current_league(self, data: str):
        cursor = self.connection.cursor()
        try:
            sql = """UPDATE user_data SET
            current_league = ? WHERE user_id = 1"""
            cursor.execute(sql, [data])
            self.connection.commit()
            self.log.info(f"Updating current league in user_data table executed.")
        except sqlite3.Error as err:
            self.log.error(err)
            self.connection.rollback()
        finally:
            cursor.close()

    def update_current_mode(self, data: str):
        cursor = self.connection.cursor()
        try:
            sql = """UPDATE user_data SET
            current_mode = ? WHERE user_id = 1"""
            cursor.execute(sql, [data])
            self.connection.commit()
            self.log.info(f"Updating current mode in user_data table executed.")
        except sqlite3.Error as err:
            self.log.error(err)
            self.connection.rollback()
        finally:
            cursor.close()

    def select_current_mode(self):
        cursor = self.connection.cursor()
        try:
            cursor.execute(f"SELECT current_mode from user_data")
            data = cursor.fetchone()
            return data[0]
        except sqlite3.Error as err:
            self.log.error(err)
        finally:
            cursor.close()

    def select_current_league(self):
        cursor = self.connection.cursor()
        try:
            cursor.execute(f"SELECT current_league from user_data")
            data = cursor.fetchone()
            return data[0]
        except sqlite3.Error as err:
            self.log.error(err)
        finally:
            cursor.close()

    def update_current_season(self, data: str):
        cursor = self.connection.cursor()
        try:
            sql = """UPDATE user_data SET
            current_season = ? WHERE user_id = 1"""
            cursor.execute(sql, [data])
            self.connection.commit()
            self.log.info(f"Updating current_season in user_data table executed.")
        except sqlite3.Error as err:
            self.log.error(err)
            self.connection.rollback()
        finally:
            cursor.close()

    def select_current_season(self):
        cursor = self.connection.cursor()
        try:
            cursor.execute(f"SELECT current_season from user_data")
            data = cursor.fetchall()
            return data[0][0]
        except sqlite3.Error as err:
            self.log.error(err)
        finally:
            cursor.close()

    def insert_league_standings(self, data: list):
        cursor = self.connection.cursor()
        try:
            sql = """INSERT INTO league_standings VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
            cursor.executemany(sql, data)
            self.connection.commit()
            self.log.info(f"Inserting league_standings executed.")
        except sqlite3.Error as err:
            self.log.error(err)
            self.connection.rollback()
        finally:
            cursor.close()

    def delete_all_teams(self):
        cursor = self.connection.cursor()
        try:
            sql = """DELETE FROM league_standings"""
            cursor.execute(sql)
            self.connection.commit()
            self.log.info(f"Delete all data from league_standings executed.")
        except sqlite3.Error as err:
            self.log.error(err)
            self.connection.rollback()
        finally:
            cursor.close()

    def select_teams(self):
        cursor = self.connection.cursor()
        try:
            cursor.execute(f"SELECT team_name from league_standings")
            data = cursor.fetchall()
            return data
        except sqlite3.Error as err:
            self.log.error(err)
        finally:
            cursor.close()

    def select_avg_goals_per_game(self, team_name: str) -> float:
        cursor = self.connection.cursor()
        try:
            cursor.execute(
                """SELECT avg from league_standings where team_name = ?""", [team_name])
            self.log.info(f"Select avg for team: {team_name} executed.")
            return cursor.fetchone()
        except sqlite3.Error as err:
            self.log.error(err)
        finally:
            cursor.close()

    def select_avg_5_goals_per_game(self, team_name: str) -> float:
        cursor = self.connection.cursor()
        try:
            cursor.execute(
                """SELECT avg_5 from league_standings where team_name = ?""", [team_name])
            self.log.info(f"Select avg_5 for team: {team_name} executed.")
            return cursor.fetchone()
        except sqlite3.Error as err:
            self.log.error(err)
        finally:
            cursor.close()

    def select_avg_10_goals_per_game(self, team_name: str) -> float:
        cursor = self.connection.cursor()
        try:
            cursor.execute(
                """SELECT avg_10 from league_standings where team_name = ?""", [team_name])
            self.log.info(f"Select avg_10 for team: {team_name} executed.")
            return cursor.fetchone()
        except sqlite3.Error as err:
            self.log.error(err)
        finally:
            cursor.close()

    def select_team(self, team_name: str) -> team.Team:
        cursor = self.connection.cursor()
        try:
            cursor.execute(
                """SELECT team_name, ROWID, points, avg, avg_5, avg_10 from league_standings where team_name = ?""", [team_name])
            team_details = cursor.fetchone()
            self.log.info(f"Create model for: {team_details[0]} executed.")
            return team.Team(
                name=team_details[0],
                rank=team_details[1],
                pts=team_details[2],
                avg_goals=team_details[3],
                avg_5=team_details[4],
                avg_10=team_details[5]
            )
        except sqlite3.Error as err:
            self.log.error(err)
        finally:
            cursor.close()

    def insert_poisson_result(self, data: tuple):
        cursor = self.connection.cursor()
        try:
            sql = """INSERT INTO poisson_results (
                        date, league, season,
                        home_team, away_team, home_goals, away_goals,
                        home_team_rank, away_team_rank, home_team_points, away_team_points,
                        home_winner, draw, away_winner, mode
                        ) VALUES (
                        ?, ?, ?,
                        ?, ?, ?, ?,
                        ?, ?, ?, ?,
                        ?, ?, ?, ?
                        )"""
            cursor.execute(sql, data)
            self.connection.commit()
            self.log.info(f"Inserting poisson_results executed.")
        except sqlite3.Error as err:
            self.log.error(err)
            self.connection.rollback()
        finally:
            cursor.close()

    def select_poisson_result(self) -> list:
        cursor = self.connection.cursor()
        try:
            cursor.execute(f"SELECT * from poisson_results")
            return cursor.fetchall()
        except sqlite3.Error as err:
            self.log.error(err)
        finally:
            cursor.close()

    def select_poisson_result_for_view(self) -> list:
        cursor = self.connection.cursor()
        try:
            cursor.execute("""SELECT pr_id, date, league, season, home_team, away_team, home_goals, away_goals,
                           home_winner, draw, away_winner, mode from poisson_results""")
            return cursor.fetchall()
        except sqlite3.Error as err:
            self.log.error(err)
        finally:
            cursor.close()

    def select_poisson_result_for_dialog(self, pr_id: int) -> list:
        cursor = self.connection.cursor()
        try:
            cursor.execute(
                """SELECT * from poisson_results WHERE pr_id = ?""", [pr_id])
            return cursor.fetchone()
        except sqlite3.Error as err:
            self.log.error(err)
        finally:
            cursor.close()

    def delete_poisson_result(self, id: int):
        cursor = self.connection.cursor()
        try:
            sql = """DELETE FROM poisson_results WHERE pr_id = ?"""
            cursor.execute(sql, [id])
            self.connection.commit()
            self.log.info(f"Delete from poisson_results executed.")
        except sqlite3.Error as err:
            self.log.error(err)
            self.connection.rollback()
        finally:
            cursor.close()

    def insert_toto_result(self, data: list):
        cursor = self.connection.cursor()
        try:
            sql = """INSERT INTO toto_table (
                week, current_league, current_season, current_mode, datetime,
                home_team, away_team, home_goals, away_goals, result, bet, poisson
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
            cursor.executemany(sql, data)
            self.connection.commit()
            self.log.info(f"Inserting data into toto_table executed.")
            return True
        except sqlite3.Error as err:
            self.log.error(err)
            self.connection.rollback()
            return False
        finally:
            cursor.close()

    def select_toto_result_for_view(self) -> list:
        cursor = self.connection.cursor()
        try:
            cursor.execute("""SELECT week, current_league, current_season, current_mode, datetime from toto_table tt GROUP BY current_league, current_season, current_mode
                           ORDER BY datetime, week""")
            return cursor.fetchall()
        except sqlite3.Error as err:
            self.log.error(err)
        finally:
            cursor.close()

    def select_toto_result_for_week(self, week, league, season, mode) -> list:
        cursor = self.connection.cursor()
        try:
            cursor.execute(
                """SELECT * from toto_table WHERE week = ? and current_league = ? and current_season = ? and current_mode = ? ORDER BY datetime""", [week, league, season, mode])
            return cursor.fetchall()
        except sqlite3.Error as err:
            self.log.error(err)
        finally:
            cursor.close()

    def delete_toto_result(self, model_data):
        cursor = self.connection.cursor()
        try:
            sql = """DELETE FROM toto_table WHERE week = ? and current_league = ? and current_season = ? and current_mode = ?"""
            cursor.execute(
                sql, [model_data[0], model_data[1], model_data[2], model_data[3]])
            self.connection.commit()
            self.log.info(f"Delete selected data from toto result executed.")
        except sqlite3.Error as err:
            self.log.error(err)
            self.connection.rollback()
        finally:
            cursor.close()
