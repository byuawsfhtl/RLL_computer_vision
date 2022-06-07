#!/bin/bash

#SBATCH --time=24:00:00   # walltime
#SBATCH --ntasks=4   # number of processor cores (i.e. tasks)
#SBATCH --nodes=1   # number of nodes
#SBATCH --gpus=1
#SBATCH --mem-per-cpu=8192M   # memory per CPU core
#SBATCH -J "1870_census_segmentation"   # job name
#SBATCH --array=1-1000 # number of albums
#SBATCH --mail-user=aoldroy2@byu.edu # email address
#SBATCH --mail-type=FAIL
#SBATCH --mail-type=END

# Compatibility variables for PBS. Delete if not needed.
export PBS_NODEFILE=`/fslapps/fslutils/generate_pbs_nodefile`
export PBS_JOBID=$SLURM_JOB_ID
export PBS_O_WORKDIR="$SLURM_SUBMIT_DIR"
export PBS_QUEUE=batch

# Set the max number of threads to use for programs using OpenMP. Should be <= ppn. Does nothing if the program doesn't use OpenMP.
export OMP_NUM_THREADS=$SLURM_CPUS_ON_NODE

# LOAD MODULES, INSERT CODE, AND RUN YOUR PROGRAMS HERE
module load python/3.8
cd /fslhome/aoldroy2/fsl_groups/fslg_census/compute/projects/
source segment_env/bin/activate

cd /fslhome/aoldroy2/fsl_groups/fslg_census/compute/projects/1870_census/imgs

if [ -z "$1" ]
then
     echo "please include the number to segment as an argument"
else
    offset=0
    SLURM_ARRAY_TASK_ID=$((SLURM_ARRAY_TASK_ID + offset))
    dir=$1
    album=$(sed -n ${SLURM_ARRAY_TASK_ID}p /fslgroup/fslg_census/compute/projects/1870_census/album_labels.txt)

    python /fslhome/aoldroy2/fsl_groups/fslg_census/compute/projects/1870_census/census_1870_segment.py $dir $album
fi
