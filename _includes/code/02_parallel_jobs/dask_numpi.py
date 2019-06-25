#!/usr/bin/env python3
import sys
import math
import dask.array as da
import numpy as np

np.random.seed(2017)
da.random.seed(2017)

def inside_circle(total_count, chunk_size = -1):
    x = da.random.uniform(size=(total_count),
                          chunks=(chunk_size))

    y = da.random.uniform(size=(total_count),
                          chunks=(chunk_size))

    radii = da.sqrt(x*x + y*y)
    filtered = da.where(radii <= 1.0)

    indices = np.array(filtered[0])
    count = len(radii[indices])

    return count

def estimate_pi(total_count, chunk_size=-1):

    count = inside_circle(total_count, chunk_size)
    return (4.0 * count / total_count)

def main():
    n_samples = 10000
    if len(sys.argv) > 1:
        n_samples = int(sys.argv[1])

    chunksize = .1*n_samples
    if len(sys.argv) > 2:
        chunksize = int(sys.argv[2])
        
    my_pi = estimate_pi(n_samples, chunksize)
    sizeof = np.dtype(np.float32).itemsize
    print("[parallel version] required memory %.3f MB" % (n_samples*sizeof*3/(1024*1024)))
    print("[using dask lib  ] pi is %f from %i samples" % (my_pi,n_samples))

if __name__=='__main__':
    main()
