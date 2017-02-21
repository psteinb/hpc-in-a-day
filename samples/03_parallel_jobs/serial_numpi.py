#!/usr/bin/env python3
import sys
import random
import numpy as np

np.random.seed(2017)

def estimate_pi(total_count):

    x = np.float32(np.random.uniform(size=total_count))
    y = np.float32(np.random.uniform(size=total_count))

    radii = np.sqrt(x*x + y*y)

    filtered = radii[np.where(radii<1.0)]

    count_inside = len(filtered)

    return (4.0 * count_inside / float(total_count))

if __name__=='__main__':

    n_iterations = 10000
    if len(sys.argv) > 1:
        n_iterations = int(sys.argv[1])

    my_pi = estimate_pi(n_iterations)
    sizeof = np.dtype(np.float32).itemsize

    print("[serial version] required memory %.3f MB" % (n_iterations*sizeof*3/(1024*1024)))
    print("[serial version] pi is %f from %i samples" % (my_pi,n_iterations))
