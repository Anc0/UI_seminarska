import numpy as np
import pandas as pd
import DataPreparation

class BuildTeams:


    def __init__(self, squad_size=11, selected_attrs=['Overall']):
        self.squad_size = squad_size
        self.base_attrs = ['Name', 'Nationality']
        self.selected_attrs = selected_attrs
        pass

    def read_data(self):
        data = pd.read_csv('data/CompleteDataset.csv')
        print(data.head())

        # only keep selected attributes
        # if selected_attrs is empty, keep all
        if len(self.selected_attrs) != 0:
            data = data[self.base_attrs + self.selected_attrs]

        print(data.head())

        self.data = data

    def build_team(self, team_name):
        print(team_name)




if __name__ == "__main__":
    bt = BuildTeams()
    bt.read_data()

    dp = DataPreparation()

    for team in dp.TEAMS:
        bt.build_team(team.name)