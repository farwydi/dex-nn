"""
Geometric utils
"""
import cv2
import numpy as np

import config


class Geometric:
    """
    G Utils
    """
    def __init__(self):
        self.zero()

    def zero(self):
        self.BG = np.zeros(
            (config.WORLD_SIZE[0], config.WORLD_SIZE[1], 3), np.uint8)

    def print(self):
        cv2.imshow(config.WORLD_NAME, self.BG)

    def drawRectangle(self, start, end, color):
        cv2.rectangle(self.BG, start, end, color, -1)

    def drawCircle(self, position, radius, color, thickness=-1):
        cv2.circle(self.BG, position, radius, color, thickness)

    def drawText(self, text, topOffest, color):
        cv2.putText(self.BG, text, (10, topOffest),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, color)

    def drawLine(self, start, end, color):
        cv2.line(self.BG, start, end, color, 5)
