#!/bin/bash

echo "checking the CPU of this machine"
grep 'model name' /proc/cpuinfo|head -n1
echo "Done."
echo "No Errors occurred!" >2
