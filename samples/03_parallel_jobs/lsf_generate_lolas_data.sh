#!/bin/bash

for i in `seq -f "%02.0f" 1 16`;do
    bsub -W 00:10 -oo lolasdata-${i}.log -n 1 ./generate_scrambled_data.py /projects/hpcsupport/steinbac/pi_estimate_${i}.data
done
