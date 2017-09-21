"""
BOX Object implementation
"""
import controller


class Box(controller.Object):
    """
    BOX
    """

    def __init__(self, gm, manager, name, size):
        super().__init__(gm, manager, name)
        self.size = size
        self.set_random_position()
        self.type = -1

    def draw(self):
        self.gmt.drawRectangle(tuple(
            self.position), (self.position[0] + self.size, self.position[1] + self.size), self.color)

    def re_init(self):
        self.set_random_position()


class Poison(Box):
    """
    Poison Object
    """

    def __init__(self, gm, manager, name, size):
        super().__init__(gm, manager, name, size)
        self.color = (0, 255, 0)
        self.type = 0


class Food(Box):
    """
    Food Object
    """

    def __init__(self, gm, manager, name, size):
        super().__init__(gm, manager, name, size)
        self.color = (0, 0, 255)
        self.type = 1

class Well(controller.Object):
    """
    Well Object
    """

    def __init__(self, gm, manager, name, start, end):
        super().__init__(gm, manager, name)
        self.color = (255, 255, 0)
        self.position = start
        self.end = end
    
    def draw(self):
        self.gmt.drawLine(tuple(self.position), tuple(self.end), self.color)