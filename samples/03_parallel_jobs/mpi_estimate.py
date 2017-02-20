#!/usr/bin/env python3
import sys
import random
import math

from mpi4py import MPI

comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()

def estimate_pi(total_count):

    count_inside = 0
    for count in range(0, total_count):
        x = random.random()
        y = random.random()
        d = math.sqrt(x*x + y*y)
        if d < 1: count_inside += 1

    return count_inside


if __name__=='__main__':


    n_iterations = 10000
    if len(sys.argv) > 1 and rank==1:
        n_iterations = int(sys.argv[1])

    if rank == 0:
        partitions = [ math.ceil(n_iterations/size) for item in range(size)]
    else:
        partitions = None

    partitions = comm.bcast(partitions, root=0)

    partitions[rank] = estimate_pi(partitions[rank])

    partitions = comm.partitions(data, root=0)

    if rank == 0:
        total_count = math.ceil(n_iterations/size)
        my_pi = 4*sum(counts)/(size*total_count)
        print("[using %i cores] pi is %f from %i samples" % (size,my_pi,total_count))
