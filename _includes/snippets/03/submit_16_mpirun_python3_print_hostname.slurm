$ cat submit_4_print_hostname.sh
#!/bin/bash

srun python3 print_hostname.py
$ sbatch -n 4 -o call_hostname.out -e call_hostname.err < submit_4_print_hostname.sh