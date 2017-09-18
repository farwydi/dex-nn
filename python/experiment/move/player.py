import geometric
import config
import controller
import manager
import random
from keras.models import Sequential
from keras.layers import Dense, LSTM, Dropout
import numpy as np


def merge(w1, w2, mutation=True):
    '''
    merge xx algorithm
    '''
    result = np.zeros((len(w1), len(w1[0])), dtype='float32')
    replace = round(len(w1[0]) / 2)

    '''
    Merge half
    '''
    for i in range(len(w1)):
        gen = []
        for x in range(replace):
            randGen = round(random.uniform(0, len(w1[0]) - 1))
            try:
                gen.index(randGen)
            except:
                gen.append(randGen)

        for g in gen:
            result[i][g] = w1[i][g]

        for x, w in np.ndenumerate(w2[i]):
            x = x[0]
            try:
                gen.index(x)
            except:
                result[i][x] = w
    '''
    Mutation default 20%
    '''
    if mutation:
        replace = round(len(w1[0]) * 0.2)
        for i in range(len(w1)):
            gen = []
            for x in range(replace):
                randGen = round(random.uniform(0, len(w1[0]) - 1))
                try:
                    gen.index(randGen)
                except:
                    gen.append(randGen)
            for g in gen:
                result[i][g] = random.uniform(-1, 1)

    return result


class Player(controller.Object):
    def __init__(self, gm, manager, name, size, offset):
        super().__init__(gm, manager, name)
        self.size = size
        self.offset = offset
        self.reInit()

        self.model = Sequential()
        self.model.add(Dense(18, input_shape=(3,), activation="relu"))
        self.model.add(Dense(4, activation="linear"))

    def reInit(self):
        self.setRandomPosition()
        self.health = 250
        self.death = False
        self.rotation = 0
        self.score = 0

    def draw(self):
        text = self.name + '        ' + \
            str(self.health) + '   ' + str(self.score)
        self.gm.drawText(text, self.offset, self.color)

        if not self.death:
            self.gm.drawLine(tuple(self.position), tuple(
                self._move(None, self.position, self.rotation, 15)), self.color)
            self.gm.drawCircle(tuple(self.position), self.size, self.color)
            self.gm.drawCircle(tuple(self.position), self.size +
                               config.PLAYER_VISION, self.color, 1)

    def life(self):
        if not self.death:
            if self.health < 0:
                self.death = True

    def eat(self):
        (wall, posion, food) = self.manager.getVision(self)
        if not posion == None:
            self.death = True
            self.health = -1
            posion.reInit()
            print(self.name, 'eat poison! and death :(')
            return True

        if not food == None:
            self.health += 100
            food.reInit()
            self.score += config.SCORE * 10
            print(self.name, 'eat food! +100 HP')
            return True

        self.health -= config.PLAYER_COST_STEP * 5
        self.life()
        return False

    def fix(self):
        self.health -= config.PLAYER_COST_STEP
        self.life()
        if self.death:
            return False

        (wall, posion, food) = self.manager.getVision(self)
        if not posion == None:
            self.manager.poison2Food(posion)
            self.score += config.SCORE * 5
            print(self.name, 'fix poison! +5 SCORE')
            return True

        return False

    def move(self):
        self.health -= config.PLAYER_COST_STEP * 2
        self.life()
        if self.death:
            return False
        (wall, posion, food) = self.manager.getVision(self)
        if wall == 1:
            return False

        self.score += config.SCORE
        super().move()

    def rotate(self):
        self.health -= config.PLAYER_COST_STEP
        self.life()
        if self.death:
            return False

        super().rotate()

    def think(self):
        (wall, posion, food) = self.manager.getVision(self)
        data = [wall, 0, 0]
        if not posion == None:
            data[1] = 1
        if not food == None:
            data[2] = 1
        out = list(self.model.predict(np.array([tuple(data)]))[0])
        out = [('move', out[0]),
               ('rotate', out[1]),
               ('eat', out[2]),
               ('fix', out[3])]
        out.sort(key=lambda x: x[1], reverse=True)
        out = out[0][0]

        if out == 'move':
            self.move()
        elif out == 'rotate':
            self.rotate()
        elif out == 'eat':
            self.eat()
        elif out == 'fix':
            self.fix()

    def setWeights(self, w1, w2):
        self.model.get_layer(index=1).set_weights(w1)
        self.model.get_layer(index=2).set_weights(w2)

    def sex(self, partner, progeny):
        wSelf = self.model.get_layer(index=1).get_weights()[0]
        wPartner = partner.model.get_layer(index=1).get_weights()[0]

        w1 = merge(wSelf, wPartner)

        wSelf_2 = self.model.get_layer(index=2).get_weights()[0]
        wPartner_2 = partner.model.get_layer(index=2).get_weights()[0]

        w2 = merge(wSelf_2, wPartner_2)

        progeny.setWeights([w1, np.zeros(len(w1[0]), dtype='float32')], [
                           w2, np.zeros(len(w2[0]), dtype='float32')])
