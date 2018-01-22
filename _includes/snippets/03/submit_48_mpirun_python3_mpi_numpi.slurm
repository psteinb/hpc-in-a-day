$ cat submit_mpi_numpi.sh
#!/bin/bash

mpirun python3 mpi_numpi.py 1000000000
$ sbatch -n 48 -o mpi_numpi.out -e mpi_numpi.err < submit_mpi_numpi.sh