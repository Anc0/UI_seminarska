from DataPreparation import DataPreparation
from NeuralNet import NeuralNet


class Simulation:

    def __init__(self):
        self.data = DataPreparation()
        self.ann = NeuralNet()
        self.teams = self.data.TEAMS
        self.groups = self.data.GROUPS
        self.games = self.data.MATCHES

    def simulate_game(self, home, away):
        home_score, away_score = self.ann.predict(home, away)
        home_team = [item for item in self.teams if item["id"] == home][0]
        away_team = [item for item in self.teams if item["id"] == away][0]
        print(home_team)
        print(away_team)
        home_team["goal_difference"] += home_score - away_score
        home_team["number_of_goals"] += home_score
        away_team["goal_difference"] += away_score - home_score
        away_team["number_of_goals"] += away_score
        if home_score == away_score:
            home_team["points"] += 1
            away_team["points"] += 1
            print("Draw")
        elif home_score > away_score:
            home_team["points"] += 3
            print("Home team wins.")
        elif home_score < away_score:
            away_team["points"] += 3
            print("Away team wins.")

    def simulate_tournament(self):
        current_game = 0
        game = self.games[current_game]
        # Group stage games simulation
        while game["stage"] == 1:
            self.simulate_game(game["home"], game["away"])

            current_game += 1
            game = self.games[current_game]
            pass
        # Determine first and second placed team in every group

        # Eight-finals simulation
        while game["stage"] == 2:

            current_game += 1
            game = self.games[current_game]
            pass
        # Quarter-finals simulation
        while game["stage"] == 3:

            current_game += 1
            game = self.games[current_game]
            pass
        # Semi-finals simulation
        while game["stage"] == 4:

            current_game += 1
            game = self.games[current_game]
            pass
        # Third place game simulation

        # Finals simulation
