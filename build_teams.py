import numpy as np
import pandas as pd
from DataPreparation import DataPreparation


class BuildTeams:

    def __init__(self, squad_size, selected_attrs):
        # no. of best players to select for each team
        self.squad_size = squad_size

        # base attributes that are always selected
        self.base_attrs = ['name', 'nationality']

        # which player's attributes to include
        self.selected_attrs = selected_attrs

    def read_data(self):
        data = pd.read_csv('data/complete.csv')
        #print(data.head())

        # only keep selected attributes
        # if selected_attrs is empty, keep all
        if len(self.selected_attrs) != 0:
            data = data[self.base_attrs + self.selected_attrs]

        self.data = data

    def build_team(self, team_name):
        #print(team_name)

        # TODO: require each team to have a certain no. of players from each position (at least one GK,...)
        team = self.data[self.data.nationality == team_name].sort_values('overall', ascending=False).head(self.squad_size)

        # remove data without base attributes (we only need those to form national teams)
        return team[self.selected_attrs]


class Games:

    def __init__(self, after_year):
        # only select games after (but including) given year
        self.after_year = after_year

    def read_data(self):
        data = pd.read_csv('data/results.csv')

        # only select games after certain year (including that year)
        data = data[(data['date'] > str(self.after_year) + '-01-01')]
        #print(data.head())

        self.data = data

    def get_all_nations(self):
        # get all nations form games dataset so we can build their teams with players' data
        return np.unique(self.data[['home_team', 'away_team']].values)

    def create_game_vector(self, teams, team1, team2):
        return np.concatenate([teams[team1], teams[team2]])

    def get_games(self, teams):
        # teams: a dict with a name of the team as a key and its' data as value

        X = []
        y = []

        # iterate over all selected games
        for index, row in self.data.iterrows():
            team1 = row['home_team']
            team2 = row['away_team']

            # if we have players data for both teams
            if team1 in teams and team2 in teams:
                game = self.create_game_vector(teams, team1, team2)
                #score = [row['home_score'], row['away_score']]

                # get the winner
                home_goals = int(row['home_score'])
                away_goals = int(row['away_score'])
                winner = 2      # it's a tie!

                if home_goals > away_goals:
                    winner = 0
                if away_goals > home_goals:
                    winner = 1

                X.append(game)
                #y.append(score)
                y.append([winner])

        # convert to numpy array
        X = np.asarray(X)
        y = np.asarray(y)
        #print(X.shape, y.shape)

        return X, y


class GameData:

    def __init__(self, squad_size=11, selected_attrs=['overall'], after_year=2012):
        # no. of best players to select for each team
        self.squad_size = squad_size

        # base attributes that are always selected
        self.base_attrs = ['name', 'nationality']

        # which player's attributes to include
        self.selected_attrs = selected_attrs

        # only select games after (but including) given year
        self.after_year = after_year

        # teams: a dict with a name of the team as a key and its' data as value
        self.teams = None

        # helper class
        self.games = Games(self.after_year)
        self.games.read_data()

    def build_teams(self):
        """
        Fill a dict with a nations' name as a key and players' data as value
        """
        # get all nations
        all_nations = self.games.get_all_nations()

        # build teams for all participating nations in FIFA World Cup 2018
        bt = BuildTeams(self.squad_size, self.selected_attrs)
        bt.read_data()

        # a dict with a nations' name as a key and players' data as value
        self.teams = {}

        # build squad for every nation
        for nation in all_nations:
            team = bt.build_team(nation)
            # if we got enough players, add team
            if team.shape[0] >= bt.squad_size:
                #print(team)
                # convert pandas dataframe to matrix and flatten it
                self.teams[nation] = team.as_matrix().flatten()

    def get_learning_data(self):
        """
        Build X and y from all available matches
        """
        if self.teams is None:
            self.build_teams()

        # now put together X and y for every match
        return self.games.get_games(self.teams)

    def get_one_game_data(self, team1, team2):
        """
        Build a vector for a match between two teams
        """
        if self.teams is None:
            self.build_teams()

        # now put together X and y for every match
        return self.games.create_game_vector(self.teams, team1, team2)


if __name__ == "__main__":
    gd = GameData()

    # this is how u get X (all available games)
    X, y = gd.get_learning_data()
    print(X.shape, y.shape)

    # this is how u get a vector for one game
    x = gd.get_one_game_data("Russia", "Germany")
    print(x)


