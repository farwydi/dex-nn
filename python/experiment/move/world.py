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

    MSG.create_well([800, 50], [800, 800])
    MSG.create_well([100, 200], [200, 200])
    MSG.create_well([500, 500], [200, 200])
    # MSG.create_well([100, 50], [100, 100])
    MSG.create_well([1000, 1000], [0, 1200])
    # MSG.create_well([100, 700], [100, 1000])
    # MSG.create_well([0, 0], [0, 500])


def cycle(iteration):
    """
    Life cycle
    """
    print('new cycle: ', iteration)

    while not MSG.if_all_player_death():
        GM.zero()
        MSG.score_all()

        if random.random() < 0.01:
            MSG.all_payer_damage(15)

        if config.REAL_MODE:
            key = cv2.waitKey()

            if key & 0xFF == ord('1'):
                PLAYER.move()

            if key & 0xFF == ord('2'):
                PLAYER.rotate(0.2)

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
                cv2.destroyAllWindows()
                
                for plr in PLAYERS:
                    plr.save_weights_and_model()

                t = np.arange(iteration)
                for score in SCORES:
                    plt.plot(t, score['data'])
                plt.show()

                return True

        offset = 25
        PLAYERS.sort(key=lambda x: x.score, reverse=True)
        for plr in PLAYERS:
            plr.get_info(offset)
            offset += 25

        if config.PLAYER_COUNT - MSG.get_count_death_player() < 2 and PLAYERS[0].score > PLAYERS[1].score:
            break

        GM.print()

    if not config.REAL_MODE:
        PLAYERS[0].crossover(PLAYERS[1], PLAYERS[5])
        PLAYERS[0].crossover(PLAYERS[2], PLAYERS[6])
        PLAYERS[0].crossover(PLAYERS[3], PLAYERS[7])
        PLAYERS[1].crossover(PLAYERS[2], PLAYERS[8])
        PLAYERS[1].crossover(PLAYERS[3], PLAYERS[9])
        PLAYERS[2].crossover(PLAYERS[3], PLAYERS[10])

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
    tick=0
    while True:
        if cycle(tick):
            break

        tick += 1

else:
    for tick in range(config.ROUND_COUNT):
        if cycle(tick):
            break

    cv2.waitkey()
