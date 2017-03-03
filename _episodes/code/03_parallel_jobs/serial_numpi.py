#!/usr/bin/env python3
import sys
import numpy as np

np.random.seed(2017)

def inside_circle(total_count):

    x = np.float32(np.random.uniform(size=total_count))
    y = np.float32(np.random.uniform(size=total_count))

    radii = np.sqrt(x*x + y*y)

    count = len(radii[np.where(radii<=1.0)])

    return count

def estimate_pi(n_samples):

    return (4.0 * inside_circle(n_samples) / n_samples)

if __name__=='__main__':

    n_samples = 10000
    if len(sys.argv) > 1:
        n_samples = int(sys.argv[1])

    my_pi = estimate_pi(n_samples)
    sizeof = np.dtype(np.float32).itemsize

    print("[serial version] required memory %.3f MB" % (n_samples*sizeof*3/(1024*1024)))
    print("[serial version] pi is %f from %i samples" % (my_pi,n_samples))
