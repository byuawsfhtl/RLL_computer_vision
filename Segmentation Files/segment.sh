#!/bin/bash

#SBATCH --time=24:00:00   # walltime
#SBATCH --ntasks=4   # number of processor cores (i.e. tasks)
#SBATCH --nodes=1   # number of nodes
#SBATCH --gpus=1
#SBATCH --mem-per-cpu=8192M   # memory per CPU core
#SBATCH -J "death_segmentation"   # job name
#SBATCH --array=1-1000 # number of albums
#SBATCH --mail-user=youremail@email.com   # change to your email so you can be notified if the job fails
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
cd /fslhome/username/fsl_groups/fslg_groupname/compute/ # Change username and fslg_groupname (change this to the path where your enviroment is)
source your_env/bin/activate # change to the name of the enviroment you are using

cd /fslhome/username/fsl_groups/fslg_group/compute/projects/location_of_scripts # Change this to the location of your python script

offset=0
SLURM_ARRAY_TASK_ID=$((SLURM_ARRAY_TASK_ID + offset))
album=$(sed -n ${SLURM_ARRAY_TASK_ID}p /fslgroup/fslg_death/compute/projects/location_of_scripts/album_labels.txt) #change to location of "album_labels.txt"

python project_segment.py $album $year #change to the name of your python script
