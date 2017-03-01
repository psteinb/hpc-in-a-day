#!/usr/bin/env python3
import sys
from mpi4py import MPI
import numpy as np

np.random.seed(2017)

comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()


def inside_circle(total_count):

    hname = MPI.Get_processor_name()

    x = np.float32(np.random.uniform(size=total_count))
    y = np.float32(np.random.uniform(size=total_count))

    radii = np.sqrt(x*x + y*y)

    count = len(radii[np.where(radii<=1.0)])

    return count

def estimate_pi(n_samples):

    counts = inside_circle(n_samples)
    return (4.0 * sum(counts) / total_count)

if __name__=='__main__':

    n_samples = 10000
    if len(sys.argv) > 1:
        n_samples = int(sys.argv[1])

    if rank == 0:
        partitions = [ int(n_samples/size) for item in range(size)]
        counts = [ int(0) ] *size
    else:
        partitions = None
        counts = None

    partition_item = comm.scatter(partitions, root=0)
    count_item = comm.scatter(counts, root=0)

    count_item = inside_circle(partition_item)

    counts = comm.gather(count_item, root=0)
    if rank == 0:
        my_pi = 4.0 * sum(counts) / sum(partitions)
        sizeof = np.dtype(np.float32).itemsize
        print("[     mpi version] required memory %.3f MB" % (n_samples*sizeof*3/(1024*1024)))
        print("[using %3i cores ] pi is %f from %i samples" % (size,my_pi,n_samples))
