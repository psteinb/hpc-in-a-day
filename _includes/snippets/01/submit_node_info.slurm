$ cat node_info.sh
#!/bin/bash

FILENAME=/tmp/`hostname`_info.log

cat /proc/cpuinfo  > ${FILENAME}

$ sbatch --time 00:01 < node_info.sh