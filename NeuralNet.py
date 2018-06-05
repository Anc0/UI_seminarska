from random import randint

from keras import Sequential
from keras.layers import Dense, Dropout
from keras.models import load_model
from keras.utils import to_categorical
from matplotlib import style
from matplotlib.pyplot import figure, plot, title, xlabel, ylabel, legend, savefig
from numpy import argmax
from numpy.core.multiarray import arange, array

from build_teams import GameData


class NeuralNet:

    def __init__(self):
        self.model = Sequential()
        self.H = None
        self.loaded_model = None
        self.game_data = GameData(selected_attrs=['overall', 'pac', 'sho', 'pas', 'dri', 'def', 'phy', 'skill_moves',
                                                  'weak_foot', 'crossing', 'finishing', 'heading_accuracy',
                                                  'short_passing', 'volleys', 'dribbling', 'curve', 'free_kick_accuracy',
                                                  'long_passing', 'ball_control', 'acceleration', 'sprint_speed',
                                                  'agility', 'reactions', 'balance', 'shot_power', 'jumping',
                                                  'stamina', 'strength', 'long_shots', 'aggression', 'interceptions',
                                                  'positioning', 'vision', 'penalties', 'composure', 'marking',
                                                  'standing_tackle', 'sliding_tackle', 'gk_diving', 'gk_handling',
                                                  'gk_kicking', 'gk_positioning', 'gk_reflexes'])


        self.epochs = 50
        self.batch_size = 32

    def build(self):
        self.model.add(Dense(units=512, input_shape=(22 * 43, ), activation='relu'))
        self.model.add(Dense(units=256, activation='relu'))
        self.model.add(Dense(units=128, activation='relu'))
        self.model.add(Dense(units=32, activation='relu'))
        self.model.add(Dense(units=3, activation='softmax'))
        self.model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

    def fit(self):
        X, y = self.game_data.get_learning_data()
        y = to_categorical(y)
        X = X / 100
        self.H = self.model.fit(X, y, epochs=self.epochs, verbose=2, validation_split=0.3, batch_size=self.batch_size, shuffle=True)
        self.model.save("world_cup.model")

    def predict(self, home, away):
        if self.loaded_model is None:
            self.loaded_model = load_model("world_cup.model")
        X = array([self.game_data.get_one_game_data(home, away)])
        result = self.loaded_model.predict(X)
        return argmax(result[0])

    def plot_results(self):
        """
        Plot accuracy and loss for every epoch of train and validation set.
        :return:
        """
        style.use("ggplot")
        figure()
        N = self.epochs
        plot(arange(0, N), self.H.history["loss"], label="train_loss")
        plot(arange(0, N), self.H.history["val_loss"], label="val_loss")
        plot(arange(0, N), self.H.history["acc"], label="train_acc")
        plot(arange(0, N), self.H.history["val_acc"], label="val_acc")
        title("Training Loss and Accuracy")
        xlabel("Epoch #")
        ylabel("Loss/Accuracy")
        legend(loc="lower left")
        savefig("graph.png")

if __name__ == "__main__":
    nn = NeuralNet()
    nn.build()
    nn.fit()
    nn.plot_results()
