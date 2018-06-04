from random import randint
from time import sleep

from DataPreparation import DataPreparation
from NeuralNet import NeuralNet


class Simulation:

    def __init__(self):
        self.data = DataPreparation()
        self.ann = NeuralNet()
        self.teams = self.data.TEAMS
        self.groups = self.data.GROUPS
        self.games = self.data.MATCHES
        self.print_counter = 0
        self.quarter_final_couner = 16
        self.print_array = [
            {"name": "", "score": ""},
            {"name": "", "score": ""},
            {"name": "", "score": ""},
            {"name": "", "score": ""},
            {"name": "", "score": ""},
            {"name": "", "score": ""},
            {"name": "", "score": ""},
            {"name": "", "score": ""},
            {"name": "", "score": ""},
            {"name": "", "score": ""},
            {"name": "", "score": ""},
            {"name": "", "score": ""},
            {"name": "", "score": ""},
            {"name": "", "score": ""},
            {"name": "", "score": ""},
            {"name": "", "score": ""},
            {"name": "", "score": ""},
            {"name": "", "score": ""},
            {"name": "", "score": ""},
            {"name": "", "score": ""},
            {"name": "", "score": ""},
            {"name": "", "score": ""},
            {"name": "", "score": ""},
            {"name": "", "score": ""},
            {"name": "", "score": ""},
            {"name": "", "score": ""},
            {"name": "", "score": ""},
            {"name": "", "score": ""},
            {"name": "", "score": ""},
            {"name": "", "score": ""},
            {"name": "", "score": ""},
            {"name": "", "score": ""},
        ]

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
        # Print game results
        self.print_group_stage()

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

    def simulate_game_knockout(self, home, away, stage, current_game):
        """
        Get the teams via id and predict the winner of the game. If the score is tied, pick a winner at random.
        :param home: home team id
        :param away: away team id
        :param stage: stage of the competition
        :return: game winner
        """
        # Predict the score
        home_score, away_score = self.ann.predict(home, away)
        winner = self.get_winner(home_score, away_score)
        self.print_game(home, away, home_score, away_score, stage)
        if stage == 2:
            self.fill_quarter_finals(self.get_team(home)["name"], self.get_team(away)["name"], home_score, away_score, winner)
        elif stage == 3:
            self.fill_semi_finals(self.get_team(home)["name"], self.get_team(away)["name"], home_score, away_score, winner)
        self.print_knockout_stage()

        if winner == "home":
            return home
        else:
            return away

    def get_winner(self, home_score, away_score):
        # Return the winners id
        if home_score > away_score:
            return "home"
        elif home_score < away_score:
            return "away"
        elif home_score == away_score:
            if randint(0, 1) == 0:
                return "home"
            else:
                return "away"

    def determine_knockout_pairs(self):
        """
        Set teams for stage 2.
        """
        eight_finals = [item for item in self.games if item["stage"] == 2]
        for pair in eight_finals:
            pair["home"] = [item["first"] for item in self.groups if item["id"] == pair["home"][1]][0]
            pair["away"] = [item["second"] for item in self.groups if item["id"] == pair["away"][1]][0]
            # Fill eight finals brackets
            self.print_array[self.print_counter] = {"name":self.get_team(pair["home"])["name"], "score":""}
            self.print_counter += 1
            self.print_array[self.print_counter] = {"name": self.get_team(pair["away"])["name"], "score": ""}
            self.print_counter += 1
        self.print_counter = 0

    def set_progressor(self, match_id, progressor):
        """
        Set opponents for the next stage.
        Find the game where the home or away team corresponds
        to match id and put the progressor (team id) on that spot.
        :param match_id: id of the current match played
        :param progressor: id of the winning team
        :param stage: current stage of the tournament
        """
        game = [item for item in self.games if item["stage"] > 2 and item["home"] == match_id]
        if len(game) > 0:
            game[0]["home"] = progressor
            return
        game = [item for item in self.games if item["stage"] > 2 and item["away"] == match_id]
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

        # Eight-finals an quarter finals simulation
        while game["stage"] == 2 or game["stage"] == 3:
            # Get game winner
            progressor = self.simulate_game_knockout(game["home"], game["away"], game["stage"], current_game)
            # Set the game winner in the next round
            self.set_progressor(game["id"], progressor)
            current_game += 1
            game = self.games[current_game]

        # Semi-finals simulation
        progressor = self.simulate_game_knockout(game["home"], game["away"], game["stage"], current_game)
        if progressor == game["home"]:
            self.games[63]["home"] = game["home"]
            self.games[62]["home"] = game["away"]
        else:
            self.games[63]["home"] = game["away"]
            self.games[62]["home"] = game["home"]
        current_game += 1
        game = self.games[current_game]

        progressor = self.simulate_game_knockout(game["home"], game["away"], game["stage"], current_game)
        if progressor == game["home"]:
            self.games[63]["away"] = game["home"]
            self.games[62]["away"] = game["away"]
        else:
            self.games[63]["away"] = game["away"]
            self.games[62]["away"] = game["home"]
        current_game += 1
        game = self.games[current_game]

        # Third place game simulation
        third_place = self.simulate_game_knockout(game["home"], game["away"], game["stage"], current_game)
        current_game += 1
        game = self.games[current_game]

        # Finals simulation
        winner = self.simulate_game_knockout(game["home"], game["away"], game["stage"], current_game)
        if winner == game["home"]:
            second_place = game["away"]
        else:
            second_place = game["home"]

        print("Third place team is:")
        print(self.get_team(third_place))
        print("Second place team is:")
        print(self.get_team(second_place))
        print("The winner is:")
        print(self.get_team(winner))

    # Helper functions
    def get_team(self, team_id):
        """
        Return team according to the input parameter.
        :param team_id: team id
        :return: team
        """
        return [item for item in self.teams if item["id"] == team_id][0]

    def print_game(self, home_id, away_id, home_score, away_score, stage):
        home_team = self.get_team(home_id)
        away_team = self.get_team(away_id)
        print("Stage: " + str(stage) + ", " + home_team["name"] + " vs " + away_team["name"] + " -> " + str(home_score) + ":" + str(away_score))

    def print_group_stage(self):
        groups = []
        print("GROUP STAGE")
        for group in self.groups:
            teams = [self.get_team(team) for team in group["teams"]]
            order = sorted(teams, key=lambda x: (x["points"], x["goal_difference"], x["number_of_goals"]),
                           reverse=True)
            groups.append(order)

        print("GROUP A                          GROUP B                          GROUP C                          GROUP D                          ")
        print("====================================================================================================================================")
        print("|Team        | Points | GD | GS ||Team        | Points | GD | GS ||Team        | Points | GD | GS ||Team        | Points | GD | GS |")
        print("|{:12}|{:>8}|{:>4}|{:>4}||{:12}|{:>8}|{:>4}|{:>4}||{:12}|{:>8}|{:>4}|{:>4}||{:12}|{:>8}|{:>4}|{:>4}|".format(
            groups[0][0]["name"], groups[0][0]["points"], groups[0][0]["goal_difference"], groups[0][0]["number_of_goals"],
            groups[1][0]["name"], groups[1][0]["points"], groups[1][0]["goal_difference"], groups[1][0]["number_of_goals"],
            groups[2][0]["name"], groups[2][0]["points"], groups[2][0]["goal_difference"], groups[2][0]["number_of_goals"],
            groups[3][0]["name"], groups[3][0]["points"], groups[3][0]["goal_difference"], groups[3][0]["number_of_goals"]))
        print("|{:12}|{:>8}|{:>4}|{:>4}||{:12}|{:>8}|{:>4}|{:>4}||{:12}|{:>8}|{:>4}|{:>4}||{:12}|{:>8}|{:>4}|{:>4}|".format(
            groups[0][1]["name"], groups[0][1]["points"], groups[0][1]["goal_difference"], groups[0][1]["number_of_goals"],
            groups[1][1]["name"], groups[1][1]["points"], groups[1][1]["goal_difference"], groups[1][1]["number_of_goals"],
            groups[2][1]["name"], groups[2][1]["points"], groups[2][1]["goal_difference"], groups[2][1]["number_of_goals"],
            groups[3][1]["name"], groups[3][1]["points"], groups[3][1]["goal_difference"], groups[3][1]["number_of_goals"]))
        print("|{:12}|{:>8}|{:>4}|{:>4}||{:12}|{:>8}|{:>4}|{:>4}||{:12}|{:>8}|{:>4}|{:>4}||{:12}|{:>8}|{:>4}|{:>4}|".format(
            groups[0][2]["name"], groups[0][2]["points"], groups[0][2]["goal_difference"], groups[0][2]["number_of_goals"],
            groups[1][2]["name"], groups[1][2]["points"], groups[1][2]["goal_difference"], groups[1][2]["number_of_goals"],
            groups[2][2]["name"], groups[2][2]["points"], groups[2][2]["goal_difference"], groups[2][2]["number_of_goals"],
            groups[3][2]["name"], groups[3][2]["points"], groups[3][2]["goal_difference"], groups[3][2]["number_of_goals"]))
        print("|{:12}|{:>8}|{:>4}|{:>4}||{:12}|{:>8}|{:>4}|{:>4}||{:12}|{:>8}|{:>4}|{:>4}||{:12}|{:>8}|{:>4}|{:>4}|".format(
            groups[0][3]["name"], groups[0][3]["points"], groups[0][3]["goal_difference"], groups[0][3]["number_of_goals"],
            groups[1][3]["name"], groups[1][3]["points"], groups[1][3]["goal_difference"], groups[1][3]["number_of_goals"],
            groups[2][3]["name"], groups[2][3]["points"], groups[2][3]["goal_difference"], groups[2][3]["number_of_goals"],
            groups[3][3]["name"], groups[3][3]["points"], groups[3][3]["goal_difference"], groups[3][3]["number_of_goals"]))
        print("====================================================================================================================================")
        print("GROUP E                          GROUP F                          GROUP G                          GROUP H                          ")
        print("====================================================================================================================================")
        print("|Team        | Points | GD | GS ||Team        | Points | GD | GS ||Team        | Points | GD | GS ||Team        | Points | GD | GS |")
        print("|{:12}|{:>8}|{:>4}|{:>4}||{:12}|{:>8}|{:>4}|{:>4}||{:12}|{:>8}|{:>4}|{:>4}||{:12}|{:>8}|{:>4}|{:>4}|".format(
            groups[4][0]["name"], groups[4][0]["points"], groups[4][0]["goal_difference"], groups[4][0]["number_of_goals"],
            groups[5][0]["name"], groups[5][0]["points"], groups[5][0]["goal_difference"], groups[5][0]["number_of_goals"],
            groups[6][0]["name"], groups[6][0]["points"], groups[6][0]["goal_difference"], groups[6][0]["number_of_goals"],
            groups[7][0]["name"], groups[7][0]["points"], groups[7][0]["goal_difference"], groups[7][0]["number_of_goals"]))
        print("|{:12}|{:>8}|{:>4}|{:>4}||{:12}|{:>8}|{:>4}|{:>4}||{:12}|{:>8}|{:>4}|{:>4}||{:12}|{:>8}|{:>4}|{:>4}|".format(
            groups[4][1]["name"], groups[4][1]["points"], groups[4][1]["goal_difference"], groups[4][1]["number_of_goals"],
            groups[5][1]["name"], groups[5][1]["points"], groups[5][1]["goal_difference"], groups[5][1]["number_of_goals"],
            groups[6][1]["name"], groups[6][1]["points"], groups[6][1]["goal_difference"], groups[6][1]["number_of_goals"],
            groups[7][1]["name"], groups[7][1]["points"], groups[7][1]["goal_difference"], groups[7][1]["number_of_goals"]))
        print("|{:12}|{:>8}|{:>4}|{:>4}||{:12}|{:>8}|{:>4}|{:>4}||{:12}|{:>8}|{:>4}|{:>4}||{:12}|{:>8}|{:>4}|{:>4}|".format(
            groups[4][2]["name"], groups[4][2]["points"], groups[4][2]["goal_difference"], groups[4][2]["number_of_goals"],
            groups[5][2]["name"], groups[5][2]["points"], groups[5][2]["goal_difference"], groups[5][2]["number_of_goals"],
            groups[6][2]["name"], groups[6][2]["points"], groups[6][2]["goal_difference"], groups[6][2]["number_of_goals"],
            groups[7][2]["name"], groups[7][2]["points"], groups[7][2]["goal_difference"], groups[7][2]["number_of_goals"]))
        print("|{:12}|{:>8}|{:>4}|{:>4}||{:12}|{:>8}|{:>4}|{:>4}||{:12}|{:>8}|{:>4}|{:>4}||{:12}|{:>8}|{:>4}|{:>4}|".format(
            groups[4][3]["name"], groups[4][3]["points"], groups[4][3]["goal_difference"], groups[4][3]["number_of_goals"],
            groups[5][3]["name"], groups[5][3]["points"], groups[5][3]["goal_difference"], groups[5][3]["number_of_goals"],
            groups[6][3]["name"], groups[6][3]["points"], groups[6][3]["goal_difference"], groups[6][3]["number_of_goals"],
            groups[7][3]["name"], groups[7][3]["points"], groups[7][3]["goal_difference"], groups[7][3]["number_of_goals"]))
        print("====================================================================================================================================")
        # sleep(0.1)

    def print_knockout_stage(self):
        print("{:12}{:>2}|                              ".format(self.print_array[0]["name"], self.print_array[0]["score"]))
        print("              - {:12}{:>2}|                  ".format(self.print_array[16]["name"], self.print_array[16]["score"]))
        print("{:12}{:>2}|               |                  ".format(self.print_array[1]["name"], self.print_array[1]["score"]))
        print("{:12}{:>2}|               - {:12}{:>2}|       ".format(self.print_array[2]["name"], self.print_array[2]["score"], self.print_array[0]["name"], self.print_array[0]["score"]))
        print("              - {:12}{:>2}|               |         ".format(self.print_array[17]["name"], self.print_array[17]["score"]))
        print("{:12}{:>2}|                               |         ".format(self.print_array[3]["name"], self.print_array[3]["score"]))
        print("{:12}{:>2}|                               - {:12}{:>2}|".format(self.print_array[8]["name"], self.print_array[8]["score"], self.print_array[0]["name"], self.print_array[0]["score"]))
        print("              - {:12}{:>2}|               |               |".format(self.print_array[18]["name"], self.print_array[18]["score"]))
        print("{:12}{:>2}|               - {:12}{:>2}|               |".format(self.print_array[9]["name"], self.print_array[9]["score"], self.print_array[0]["name"], self.print_array[0]["score"]))
        print("{:12}{:>2}|               |                               |".format(self.print_array[10]["name"], self.print_array[10]["score"]))
        print("              - {:12}{:>2}|                               |".format(self.print_array[19]["name"], self.print_array[19]["score"]))
        print("{:12}{:>2}|                                               |".format(self.print_array[11]["name"], self.print_array[11]["score"]))
        print("{:12}{:>2}|                                               - {:12}".format(self.print_array[4]["name"], self.print_array[4]["score"], self.print_array[0]["name"]))
        print("              - {:12}{:>2}|                               |".format(self.print_array[20]["name"], self.print_array[20]["score"]))
        print("{:12}{:>2}|               |                               |".format(self.print_array[5]["name"], self.print_array[5]["score"], self.print_array[0]["name"], self.print_array[0]["score"]))
        print("{:12}{:>2}|               - {:12}{:>2}|               |".format(self.print_array[6]["name"], self.print_array[6]["score"], self.print_array[0]["name"], self.print_array[0]["score"]))
        print("              - {:12}{:>2}|               |               |".format(self.print_array[21]["name"], self.print_array[21]["score"]))
        print("{:12}{:>2}|                               - {:12}{:>2}|".format(self.print_array[7]["name"], self.print_array[7]["score"], self.print_array[0]["name"], self.print_array[0]["score"]))
        print("{:12}{:>2}|                               |         ".format(self.print_array[12]["name"], self.print_array[12]["score"]))
        print("              - {:12}{:>2}|               |         ".format(self.print_array[22]["name"], self.print_array[22]["score"]))
        print("{:12}{:>2}|               - {:12}{:>2}|       ".format(self.print_array[13]["name"], self.print_array[13]["score"], self.print_array[0]["name"], self.print_array[0]["score"]))
        print("{:12}{:>2}|               |                  ".format(self.print_array[14]["name"], self.print_array[14]["score"]))
        print("              - {:12}{:>2}|                  ".format(self.print_array[23]["name"], self.print_array[23]["score"]))
        print("{:12}{:>2}|                              ".format(self.print_array[15]["name"], self.print_array[15]["score"]))

    def fill_quarter_finals(self, home, away, home_score, away_score, winner):
        self.print_array[self.print_counter] = {"name":home, "score":home_score}
        self.print_counter += 1
        self.print_array[self.print_counter] = {"name":away, "score":away_score}
        self.print_counter += 1
        if winner == "home":
            self.print_array[self.quarter_final_couner] = {"name":home, "score":""}
        else:
            self.print_array[self.quarter_final_couner] = {"name":away, "score": ""}
        self.quarter_final_couner += 1

    def fill_semi_finals(self, home, away, home_score, away_score, winner):
        pass


if __name__ == "__main__":
    s = Simulation()
    s.simulate_tournament()
