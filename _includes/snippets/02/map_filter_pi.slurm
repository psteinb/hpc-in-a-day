$ cat map_step.sh
#!/bin/bash

#SBATCH -t 00:10
#SBATCH -n 1
#SBATCH -J "map_step"  # define job name and that we want 16 instances
#SBATCH --array 1-16
#SBATCH -o map_step.%A-%a.log   # file where the output goes (%A is replaced by the job id, %a is replaced by the job index inside the array of sub jobs)
#SBATCH -e map_step.%A-%a.err   # file where the error messages go

python3 filter_pi_estimates.py pi_estimate_${SLURM_ARRAY_TASK_ID}.data
$ sbatch < map_step.sh