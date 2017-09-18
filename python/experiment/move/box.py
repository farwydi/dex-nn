import geometric
import config
import controller


class Box(controller.Object):
    def __init__(self, gm, manager, name, size):
        super().__init__(gm, manager, name)
        self.size = size
        self.setRandomPosition()

    def draw(self):
        self.gm.drawRectangle(tuple(
            self.position), (self.position[0] + self.size, self.position[1] + self.size), self.color)

    def reInit(self):
        self.setRandomPosition()


class Poison(Box):
    def __init__(self, gm, manager, name, size):
        super().__init__(gm, manager, name, size)
        self.color = (0, 255, 0)


class Food(Box):
    def __init__(self, gm, manager, name, size):
        super().__init__(gm, manager, name, size)
        self.color = (0, 0, 255)
