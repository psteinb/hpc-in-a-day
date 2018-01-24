#!/usr/bin/env python3
import sys
import numpy as np
import argparse

np.random.seed(2017)

def inside_circle(total_count):

    x = np.float32(np.random.uniform(size=total_count))
    y = np.float32(np.random.uniform(size=total_count))

    radii = np.sqrt(x*x + y*y)

    filtered = np.where(radii<=1.0)
    count = len(radii[filtered])

    return count

def estimate_pi(total_count):

    count = inside_circle(total_count)
    return (4.0 * count / float(total_count))

if __name__=='__main__':

    parser = argparse.ArgumentParser(description='Estimate Pi using a Monte Carlo method.')
    parser.add_argument('n_samples', metavar='N', type=int, nargs=1,
                        default=10000,
                        help='number of times to draw a random number')

    args = parser.parse_args()

    n_samples = args.n_samples[0]
    my_pi = estimate_pi(n_samples)
    sizeof = np.dtype(np.float32).itemsize

    print("[serial version] required memory %.3f MB" % (n_samples*sizeof*3/(1024*1024)))
    print("[serial version] pi is %f from %i samples" % (my_pi,n_samples))

    sys.exit(0)
