<<<<<<< HEAD
import numpy as np
import random

np.random.seed(72)

# [np.array([[1, 5], [4, 6]], dtype='float32'), np.zeros(layerSize, dtype='float32')]
# a = [np.array([[1, 5], [4, 6]], dtype='float32'), np.zeros(2, dtype='float32')]


w1 = np.random.rand(2, 32)
w2 = np.random.rand(2, 32)
# w1 = np.random.rand(32, 3)

result = np.zeros((len(w1), len(w1[0])))
replace = round(len(w1[0]) / 2)

'''
Merge half
'''
for i in range(len(w1)):
    gen = []
    for x in range(replace):
        randGen = round(random.uniform(0, len(w1[0]) - 1))
        try:
            gen.index(randGen)
        except:
            gen.append(randGen)

    for g in gen:
        result[i][g] = w1[i][g]

    for x, w in np.ndenumerate(w2[i]):
        x = x[0]
        try:
            gen.index(x)
        except:
            result[i][x] = w
'''
Mutation 20%
'''
replace = round(len(w1[0]) * 0.2)

for i in range(len(w1)):
    gen = []
    for x in range(replace):
        randGen = round(random.uniform(0, len(w1[0]) - 1))
        try:
            gen.index(randGen)
        except:
            gen.append(randGen)
    for g in gen:
        result[i][g] = random.uniform(-1, 1)

print(result)
=======
import pydot_ng as pydot

pydot.Dot.create(pydot.Dot())
>>>>>>> c69d73584897a6cb513654abcb3a500b51bae82b
