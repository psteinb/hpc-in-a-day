$ cat multiple_commands.sh
#!/bin/bash

hostname
date
$ sbatch -o multiple_commands.log -e multiple_commands.err  < multiple_commands.sh