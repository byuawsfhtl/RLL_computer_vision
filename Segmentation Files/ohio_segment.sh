#!/bin/bash

#SBATCH --time=24:00:00   # walltime
#SBATCH --ntasks=4   # number of processor cores (i.e. tasks)
#SBATCH --nodes=1   # number of nodes
#SBATCH --gpus=1
#SBATCH --mem-per-cpu=8192M   # memory per CPU core
#SBATCH -J "death_segmentation"   # job name
#SBATCH --array=1-1000 # number of albums
#SBATCH --mail-user=logansowards@hotmail.com   # email address
#SBATCH --mail-type=FAIL

# Compatibility variables for PBS. Delete if not needed.
export PBS_NODEFILE=`/fslapps/fslutils/generate_pbs_nodefile`
export PBS_JOBID=$SLURM_JOB_ID
export PBS_O_WORKDIR="$SLURM_SUBMIT_DIR"
export PBS_QUEUE=batch

# Set the max number of threads to use for programs using OpenMP. Should be <= ppn. Does nothing if the program doesn't use OpenMP.
export OMP_NUM_THREADS=$SLURM_CPUS_ON_NODE

# LOAD MODULES, INSERT CODE, AND RUN YOUR PROGRAMS HERE
module load python/3.8
cd /fslhome/lojin/fsl_groups/fslg_death/compute/
source new_death_env/bin/activate

cd /fslhome/lojin/fsl_groups/fslg_death/compute/projects/ohio_death_3

if [ -z "$1" ]
then
     echo "please include the year to segment as an argument"
else
    offset=0
    SLURM_ARRAY_TASK_ID=$((SLURM_ARRAY_TASK_ID + offset))
    year=$1
    state=ohio
    album=$(sed -n ${SLURM_ARRAY_TASK_ID}p /fslgroup/fslg_death/compute/projects/"$state"_death_3/album_labels.txt)

    python ohio1949_seg_bound.py $album $year
fi
