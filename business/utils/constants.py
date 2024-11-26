LEAGUES = ["Premier League", "Serie A", "Bundesliga", "La Liga", "Ligue 1"]
SEASONS = ["24/25", "23/24", "22/23"]
ANALYSIS_MODES = ["Szezon átlag", "Utolsó 5", "Utolsó 10"]
WEBSITE_URL = 'https://www.football-data.co.uk/mmz4281/2425/'

LEAGUE_PREFIX = {
    "Premier League": "E0",
    "Serie A": "I1",
    "Bundesliga": "D1",
    "La Liga": "SP1",
    "Ligue 1": "F1"
}

SEASON_PREFIX = {
    "24/25": "2024_2025",
    "23/24": "2023_2024",
    "22/23": "2022_2023"
}

CONSTS = {
    'GOAL_NUMBERS': 6,
    'GOAL_OVER_UNDER': 5
}

ANALYSIS_MODE_PREFIX = {
    "Szezon átlag": "avg",
    "Utolsó 5": "avg_5",
    "Utolsó 10": "avg_10"
}

LEAGUE_URL = {
    "Premier League": "englandm.php",
    "Serie A": "italym.php"
}

LANGUAGE = {
    'HU': './business/utils/hu.json',
    'EN': './business/utils/en.json'
}
