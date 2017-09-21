import os
import random

import numpy as np
from keras.layers import Dense, Dropout
from keras.models import Sequential

import config
import controller

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'


def random_gen(size, max_value):
    gen = []
    for _ in range(size):
        rand_gen = round(random.uniform(0, max_value - 1))
        try:
            gen.index(rand_gen)
        except ValueError:
            gen.append(rand_gen)

    return gen


def merge_liner(size, weights_1, weights_2, mutation):
    replace = round(size / 2)
    gen = random_gen(replace, size)
    result = np.zeros(size, dtype='float32')

    for itr in gen:
        result[itr] = weights_1[itr]

    for itr, _ in np.ndenumerate(weights_2):
        itr = itr[0]
        if itr not in gen:
            result[itr] = weights_2[itr]

    if mutation:
        replace = round(size * 0.2)
        gen = random_gen(replace, size)
        for itr in gen:
            result[itr] = random.uniform(-1, 1)

    return result


def merge(weights_1, weights_2, mutation=True):
    '''
    merge xx algorithm
    Merge half
    Mutation default 20%

    # param
    weights_1 = [[ [weight], [weight], [weight] ], [offsets]]
    '''
    if len(weights_1[0]) != len(weights_2[0]):
        raise Exception()

    if len(weights_1[0][0]) != len(weights_2[0][0]):
        raise Exception()

    if len(weights_1[1]) != len(weights_2[1]):
        raise Exception()

    depth_weights = len(weights_1[0])
    size_weights = len(weights_1[0][0])

    result = [np.zeros((depth_weights, size_weights), dtype='float32'), np.zeros(
        size_weights, dtype='float32')]

    for depth in range(depth_weights):
        result[0][depth] = merge_liner(
            size_weights, weights_1[0][depth], weights_2[0][depth], mutation)

    return result


class Player(controller.Object):
    def __init__(self, gm, manager, name, size):
        super().__init__(gm, manager, name)
        self.size = size
        self.re_init()

        if not config.REAL_MODE:
            self.model = Sequential()
            self.input = Dense(18, input_shape=(5,), activation="relu")
            self.model.add(self.input)
            self.hidden_1 = Dense(32, activation="tanh")
            self.model.add(self.hidden_1)
            self.model.add(Dropout(0.35))
            self.hidden_2 = Dense(32, activation="tanh")
            self.model.add(self.hidden_2)
            self.model.add(Dropout(0.35))
            self.output = Dense(4, activation="sigmoid")
            self.model.add(self.output)

            # json_model = open("mnist_model.json", "r")
            # json_model_data = json_model.read()
            # json_model.close()
            # model = model_from_json(json_model_data)

            # self.model.load_weights("move/" + str(self.name) + "_weights.h5")
            self.model.load_weights("move/moveGame.h5")

    def re_init(self):
        self.set_random_position()
        self.health = 500
        self.death = False
        self.rotation = 0
        self.score = 0
        self.__score_buffer = 0
        self.rotate_mem = False
        self.action = ''

    def get_info(self, offset):
        text = self.name + '    ' + \
            str(self.health) + '   ' + \
            str(self.score) + '  ' + str(self.action)
        self.gmt.drawText(text, offset, self.color)

    def draw(self):
        if not self.death:
            self.gmt.drawLine(tuple(self.position), tuple(
                self.get_move(self.position, self.rotation, 15)), self.color)
            self.gmt.drawCircle(tuple(self.position), self.size, self.color)
            self.gmt.drawCircle(tuple(self.position),
                                self.size + config.PLAYER_VISION, self.color, 1)

    def life(self):
        self.rotate_mem = False
        if not self.death:
            if self.health < 0:
                self.death = True

    def eat(self):
        (wall, posion, food) = self.manager.get_vision(self)
        if not posion == None:
            self.death = True
            self.health = -1
            posion.re_init()
            print(self.name, 'eat poison! and death :(')
            return True

        if not food == None:
            self.health += 250
            food.re_init()
            self.score += config.SCORE * 10
            print(self.name, 'eat food! +250 HP 10x SCORE')
            return True

        self.health -= config.PLAYER_COST_STEP * 10
        self.life()
        return False

    def fix(self):
        (wall, posion, food) = self.manager.get_vision(self)
        if not posion == None:
            self.manager.poison_2_food(posion)
            print(self.name, 'fix poison! +5x SCORE')
            self.score += config.SCORE * 5
            return True

        self.health -= config.PLAYER_COST_STEP * 10
        self.life()
        return False

    def move(self):
        (wall, posion, food) = self.manager.get_vision(self)
        if wall == 1:
            self.health -= config.PLAYER_COST_STEP * 10
            self.life()
            return False

        super().move()

    def rotate(self, angle):
        if self.rotate_mem:
            self.health -= config.PLAYER_COST_STEP * 10
            self.life()
            if self.death:
                return False

        super().rotate(angle)
        self.rotate_mem = True

    def think(self):
        """
        think
        """
        if config.REAL_MODE:
            return False

        (wall, posion, food) = self.manager.get_vision(self)
        data = [wall, 0, 0, 0, 0]
        if not posion == None:
            data[1] = 1
        if not food == None:
            data[2] = 1

        # thought
        data[3] = random.random()

        # data[4] = (self.score - self.__score_buffer) / \
        #     config.PLAYER_COST_STEP * 5
        data[4] = self.health / config.PLAYER_MAX_HEALTH

        out = list(self.model.predict(np.array([tuple(data)]))[0])
        out = [('move', out[0]),
               ('rotate', out[1]),
               ('eat', out[2]),
               ('fix', out[3])]
        out.sort(key=lambda x: x[1], reverse=True)
        out = out[0]

        self.action = out[0]

        if self.action == 'move':
            self.move()
        elif self.action == 'rotate':
            self.rotate(out[1])
        elif self.action == 'eat':
            self.eat()
        elif self.action == 'fix':
            self.fix()

        self.__score_buffer = self.score

    def set_weights(self, weights):
        """
        set_weights
        """
        if config.REAL_MODE:
            return False

        if len(weights) != 4:
            raise Exception()

        self.input.set_weights(weights[0])
        self.hidden_1.set_weights(weights[1])
        self.hidden_2.set_weights(weights[2])
        self.output.set_weights(weights[3])

    def save_weights_and_model(self):
        if config.REAL_MODE:
            return False

        self.model.save_weights("move/" + str(self.name) + "_weights.h5")
        json_file = open("move/" + str(self.name) + "_model.json", "w")
        json_file.write(self.model.to_json())
        json_file.close()

    def crossover(self, partner, progeny):
        """
        crossover self with partner
        """
        if config.REAL_MODE:
            return False

        input_w = merge(self.input.get_weights(), partner.input.get_weights())
        hidden_1_w = merge(self.hidden_1.get_weights(),
                           partner.hidden_1.get_weights())
        hidden_2_w = merge(self.hidden_2.get_weights(),
                           partner.hidden_2.get_weights())
        output_w = merge(self.output.get_weights(),
                         partner.output.get_weights())

        progeny.set_weights((input_w, hidden_1_w, hidden_2_w, output_w))
