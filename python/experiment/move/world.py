import cv2
import config
import numpy as np
import geometric
import manager
import player
import time


gm = geometric.Geometric()
manager = manager.Manager(gm)

p1 = manager.createPlayer(config.PLAYER_SIZE)
players = [p1]

def init():
    for x in range(config.WORLD_START_FOOD_COUNT):
        manager.createFood(config.BOX_SIZE)

    for x in range(config.WORLD_START_POISON_COUNT):
        manager.createPoison(config.BOX_SIZE)

    if not config.REAL_MODE:
        for x in range(config.PLAYER_COUNT - 1):
            players.append(manager.createPlayer(config.PLAYER_SIZE))



def cycle(n):
    print('new cycle: ', n)

    while not manager.ifAllPlayerDeath():
        gm.zero()

        if config.REAL_MODE:
            key = cv2.waitKey()

            if key & 0xFF == ord('1'):
                p1.move()

            if key & 0xFF == ord('2'):
                p1.rotate()

            if key & 0xFF == ord('3'):
                p1.eat()

            if key & 0xFF == ord('4'):
                p1.fix()

            if key & 0xFF == ord('q'):
                return True

            print(manager.getVision(p1))

            manager.drawAll()
        else:
            manager.action()
            manager.drawAll()

            if cv2.waitKey(50) & 0xFF == ord('q'):
                return True

        gm.print()

    players.sort(key=lambda x: x.score, reverse=True)
    players[0].sex(players[1], players[3])

    manager.reInitWorld()
    gm.zero()
    manager.drawAll()
    gm.print()

    return False


init()

if config.ROUND_COUNT == -1:
    n = 0
    while True:
        if cycle(n):
            break

        n += 1

else:
    for tick in range(config.ROUND_COUNT):
        if cycle(tick):
            break

    cv2.waitKey()
