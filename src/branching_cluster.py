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
import numpy as np
#import matplotlib.pyplot as plt
import argparse
import math
import cPickle as pickle



#sns.set_style("whitegrid")
#sns.set_context("talk",font_scale=2.0)

parser = argparse.ArgumentParser()
parser.add_argument('--alpha', type=float, default=0.0)
parser.add_argument('--s', type=float, default=0.1)
parser.add_argument('--numsims',type=int,default=100)
parser.add_argument('--runno', type=int, default=0)
parser.add_argument('--name', type=str, default='test')

args=parser.parse_args()

alpha = args.alpha
s = args.s
numsims = args.numsims
runno = args.runno
name = args.name

def simulate_bp(s, alpha=0):
    trajectory = [1]
    gens = [0]
    gen = 0
    while (trajectory[-1] != 0 and trajectory[-1] < 10.0/s):
        n = trajectory[-1]
        overall_rate = n*(2+(1-alpha)*s+alpha*n*s)
        birth_prob = 1.0*n*(1+(1-alpha)*s+alpha*n*s)/overall_rate
        if np.random.rand() < birth_prob:
            trajectory.append(n+1)
        else:
            trajectory.append(n-1)
        gens.append(gens[-1]+np.random.exponential(1.0/overall_rate))
        gen += 1
#        if trajectory[-1] >= 10.0/s:
#            print s, alpha, len(trajectory)
    return trajectory, gens

extinct_traj = []
extinct_times = []
fixed_traj = []
fixed_times = []

sample_interval = int(math.ceil(0.1/s))

num_extinct = 0
for i in range(numsims):
    traj, gens = simulate_bp(s,alpha)
    sampled_traj = traj[::sample_interval]
    sampled_times = gens[::sample_interval]
    if traj[-1] == 0:
        num_extinct += 1
        if not len(traj)%sample_interval:
            sampled_traj.append(traj[-1])
            sampled_times.append(gens[-1])
        extinct_traj.append(sampled_traj)
        extinct_times.append(sampled_times)
    else:
        fixed_traj.append(sampled_traj)
        fixed_times.append(sampled_times)

with open('output/branching_process_sims_'+name+'/s_'+str(s)+'_alpha_'+str(alpha)+'_fixed_traj_'+str(runno)+'.pkl', 'w') as file:
    pickle.dump(fixed_traj, file)
with open('output/branching_process_sims_'+name+'/s_'+str(s)+'_alpha_'+str(alpha)+'_fixed_times_'+str(runno)+'.pkl', 'w') as file:
    pickle.dump(fixed_times, file)
with open('output/branching_process_sims_'+name+'/s_'+str(s)+'_alpha_'+str(alpha)+'_extinct_traj_'+str(runno)+'.pkl', 'w') as file:
    pickle.dump(extinct_traj, file)
with open('output/branching_process_sims_'+name+'/s_'+str(s)+'_alpha_'+str(alpha)+'_extinct_times_'+str(runno)+'.pkl', 'w') as file:
    pickle.dump(extinct_times, file)

#for traj in fixed_traj:
#    print s, len(traj)