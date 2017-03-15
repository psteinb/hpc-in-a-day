$ cat node_info.sh
#!/bin/bash

FILENAME=/tmp/`hostname`_info.log

hostname > ${FILENAME}
free -g  >> ${FILENAME}
cat /proc/cpuinfo  >> ${FILENAME}
df -h  >> ${FILENAME}

$ sbatch --time 00:01 < node_info.sh