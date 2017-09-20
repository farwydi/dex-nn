"""
World Object
"""
import math
import random

import config


class Object:
    """
    Object
    """

    def __init__(self, gm, manager, name):
        self.size = 60
        self.gmt = gm
        self.name = name
        self.manager = manager
        self.position = [int(config.WORLD_SIZE[0] / 2),
                         int(config.WORLD_SIZE[1] / 2)]
        self.rotation = 0
        self.color = (int(random.uniform(0, 255)),
                      int(random.uniform(0, 255)),
                      int(random.uniform(0, 255)))

    def set_random_position(self):
        """
        Set random object position
        """
        self.position = [round(random.uniform(0, config.WORLD_SIZE[0])),
                         round(random.uniform(0, config.WORLD_SIZE[1]))]

    def re_init(self):
        """
        need implement
        """
        pass

    def draw(self):
        """
        need implement
        """
        pass

    def life(self):
        """
        need implement
        """
        pass

    @staticmethod
    def get_move(start_position, angle, distance):
        '''
        angle - 0 - 360 degrees
        x1 = dx * sin(a) + x
        y1 = dy * cos(a) + y
        '''
        end_position = (int(math.cos(math.radians(angle)) * distance + start_position[0]), int(
            math.sin(math.radians(angle)) * distance + start_position[1]))

        return end_position

    def move(self):
        """
        move object forward
        """
        self.position = self.get_move(
            self.position, self.rotation, config.PLAYER_STEP)
        self.life()

    def rotate(self, angle):
        """
        rotate object on angle
        """
        self.rotation += angle * 360
        self.rotation -= round(self.rotation / 360) * 360
        # self.rotation += 90
        # if self.rotation > 360:
        #     self.rotation -= round(self.rotation / 360) * 360
