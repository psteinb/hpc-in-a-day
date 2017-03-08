$ cat multiple_commands.sh
#!/bin/bash

hostname
date
$ sbatch -o multiple_commands.log < multiple_commands.sh