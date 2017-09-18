import geometric
import config
import controller
import player
import box


class Manager:
    def __init__(self, gm):
        self.iterator = 0
        self.gm = gm
        self.objects = []
        self.playerOffset = 25

    def createPlayer(self, size, name='Player', random=True):
        obj = player.Player(self.gm, self, name + str(self.iterator),
                            size, self.playerOffset)
        self.objects.append(obj)
        self.iterator += 1
        self.playerOffset += 30
        return obj

    def createFood(self, size, name='Food', random=True):
        obj = box.Food(self.gm, self, name + str(self.iterator), size)
        self.objects.append(obj)
        self.iterator += 1
        return obj

    def createPoison(self, size, name='Poison', random=True):
        obj = box.Poison(self.gm, self, name + str(self.iterator), size)
        self.objects.append(obj)
        self.iterator += 1
        return obj

    def drawAll(self):
        for x in self.objects:
            x.draw()

    def areLive(self):
        for x in self.objects:
            if type(x) is player.Player:
                if x.death:
                    return False
        return True

    def reInitDeathPlayer(self):
        for x in self.objects:
            if type(x) is player.Player:
                if x.death:
                    x.reInit()

    def ifAllPlayerDeath(self):
        for x in self.objects:
            if type(x) is player.Player:
                if not x.death:
                    return False

        return True

    def reInitWorld(self):
        for x in self.objects:
            x.reInit()

    def _inVision(self, position1, position2):
        f = pow(position1[0] - position2[0], 2) + \
            pow(position1[1] - position2[1], 2)
        if f <= pow(config.PLAYER_VISION * 1.3, 2):
            return True
        else:
            return False

    def getVision(self, obj):
        wall = 0
        posion = None
        food = None
        for b in self.objects:
            bPosition = list(b.position)
            bPosition[0] += int(b.size / 2)
            bPosition[1] += int(b.size / 2)
            if type(b) is box.Poison:
                if self._inVision(bPosition, obj.position):
                    posion = b
            if type(b) is box.Food:
                if self._inVision(bPosition, obj.position):
                    food = b

        toMove = controller.Object._move(
            None, obj.position, obj.rotation, config.PLAYER_VISION)

        if toMove[0] > config.WORLD_SIZE[0] or toMove[1] > config.WORLD_SIZE[1] or toMove[0] < 0 or toMove[1] < 0:
            wall = 1

        return (wall, posion, food)

    def poison2Food(self, poison):
        position = poison.position
        self.objects.remove(poison)
        food = self.createFood(config.BOX_SIZE)
        food.position = position

    def lifeCycle(self):
        for x in self.objects:
            x.life()

    def action(self):
        for x in self.objects:
            if type(x) is player.Player:
                if not x.death:
                    x.think()
