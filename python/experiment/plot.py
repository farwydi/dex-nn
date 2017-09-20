import numpy as np
import matplotlib.pyplot as plt

iteration_count = 523
data1 = np.random.randn(iteration_count)
data2 = np.random.randn(iteration_count)
data3 = np.random.randn(iteration_count)

t = np.arange(0, iteration_count, 1)

plt.figure(1)
plt.plot(t, data1)
plt.plot(t, data2)
plt.show()
