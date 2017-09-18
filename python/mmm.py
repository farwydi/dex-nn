
from memory_profiler import profile

@profile
def a():
    f = []
    for x in range(1555):
        f.append(x)

    del(f)



for x in range(1555):
    a()