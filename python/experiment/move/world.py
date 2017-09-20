"""
Model of world
"""
import random

import cv2
import matplotlib.pyplot as plt
import numpy as np

import config
import geometric
import manager

GM = geometric.Geometric()
MSG = manager.Manager(GM)

PLAYER = MSG.create_player(config.PLAYER_SIZE)
PLAYERS = [PLAYER]
SCORES = []
SCORES.append({'name': PLAYER.name, 'data': []})

def init():
    """
    First initialization world
    """
    if not config.REAL_MODE:
        for _ in range(config.PLAYER_COUNT - 1):
            plr = MSG.create_player(config.PLAYER_SIZE)
            PLAYERS.append(plr)
            SCORES.append({'name': plr.name, 'data': []})

    for _ in range(config.WORLD_START_FOOD_COUNT):
        MSG.create_food(config.BOX_SIZE)

    for _ in range(config.WORLD_START_POISON_COUNT):
        MSG.create_poison(config.BOX_SIZE)


def cycle(iteration):
    """
    Life cycle
    """
    print('new cycle: ', iteration)

    while not MSG.if_all_player_death():
        GM.zero()
        MSG.score_all()

        if random.random() < 0.1:
            MSG.all_payer_damage()
            print('all player give 25 damage')

        if config.REAL_MODE:
            key = cv2.waitkey()

            if key & 0xFF == ord('1'):
                PLAYER.move()

            if key & 0xFF == ord('2'):
                PLAYER.rotate(90)

            if key & 0xFF == ord('3'):
                PLAYER.eat()

            if key & 0xFF == ord('4'):
                PLAYER.fix()

            if key & 0xFF == ord('q'):
                return True

            print(MSG.get_vision(PLAYER))

            MSG.draw_all()
        else:
            MSG.action()
            MSG.draw_all()

            if cv2.waitKey(config.DELAY) & 0xFF == ord('q'):
                t = np.arange(iteration)
                for score in SCORES:
                    plt.plot(t, score['data'])
                plt.show()
                return True

        GM.print()

    if not config.REAL_MODE:
        PLAYERS.sort(key=lambda x: x.score, reverse=True)
        PLAYERS[0].sex(PLAYERS[1], PLAYERS[3])

    for plr in PLAYERS:
        print(plr.name, ':', plr.score)
        for score in SCORES:
            if score['name'] == plr.name:
                score['data'].append(plr.score)

    MSG.re_init_world()
    GM.zero()
    MSG.draw_all()
    GM.print()

    return False


init()

if config.ROUND_COUNT == -1:
    IT = 0
    while True:
        if cycle(IT):
            break

        IT += 1

else:
    for tick in range(config.ROUND_COUNT):
        if cycle(tick):
            break

    cv2.waitkey()
