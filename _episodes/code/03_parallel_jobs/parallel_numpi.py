#!/usr/bin/env python3
import sys

import numpy as np

from multiprocessing import cpu_count, Pool

np.random.seed(2017)

def inside_circle(total_count):

    x = np.float32(np.random.uniform(size=total_count))
    y = np.float32(np.random.uniform(size=total_count))

    radii = np.sqrt(x*x + y*y)

    count = len(radii[np.where(radii<=1.0)])

    return count

def estimate_pi(n_samples,n_cores):

    partitions = [ ]
    for i in range(n_cores):
        partitions.append(int(n_samples/n_cores))

    pool = Pool(processes=n_cores)
    counts=pool.map(inside_circle, partitions)

    total_count = sum(partitions)
    return (4.0 * sum(counts) / total_count)

if __name__=='__main__':

    ncores = cpu_count()
    n_samples = 10000
    if len(sys.argv) > 1:
        n_samples = int(sys.argv[1])

    partitions = [ int(n_samples/ncores) for item in range(ncores)]

    sizeof = np.dtype(np.float32).itemsize

    my_pi = estimate_pi(n_samples,ncores)

    print("[parallel version] required memory %.3f MB" % (n_samples*sizeof*3/(1024*1024)))
    print("[using %3i cores ] pi is %f from %i samples" % (ncores,my_pi,n_samples))
