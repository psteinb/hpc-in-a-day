$ cat print_hostname.py
from mpi4py import MPI

def print_hostname():
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    hname = MPI.Get_processor_name()

    print("this is rank = %2i (total: %2i) running on %s" % (rank,size,hname))

    comm.Barrier()


if __name__ == '__main__':

    print_hostname()

$ cat submit_16_print_hostname.sh
#!/bin/bash

mpirun python3 print_hostname.py
$ sbatch -n 16 -o call_hostname.out -e call_hostname.err < submit_16_print_hostname.sh