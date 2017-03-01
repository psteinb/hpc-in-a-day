#!/usr/bin/env python3
import sys
import random
import math
from multiprocessing import cpu_count, Pool

def estimate_pi(total_count):

    count_inside = 0
    for count in range(0, total_count):
        x = random.random()
        y = random.random()
        d = math.sqrt(x*x + y*y)
        if d < 1: count_inside += 1

    return count_inside


if __name__=='__main__':

    ncores = cpu_count()
    n_iterations = 10000
    if len(sys.argv) > 1:
        n_iterations = int(sys.argv[1])

    partitions = [ math.ceil(n_iterations/ncores) for item in range(ncores)]
    pool = Pool(processes=ncores)

    counts=pool.map(estimate_pi, partitions)

    my_pi = 4*sum(counts)/sum(partitions)

    print("[using %i cores] pi is %f from %i samples" % (ncores,my_pi,n_iterations))
