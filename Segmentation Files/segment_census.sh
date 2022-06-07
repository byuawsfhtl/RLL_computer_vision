                                                  
# Compatibility variables for PBS. Delete if not needed.
export PBS_NODEFILE=`/fslapps/fslutils/generate_pbs_nodefile`
export PBS_JOBID=$SLURM_JOB_ID
export PBS_O_WORKDIR="$SLURM_SUBMIT_DIR"
export PBS_QUEUE=batch

# Set the max number of threads to use for programs using OpenMP. Should be <= ppn. Does nothing if the program doesn't$export OMP_NUM_THREADS=$SLURM_CPUS_ON_NODE

# LOAD MODULES, INSERT CODE, AND RUN YOUR PROGRAMS HERE
module load python/3.8
cd /fslhome/<PUT YOUR SUPERCOMPUTER USERNAME HERE>/fsl_groups/fslg_census/compute/projects/
source segment_env/bin/activate

cd /fslhome/fsl_groups/fslg_census/compute/projects/PATH_TO_IMAGES_FOLDER

if [ -z "$1" ]
then
     echo "please include the number to segment as an argument"
else
    offset=0
    SLURM_ARRAY_TASK_ID=$((SLURM_ARRAY_TASK_ID + offset))
    dir=$1
    album=$(sed -n ${SLURM_ARRAY_TASK_ID}p /fslgroup/fslg_census/compute/projects/CHANGE_TO_PATH_TO_THIS_FILE/album_labels.txt)

    python /fslhome/fsl_groups/fslg_census/compute/projects/CHANGE_PATH_TO_PY_SEGMENTING_FILE/1900_segment.py $dir $album
fi