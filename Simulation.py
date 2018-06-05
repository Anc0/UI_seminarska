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
        self.print_array = ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "",
                            "", "", "", "", "", "", "", "", ""]
        self.print_counter = 0

    def simulate_game_group(self, home, away):
        """
        Get teams via id, predict the score and update necessary statistics.
        :param home: home team id
        :param away: away team id
        """
        # Get the teams
        home_team = self.get_team(home)
        away_team = self.get_team(away)

        # Predict the outcome
        result = self.ann.predict(home_team["name"], away_team["name"])


        # Add points according to the score
        if result == 0:
            home_team["points"] += 3
        elif result == 1:
            away_team["points"] += 3
        elif result == 2:
            home_team["points"] += 1
            away_team["points"] += 1
        return result

    def set_progressing_teams(self):
        group_i = 0
        for i in range(0, 30, 4):
            teams = self.teams[i:(i+4)]
            teams = sorted(teams, key=lambda k: k['points'], reverse=True)
            self.groups[group_i]["first"] = teams[0]["id"]
            self.groups[group_i]["second"] = teams[1]["id"]
            group_i += 1

    def determine_knockout_pairs(self):
        """
        Set teams for stage 2.
        """
        eight_finals = [item for item in self.games if item["stage"] == 2]
        for pair in eight_finals:
            pair["home"] = [item["first"] for item in self.groups if item["id"] == pair["home"][1]][0]
            pair["away"] = [item["second"] for item in self.groups if item["id"] == pair["away"][1]][0]

    def fill_knockout_print(self):
        games = [49, 50, 51, 52, 53, 54, 55, 56]
        for game in games:
            self.set_print_chart(self.get_team(self.games[game - 1]["home"])["name"])
            self.set_print_chart(self.get_team(self.games[game - 1]["away"])["name"])

    def set_print_chart(self, name):
        self.print_array[self.print_counter] = name
        self.print_counter += 1

    def simulate_game_knockout(self, home, away, stage, current_game):
        """
        Get the teams via id and predict the winner of the game. If the score is tied, pick a winner at random.
        :param home: home team id
        :param away: away team id
        :param stage: stage of the competition
        :return: game winner
        """
        # Get the teams
        home_team = self.get_team(home)
        away_team = self.get_team(away)

        # Predict the score
        result = self.ann.predict(home_team["name"], away_team["name"])

        # If the game is tied, select winner at random
        if result == 2:
            result = randint(0, 1)
        # The winner progresses to the next round
        if result == 0:
            self.set_winner(home, stage, current_game)
            self.set_print_chart(home_team["name"])
        elif result == 1:
            self.set_winner(away, stage, current_game)
            self.set_print_chart(away_team["name"])
        return result

    def set_winner(self, winner, stage, current_game):
        current_game += 1
        for game in self.games:
            if game["stage"] == stage + 1:
                if game["home"] == current_game:
                    game["home"] = winner
                    break
                elif game["away"] == current_game:
                    game["away"] = winner
                    break

    def simulate_semis(self, home, away, current_game):
        # Get the teams
        home_team = self.get_team(home)
        away_team = self.get_team(away)

        # Predict the score
        result = self.ann.predict(home_team["name"], away_team["name"])

        # If the game is tied, select winner at random
        if result == 2:
            result = randint(0, 1)

        side = "home"
        if current_game == 61:
            side = "away"

        if result == 0:
            self.games[62][side] = away
            self.games[63][side] = home
            self.set_print_chart(home_team["name"])
        if result == 1:
            self.games[62][side] = home
            self.games[63][side] = away
            self.set_print_chart(away_team["name"])
        return result

    def simulate_tournament(self):
        current_game = 0
        game = self.games[current_game]
        # Group stage games simulation
        while game["stage"] == 1:
            result = self.simulate_game_group(game["home"], game["away"])
            self.print_game(game["home"], game["away"], 1, result)

            current_game += 1
            game = self.games[current_game]

        self.set_progressing_teams()
        self.determine_knockout_pairs()
        self.fill_knockout_print()

        self.print_knockout_stage()

        # Simulate eight-finals
        while game["stage"] == 2:
            result = self.simulate_game_knockout(game["home"], game["away"], game["stage"], current_game)

            current_game += 1
            game = self.games[current_game]
        self.print_knockout_stage()

        # Simulate quarter-finals
        while game["stage"] == 3:
            result = self.simulate_game_knockout(game["home"], game["away"], game["stage"], current_game)

            current_game += 1
            game = self.games[current_game]
        self.print_knockout_stage()

        # Simulate semi-finals
        while game["stage"] == 4:
            result = self.simulate_semis(game["home"], game["away"], current_game)
            # self.print_game(game["home"], game["away"], game["stage"], result)

            current_game += 1
            game = self.games[current_game]
        self.print_knockout_stage()

        # Simulate 3rd place game
        home_team = self.get_team(game["home"])
        away_team = self.get_team(game["away"])

        # Predict the score
        result = self.ann.predict(home_team["name"], away_team["name"])
        if result == 2:
            result = randint(0, 1)
        if result == 0:
            third_place = home_team["name"]
        elif result == 1:
            third_place = away_team["name"]
        # self.print_game(game["home"], game["away"], game["stage"], result)

        current_game += 1
        game = self.games[current_game]

        # Simulate the final
        home_team = self.get_team(game["home"])
        away_team = self.get_team(game["away"])

        # Predict the score
        result = self.ann.predict(home_team["name"], away_team["name"])
        if result == 2:
            result = randint(0, 1)
        if result == 0:
            winner = home_team["name"]
            second_place = away_team["name"]
        elif result == 1:
            winner = away_team["name"]
            second_place = home_team["name"]
        self.set_print_chart(winner)
        self.print_knockout_stage()
        print()

        # self.print_game(game["home"], game["away"], game["stage"], result)
        print("Third place: " + third_place)
        print("Second place: " + second_place)
        print("The champion: " + winner)


    # Helper functions
    def get_team(self, team_id):
        """
        Return team according to the input parameter.
        :param team_id: team id
        :return: team
        """
        return [item for item in self.teams if item["id"] == team_id][0]

    def print_game(self, home_id, away_id, stage, result):
        home_team = self.get_team(home_id)
        away_team = self.get_team(away_id)
        if result == 0:
            winner = home_team["name"]
        elif result == 1:
            winner = away_team["name"]
        elif result == 2:
            winner = "Draw"
        print("Stage: " + str(stage) + ", " + home_team["name"] + " vs " + away_team["name"] + " -> " + winner)

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
        print()
        print("{:12}|                              ".format(self.print_array[0]))
        print("             -- {:12}|                  ".format(self.print_array[16]))
        print("{:12}|               |                  ".format(self.print_array[1]))
        print("{:12}|                -- {:12}|       ".format(self.print_array[2], self.print_array[24]))
        print("             -- {:12}|               |         ".format(self.print_array[17]))
        print("{:12}|                               |         ".format(self.print_array[3]))
        print("{:12}|                                -- {:12}|".format(self.print_array[8], self.print_array[28]))
        print("             -- {:12}|               |               |".format(self.print_array[20]))
        print("{:12}|                -- {:12}|               |".format(self.print_array[9], self.print_array[25]))
        print("{:12}|               |                               |".format(self.print_array[10]))
        print("             -- {:12}|                               |".format(self.print_array[21]))
        print("{:12}|                                               |".format(self.print_array[11]))
        print("{:12}|                                                -- {:12}".format(self.print_array[4], self.print_array[30]))
        print("             -- {:12}|                               |".format(self.print_array[18]))
        print("{:12}|               |                               |".format(self.print_array[5]))
        print("{:12}|                -- {:12}|               |".format(self.print_array[6], self.print_array[27]))
        print("             -- {:12}|               |               |".format(self.print_array[19]))
        print("{:12}|                                -- {:12}|".format(self.print_array[7], self.print_array[29]))
        print("{:12}|                               |         ".format(self.print_array[12]))
        print("             -- {:12}|               |         ".format(self.print_array[22]))
        print("{:12}|                -- {:12}|       ".format(self.print_array[13], self.print_array[26]))
        print("{:12}|               |                  ".format(self.print_array[14]))
        print("             -- {:12}|                  ".format(self.print_array[23]))
        print("{:12}|                              ".format(self.print_array[15]))
        sleep(5)


if __name__ == "__main__":
    s = Simulation()
    s.simulate_tournament()
