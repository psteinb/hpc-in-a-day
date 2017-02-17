#/usr/bin/env python3

from mpi4py import MPI
from datetime import datetime

def print_hostname():
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    hname = MPI.Get_processor_name()
    tod   = datetime.now().isoformat(' ')
    print("this is rank = %2i (total: %2i) running on %s at %s" % (rank,size,hname,tod))

    comm.Barrier()


if __name__ == '__main__':

    print_hostname()
