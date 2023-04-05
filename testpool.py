import multiprocessing
from multiprocessing import Pool, Process

import multiprocessing as mp


def foo(x):
    i = 0
    while i < 1000000000000000:
        i += 1
    return x * x


if __name__ == '__main__':
    num_cores = 4
    mp.set_start_method('spawn')
    pool = mp.Pool(num_cores)
    results = [pool.apply_async(foo, args=(x,)) for x in range(10)]
    output = [r.get() for r in results]
    print(output)
