#!/bin/bash
#SBATCH -J 2000b0500l4000d5
#SBATCH -o output_2000b0500l4000d5.txt
#SBATCH -e errors_2000b0500l4000d5.txt
#SBATCH -t 04:00:00
# request 32 MPI tasks
#SBATCH -n 1
#SBATCH -p arrow
#SBATCH -c 4

cd /home/dovigoamin/AminTesi/Cluster/
#your working directory

srun ./GG.sh
