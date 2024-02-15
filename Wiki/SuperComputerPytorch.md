# PyTorch and CUDA Configuration for Supercomputer Usage

This document outlines the necessary steps and configurations required to utilize PyTorch with CUDA on the BYU supercomputer. These instructions are the result of collaborative efforts with the research computing office to resolve common issues encountered during setup.

## Configuration Steps

1. **Loading CUDA:** To use PyTorch with the supercomputer, CUDA must be loaded from the supercomputer's module system. For example, to load CUDA 11.8, you would use the command: ```module load cuda/11.8```
2. **Matching CUDA and PyTorch Versions:** Ensure the version of CUDA loaded is supported by the installed version of PyTorch. The latest version of CUDA on the supercomputer as of Febuary 15th, 2024 is 11.8, so the compatible version of PyTorch that supports CUDA 11.8 must be installed in Conda as well.
3. **Activating the Environment:** Load the CUDA module after activating the Conda environment to ensure detection. This is not necessarily required but is best practice according to the research computing office.

An example script to load and use pytorch is the following:
```
#!/bin/bash --login

#SBATCH --time=0:15:00   # walltime
#SBATCH --ntasks=1   # number of processor cores (i.e. tasks)
#SBATCH --nodes=1   # number of nodes
#SBATCH --gpus=1
#SBATCH --mem-per-cpu=10G   # memory per CPU core
#SBATCH -J "train_unet_grid"   # job name
#SBATCH --mail-user=example@byu.edu   # email address (update this to your email)
#SBATCH --mail-type=BEGIN
#SBATCH --mail-type=END
#SBATCH --mail-type=FAIL


# LOAD MODULES, INSERT CODE, AND RUN YOUR PROGRAMS HERE
mamba activate unet_seg
module load cuda/11.8
python script.py
```

## Job Submission Tips

- Submitting multiple small jobs is preferable to one large job. Because the scheduler prioritizes users based on their recent compute "volume" (CPU cores * memory allocated), small and large jobs will effect priority the same. However, multiple small jobs can run in parallel and be scheduled sooner, usually leading to quicker results.
