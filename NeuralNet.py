from random import randint
from keras.models import Sequential
from keras.layers import Dense
from build_teams import GameData


class NeuralNet:

    def __init__(self):

        # get data
        gd = GameData()
        self.X, self.y = gd.get_learning_data()

        # first layer (= no. of attrs.)
        self.first_layer = self.X.shape[1]

        # model
        self.model = None

    def build(self):
        # TODO: build a great model!
        model = Sequential()
        model.add(Dense(units=64, activation='relu', input_dim=self.first_layer))
        model.add(Dense(units=2, activation='softmax'))
        model.compile(loss='categorical_crossentropy', optimizer='sgd', metrics=['accuracy'])

        self.model = model

    def fit(self):
        if self.model is None:
            self.build()

        self.model.fit(self.X, self.y, epochs=10, batch_size=32)

    def predict(self, home, away):
        return randint(0, 3), randint(0, 3)


if __name__ == "__main__":
    nn = NeuralNet()
    nn.fit()