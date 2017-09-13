import nn

# init
# _nn = nn.NeuralNetwork(10, 28, 10, 1)
# _nn.setEA(.15, .3)

from PIL import Image
from pathlib import Path

for epoch in range(1):
    pathlist = Path('./ll').glob('**/*.png')

    letter = 0
    for path in pathlist:
        path_in_str = str(path)

        image = Image.open(path_in_str, mode='r')

        set = []
        for x in range(10):
            for y in range(10):
                pix = image.getpixel((x, y))[3]
                pix = pix / 255
                set.append(pix)

        # _nn.set(set)
        # _nn.learning(letter)

        # r = _nn.result()
        # mse = _nn.mse(r, [params[2]])
        # mse = mse[0]
        # print('Error: ', round(mse * 100, 2))

        letter += 1


# image = Image.open()
# leaning
# for epoch in range(80000):
#     for params in _test:
#         _nn.set([params[0], params[1]])

#         _nn.learning([params[2]])

#         r = _nn.result()
#         mse = _nn.mse(r, [params[2]])
#         mse = mse[0]

#         print('Error: ', round(mse * 100, 2))

# e2e
_nn.save('letter.nn')
