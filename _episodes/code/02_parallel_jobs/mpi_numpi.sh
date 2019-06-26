#!/bin/bash
#SBATCH -n 30
#SBATCH -t 00:05:00
#SBATCH -o mpi_numpi.log


mpirun -np 30 python3 mpi_numpi.py 10000000
