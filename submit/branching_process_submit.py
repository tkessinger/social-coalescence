#!/usr/bin/env python

# Set your minimum acceptable walltime, format: day-hours:minutes:seconds
#SBATCH --time=0-00:30:00

# Set name of job shown in squeue
#SBATCH --job-name src/branching_cluster.py

# Request CPU resources
#SBATCH --ntasks=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=1
'''
branching.py
Author: Taylor Kessinger
Date: July 4, 2016
Description: Simulation of density independent (Desai and Fisher) and density dependent branching processes.
'''

import os
import shutil

s_range = {}
alpha_range = {}
numruns = {}
numsims = {}
s_range['160717'] = [0.00001,0.00003,0.0001,0.0003,0.001,0.003,0.01,0.03,0.1]
alpha_range['160717'] = [0,0.001,0.003,0.01,0.03,0.1]
#s_range['160717'] = [0.00001]
#alpha_range['160717'] = [0]
numruns['160717'] = 1
numsims['160717'] = 10000

name = '160717'

s_range,alpha_range,numruns,numsims = s_range[name],alpha_range[name],numruns[name], numsims[name]

if not os.path.exists('output/branching_process_sims_'+name):
    os.makedirs('output/branching_process_sims_'+name)

shutil.copy('src/branching_cluster.py', 'output/branching_process_sims_'+name)

for s in s_range:
    for alpha in alpha_range:
        for runno in range(numruns):
            call_list = ['sbatch', 'src/branching_cluster.py', '--name', name, '--s', str(s), '--alpha', str(alpha), '--numsims', str(numsims),
             '--runno', str(runno)]
            call = ' '.join(call_list)
            print call
            #sp.call(call)
            os.system(call)