#!/bin/bash

for i in `seq -f "%02.0f" 1 16`;do
    export HPCINADAY_FILENUMBER=${i}
    srun --time=00:10:00 -oo lolasdata-${i}.log -n 1 < slurm_call_generate_scrambled_data.py.sh
done
