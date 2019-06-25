#!/usr/bin/env python3
import sys
import random
import numpy as np
import math
from multiprocessing import cpu_count
from multiprocessing.pool import ThreadPool as Pool

def estimate_pi(total_count):

    x = np.float32(np.random.uniform(size=total_count))
    y = np.float32(np.random.uniform(size=total_count))

    radii = np.sqrt(x*x + y*y)

    filtered = radii[np.where(radii<1.0)]

    return len(filtered)

if __name__=='__main__':

    ncores = cpu_count()
    n_iterations = 10000
    if len(sys.argv) > 1:
        n_iterations = int(sys.argv[1])

    partitions = [ math.ceil(n_iterations/ncores) for item in range(ncores)]
    pool = Pool(processes=ncores)

    sizeof = np.dtype(np.float32).itemsize
    n_iterations = sum(partitions)
    counts=pool.map(estimate_pi, partitions)

    my_pi = 4*sum(counts)/sum(partitions)

    print("[threads version ] required memory %.3f MB" % (n_iterations*sizeof*3/(1024*1024)))
    print("[using %3i cores ] pi is %f from %i samples" % (ncores,my_pi,n_iterations))
