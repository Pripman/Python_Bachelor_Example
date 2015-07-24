#!/bin/bash

# #SBATCH --output=sbatch_output.txt#
#BATCH --job-name=run_verifyta
#SBATCH --ntasks=1
#SBATCH --time=10:00
#SBATCH --mem-per-cpu=100

srun python $1 $2 
