from random import randint

from DataPreparation import DataPreparation
from NeuralNet import NeuralNet


class Simulation:

    def __init__(self):
        self.data = DataPreparation()
        self.ann = NeuralNet()
        self.teams = self.data.TEAMS
        self.groups = self.data.GROUPS
        self.games = self.data.MATCHES

    def simulate_game_group(self, home, away):
        """
        Get teams via id, predict the score and update necessary statistics.
        :param home: home team id
        :param away: away team id
        """
        # Predict the score
        home_score, away_score = self.ann.predict(home, away)
        # Get the teams
        home_team = self.get_team(home)
        away_team = self.get_team(away)
        # Update total goals scored and goal difference
        home_team["goal_difference"] += home_score - away_score
        home_team["number_of_goals"] += home_score
        away_team["goal_difference"] += away_score - home_score
        away_team["number_of_goals"] += away_score
        # Add points according to the score
        if home_score == away_score:
            home_team["points"] += 1
            away_team["points"] += 1
        elif home_score > away_score:
            home_team["points"] += 3
        elif home_score < away_score:
            away_team["points"] += 3

    def set_advancing_teams(self):
        """
        Set first and second team in every group after group stage.
        """
        for group in self.groups:
            teams = [self.get_team(team) for team in group["teams"]]
            order = sorted(teams, key=lambda x: (x["points"], x["goal_difference"], x["number_of_goals"]),
                           reverse=True)
            group["first"] = order[0]["id"]
            group["second"] = order[1]["id"]

    def simulate_game_knockout(self, home, away):
        """
        Get the teams via id and predict the winner of the game. If the score is tied, pick a winner at random.
        :param home: home team id
        :param away: away team id
        :return: game winner
        """
        # Predict the score
        home_score, away_score = self.ann.predict(home, away)
        # Return the winners id
        if home_score > away_score:
            return home
        elif home_score < away_score:
            return away
        elif home_score == away_score:
            if randint(0, 1) == 0:
                return home
            else:
                return away

    def determine_knockout_pairs(self):
        """
        Set teams for stage 2.
        """
        eight_finals = [item for item in self.games if item["stage"] == 2]
        for pair in eight_finals:
            pair["home"] = [item["first"] for item in self.groups if item["id"] == pair["home"][1]][0]
            pair["away"] = [item["second"] for item in self.groups if item["id"] == pair["away"][1]][0]
        for x in self.games:
            print(x)

    def set_progressor(self, match_id, progressor):
        """
        Set opponents for the next stage.
        Find the game where the home or away team corresponds
        to match id and put the progressor (team id) on that spot.
        :param match_id: id of the current match played
        :param progressor: id of the winning team
        :param stage: current stage of the tournament
        """
        game = [item for item in self.games if item["stage"] > 2 and int(item["home"][1:3]) == match_id]
        if len(game) > 0:
            game[0]["home"] = progressor
            return
        game = [item for item in self.games if item["stage"] > 2 and int(item["away"][1:3]) == match_id]
        if len(game) > 0:
            game[0]["away"] = progressor
            return
        raise Exception("No match found")



    def simulate_tournament(self):
        current_game = 0
        game = self.games[current_game]
        # Group stage games simulation
        while game["stage"] == 1:
            self.simulate_game_group(game["home"], game["away"])
            current_game += 1
            game = self.games[current_game]
        # Determine first and second placed team in every group
        self.set_advancing_teams()
        # Set stage 2 matches with appropriate team ids
        self.determine_knockout_pairs()
        # Eight-finals simulation
        while game["stage"] == 2:
            # Get game winner
            progressor = self.simulate_game_knockout(game["home"], game["away"])
            # Set the game winner in the next round
            self.set_progressor(game["id"], progressor)
            current_game += 1
            game = self.games[current_game]
            pass
        for x in self.games:
            print(x)
        # Quarter-finals simulation
        """while game["stage"] == 3:

            current_game += 1
            game = self.games[current_game]
            pass
        # Semi-finals simulation
        while game["stage"] == 4:

            current_game += 1
            game = self.games[current_game]
            pass
        # Third place game simulation

        # Finals simulation"""

    # Helper functions
    def get_team(self, team_id):
        """
        Return team according to the input parameter.
        :param id: team id
        :return: team
        """
        return [item for item in self.teams if item["id"] == team_id][0]

if __name__ == "__main__":
    s = Simulation()
    s.simulate_tournament()
