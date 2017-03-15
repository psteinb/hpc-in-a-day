#!/bin/bash

FILENAME=`hostname`_info.log

hostname > ${FILENAME}
free -g  >> ${FILENAME}
cat /proc/cpuinfo  >> ${FILENAME}
df -h  >> ${FILENAME}
