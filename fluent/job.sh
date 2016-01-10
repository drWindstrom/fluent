#!/bin/bash -login
#PBS -N SIMNAME
#PBS -M winstroth@tfd.uni-hannover.de
#PBS -m ae
#PBS -j oe
#PBS -l nodes=1:ppn=2
#PBS -l walltime=02:00:00
#PBS -l mem=2gb
#PBS -W x=PARTITION:lena:tane:taurus:tfd

# show which computer the job ran on
echo "Job ran on:" $(hostname)

# load the relevant modules
module load fluent/16.0

# change to work dir:
cd $PBS_O_WORKDIR

# the program to run in parallel
fluent -r16.0.0 2ddp -t2 -pinfiniband -mpi=intel -cnf=$PBS_NODEFILE -ssh -g -i in.jou > fluent.out

