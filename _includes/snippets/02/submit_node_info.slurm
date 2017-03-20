$ cat node_info.sh
#!/bin/bash

FILENAME=/tmp/`hostname`_info.log

head -n30 /proc/cpuinfo  > ${FILENAME}

$ sbatch --time 00:01 < node_info.sh