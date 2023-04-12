#!/bin/bash
#SBATCH --time=2:00:00   # walltime
#SBATCH --ntasks=1   # number of processor cores (i.e. tasks)
#SBATCH --nodes=1   # number of nodes
#SBATCH --gpus=1
#SBATCH --mem-per-cpu=4096M   # memory per CPU core
#SBATCH -J "rowSegment"   # job name
#SBATCH --mail-user=myemail@example.com   # email address
echo "$USER: Please change the --mail-user option to your real email address before submitting. Then remove this line."; exit 1
#SBATCH --mail-type=END
#SBATCH --mail-type=FAIL


# Set the max number of threads to use for programs using OpenMP. Should be <= ppn. Does nothing if the program doesn't use OpenMP.
export OMP_NUM_THREADS=$SLURM_CPUS_ON_NODE

# LOAD MODULES, INSERT CODE, AND RUN YOUR PROGRAMS HERE
module load python/3.8
source ~/fsl_groups/fslg_census/compute/envs/detectron2/bin/activate
python segmentation.py
