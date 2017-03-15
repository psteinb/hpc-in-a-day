#!/bin/bash

echo "[INFO] checking the CPU of this machine"
echo -n "[INFO] "
grep 'model name' /proc/cpuinfo|head -n1|sed -e 's/^.*: //'
echo "[INFO] Done."
echo "[ERROR] No Errors occurred!" >&2
