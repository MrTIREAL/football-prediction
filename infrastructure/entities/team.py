class Team:
    def __init__(self, name, rank, pts, avg_goals, avg_5, avg_10):
        self._team = []
        self.name = name
        self.rank = rank
        self.pts = pts
        self.avg_goals = avg_goals
        self.avg_5 = avg_5
        self.avg_10 = avg_10

    def __str__(self):
        return f"[{self.rank}] {self.name} - {self.pts} {self.avg_goals}"

    def __len__(self):
        return len(self._team)

    def __getitem__(self, key):
        return self._team[key]
