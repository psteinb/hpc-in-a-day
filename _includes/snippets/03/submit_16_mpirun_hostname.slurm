$ cat call_hostname.sh
#!/bin/bash

mpirun hostname
$ sbatch -n 16 -o call_hostname.out -e call_hostname.err < call_hostname.sh