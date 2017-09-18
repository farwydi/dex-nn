import random
import config
import math


class Object:
    def __init__(self, gm, manager, name):
        self.size = 60
        self.gm = gm
        self.name = name
        self.manager = manager
        self.position = [int(config.WORLD_SIZE[0] / 2),
                         int(config.WORLD_SIZE[1] / 2)]

        self.color = (int(random.uniform(0, 255)),
                      int(random.uniform(0, 255)),
                      int(random.uniform(0, 255)))

    def setRandomPosition(self):
        self.position = [round(random.uniform(0, config.WORLD_SIZE[0])),
                         round(random.uniform(0, config.WORLD_SIZE[1]))]

    def reInit(self):
        pass

    def draw(self):
        pass

    def life(self):
        pass

    @staticmethod
    def _move(self, start_position, angle, distance):
        '''
        angle - 0 - 360 degrees
        x1 = dx * sin(a) + x
        y1 = dy * cos(a) + y
        '''
        end_position = (int(math.cos(math.radians(angle)) * distance +
                            start_position[0]), int(math.sin(math.radians(angle)) * distance + start_position[1]))

        return end_position

    def move(self):
        self.position = self._move(
            None, self.position, self.rotation, config.PLAYER_STEP)
        self.life()

    def rotate(self, angle):
        self.rotation += angle * 360
        self.rotation -= round(self.rotation / 360) * 360
        # self.rotation += 90
        # if self.rotation > 360:
        #     self.rotation -= round(self.rotation / 360) * 360
