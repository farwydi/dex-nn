'''
move controller
'''
import math
import cv2
import numpy as np
import random
import time
from keras.models import Sequential
from keras.layers import Dense, LSTM, Dropout

# from memory_profiler import profile

size = (1024, 1024)


def clamp(n, smallest, largest):
    return max(smallest, min(round(n), largest))


layerSize = 32
layerSizeHalf = int(layerSize / 2)


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


class Player:
    def __init__(self):
        global it, text

        self.rand()

        self.name = str(it)
        it += 1
        self.text = text
        text += 25
        self.color = (int(random.uniform(0, 255)), int(
            random.uniform(0, 255)), int(random.uniform(0, 255)))

        self.model = Sequential()

        self.model.add(Dense(18, input_shape=(2,)))
        self.model.add(Dense(25))
        # self.model.add(Dropout(.2))
        # self.model.add(LSTM(52, activation="relu"))
        self.model.add(Dense(1, activation="linear"))

        # self.model.load_weights("move.h5")

        # self.model.compile(loss="mean_squared_error",
        #                    optimizer="Adam")

    def setWeights(self, w1, w2):
        self.model.get_layer(index=1).set_weights(w1)
        self.model.get_layer(index=3).set_weights(w2)

    # @profile
    def sex(self, partner, progeny):
        global it

        wSelf = self.model.get_layer(index=1).get_weights()[0]
        wPartner = partner.model.get_layer(index=1).get_weights()[0]

        w1 = merge(wSelf, wPartner)

        wSelf_2 = self.model.get_layer(index=3).get_weights()[0]
        wPartner_2 = partner.model.get_layer(index=3).get_weights()[0]

        w2 = merge(wSelf_2, wPartner_2, False)


        '''
        hidden layer
        '''
        wSelf_3 = self.model.get_layer(index=2).get_weights()[0]
        wPartner_3 = partner.model.get_layer(index=2).get_weights()[0]

        print(wSelf_3)

        progeny.name = str(it)
        it += 1

        progeny.setWeights([w1, np.zeros(len(w1[0]), dtype='float32')], [
                           w2, np.zeros(len(w2[0]), dtype='float32')])

    # @profile
    def rand(self):
        self.death = False
        self.scope = 0
        self.health = 60
        # self.position = [int(size[0] / 2), int(size[1] / 2)]
        self.position = [round(random.uniform(0, size[1])),
                         round(random.uniform(0, size[0]))]

    def calc(self):
        if not self.death:
            # dist = ((self.position[0] - targetCenter[0]) / size[0],
            #         (self.position[1] - targetCenter[1]) / size[1])

            # pred = ((size[0] - self.position[0]) / size[0],
            #         (size[1] - self.position[1]) / size[1],
            #         (size[0] - targetCenter[0]) / size[0],
            #         (size[1] - targetCenter[1]) / size[1])

            pred = (abs(self.position[0] - targetCenter[0]) / size[0],
                    abs(self.position[1] - targetCenter[1]) / size[1])

            # if self.name == '1':
            #     print(pred)

            # print(pred)

            out = self.model.predict(np.array([pred]))[0][0]

            cv2.putText(bg, str(pred), (10, self.text),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, 242)

            # print(out)

            self.scope += 10
            self.health -= 1

            self.move(out)

    def _move(self, start_position, angle, distance):
        '''
        angle - 0 - 360 degrees
        x1 = dx * sin(a) + x
        y1 = dy * cos(a) + y
        '''
        end_position = (int(math.cos(math.radians(angle)) * distance +
                            start_position[0]), int(math.sin(math.radians(angle)) * distance + start_position[1]))

        return end_position

    def move(self, angle):
        # (x, y) = x_y_s

        # print(x_y_s)

        # position = (int(round(y * 50)), int(round(x * 50)))
        self.position = self._move(self.position, angle * 360, 10)

        # if position[0] == 0 & position[1] == 0:
        #     self.death = True

        # self.position[0] = self.position[0] + position[0]
        # self.position[1] = self.position[1] + position[1]

        if abs(self.position[0] - targetCenter[0]) < 30 and abs(self.position[1] - targetCenter[1]) < 30:
            self.health += 100
            newTarget()

        if self.health < 0:
            self.death = True

        if self.position[0] > size[0] or self.position[0] < 0:
            self.death = True

        if self.position[1] > size[1] or self.position[1] < 0:
            self.death = True

        if not self.death:
            self.draw()

    def draw(self):
        cv2.circle(bg, tuple(self.position), 15, self.color, -1)


it = 0
text = 50
# players = [Player(), Player(), Player()]
players = [Player(), Player(), Player(), Player()]
# players = [Player()]

targetPosition = (round(random.uniform(0, size[1] - 60)),
                  round(random.uniform(0, size[0] - 60)))
targetSize = (targetPosition[0] + 60, targetPosition[1] + 60)
targetCenter = (targetPosition[0] + 30, targetPosition[1] + 30)


def newTarget():
    global targetPosition, targetSize, targetCenter
    targetPosition = (round(random.uniform(0, size[1] - 60)),
                      round(random.uniform(0, size[0] - 60)))
    targetSize = (targetPosition[0] + 60, targetPosition[1] + 60)
    targetCenter = (targetPosition[0] + 30, targetPosition[1] + 30)


x = 0
# for x in range(2):
while True:
    for p in players:
        p.rand()

    print('round: ', x)
    x += 1

    newTarget()

    # time.sleep(2)

    while True:
        bg = np.zeros((size[0], size[1], 3), np.uint8)
        cv2.rectangle(bg, targetPosition, targetSize, (0, 255, 0), -1)

        for p in players:
            p.calc()

        cv2.imshow("t", bg)

        i = 0
        for p in players:
            if p.death:
                i += 1

        if i == len(players):
            break

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    players.sort(key=lambda x: x.scope * x.health, reverse=True)

    for p in players:
        print(p.name, ':', p.scope)

    players[0].sex(players[1], players[3])
    # players[0].sex(players[2], players[2])
    # players[1].sex(players[2], players[9])
    # players[1].sex(players[3], players[8])
