import math


def move(start_position, angle, distance):
    '''
    angle - 0 - 360 degrees
    x1 = dx * sin(a) + x
    y1 = dy * cos(a) + y
    '''
    end_position = (int(math.cos(math.radians(angle)) * distance +
                        start_position[0]), int(math.sin(math.radians(angle)) * distance + start_position[1]))

    return end_position


print(move((0, 0), 270, 50))