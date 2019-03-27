$ cat multiple_commands_and_sleep.sh
#!/bin/bash

hostname
date
sleep 300
date
$ sbatch -t 00:06:00 -o multiple_commands_and_sleep.log < multiple_commands_and_sleep.sh