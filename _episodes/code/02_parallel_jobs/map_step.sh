#!/bin/bash

#BSUB -W 00:10
#BSUB -n 1
#BSUB -J "map_step[1-16]"     # define job name and that we want 16 instances
#BSUB -o map_step.%I.log   # file where the output goes (%J is replaced by the job id, %I is replaced by the job index)
#BSUB -e map_step.%I.err   # file where the error messages go

python3 filter_pi_estimates.py pi_estimate_${LSB_JOBINDEX}.data
