import numpy as np
import pandas as pd
from DataPreparation import DataPreparation


class BuildTeams:

    def __init__(self, squad_size, selected_attrs):
        # no. of best players to select for each team
        self.squad_size = squad_size

        # base attributes that are always selected
        self.base_attrs = ['Name', 'Nationality']

        # which player's attributes to include
        self.selected_attrs = selected_attrs

    def read_data(self):
        data = pd.read_csv('data/CompleteDataset.csv')
        #print(data.head())

        # only keep selected attributes
        # if selected_attrs is empty, keep all
        if len(self.selected_attrs) != 0:
            data = data[self.base_attrs + self.selected_attrs]

        self.data = data

    def build_team(self, team_name):
        #print(team_name)

        # TODO: require each team to have a certain no. of players from each position (at least one GK,...)
        team = self.data[self.data.Nationality == team_name].sort_values('Overall', ascending=False).head(self.squad_size)

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
                game = np.concatenate([teams[team1], teams[team2]])
                score = [row['home_score'], row['away_score']]
                X.append(game)
                y.append(score)

        # convert to numpy array
        X = np.asarray(X)
        y = np.asarray(y)
        #print(X.shape, y.shape)

        return X, y


class GameData:

    def __init__(self, squad_size=11, selected_attrs=['Overall'], after_year=2015):
        # no. of best players to select for each team
        self.squad_size = squad_size

        # base attributes that are always selected
        self.base_attrs = ['Name', 'Nationality']

        # which player's attributes to include
        self.selected_attrs = selected_attrs

        # only select games after (but including) given year
        self.after_year = after_year

    def get_learning_data(self):
        # get all nations
        games = Games(self.after_year)
        games.read_data()
        all_nations = games.get_all_nations()

        # build teams for all participating nations in FIFA World Cup 2018
        bt = BuildTeams(self.squad_size, self.selected_attrs)
        bt.read_data()

        # a dict with a nations' name as a key and players' data as value
        team_dict = {}

        # build squad for every nation
        for nation in all_nations:
            team = bt.build_team(nation)
            # if we got enough players, add team
            if team.shape[0] >= bt.squad_size:
                #print(team)
                # convert pandas dataframe to matrix and flatten it
                team_dict[nation] = team.as_matrix().flatten()

        # now put together X and y for every match
        return games.get_games(team_dict)



if __name__ == "__main__":
    gd = GameData()
    X, y = gd.get_learning_data()
    print(X.shape, y.shape)

