import random

# random.seed(45)

# class A:
#     def __init__(self):
#         self.score = random.uniform(0, 100)


# a = [A(), A(), A(), A(), A(), A(), A(), A(), A()]


# a.sort(key=lambda x: x.score, reverse=True)

# del(a[-1:])
# for x in a:
#     print(x.score)


import numpy as np

layerSize = 18

np.random.seed(72)

wSelf = np.random.rand(layerSize)
wPartner = np.random.rand(layerSize)

progeny = [.0] * layerSize
print(progeny)

c = 0
ex = []

while True:
    for i, w in np.ndenumerate(wSelf):
        i = i[0]

        if c == 9:
            break

        try:
            ex.index(i)
            continue
        except:
            if round(random.random()) == 1:
                progeny[i] = w
                c += 1
                ex.append(i)

    if c == 9:
        break


for i, w in np.ndenumerate(wPartner):
    i = i[0]

    try:
        ex.index(i)
        continue
    except:
        progeny[i] = w

# print(wSelf)
# print(wPartner)
print(progeny)
