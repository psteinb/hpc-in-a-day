$ cat call_hostname.sh
#!/bin/bash

srun hostname
$ sbatch -n 4 --ntasks-per-node=1 -o call_hostname.out -e call_hostname.err < call_hostname.sh