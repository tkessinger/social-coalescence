#!/usr/bin/env python
'''
branching.py
Author: Taylor Kessinger
Date: July 4, 2016
Description: Simulation of density independent (Desai and Fisher) and density dependent branching processes.
'''
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_style("whitegrid")
sns.set_context("talk",font_scale=2.0)

def simulate_bp(genmax, s, alpha=0):
    trajectory = [1]
    gens = [0]
    gen = 0
#    while (gen < genmax and trajectory[-1] != 0 and trajectory[-1] < 100.0/s):
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
        if trajectory[-1] >= 10.0/s:
            print s, alpha, len(trajectory)
    return trajectory, gens

for s in [0.0001, 0.001, 0.01]:
    for alpha in [0, 0.001, 0.01,0.1]:
    #for alpha in [0]:
        fig=plt.figure(figsize=(12,10))
        num_extinct = 0
        num_trials = 100
        num_gens = 100000
        for i in range(num_trials):
            traj, gens = simulate_bp(num_gens,s,alpha)
            if traj[-1] == 0:
                num_extinct += 1
            else:
                plt.plot(gens, traj)
                plt.plot(gens[::100], traj[::100])
        ax=plt.gca()
        ax.set_yscale('log')
        if s != 0:
            plt.axhline(1.0/s,ls='--')
        plt.title('s = '+str(s)+' , alpha = '+str(alpha))
        plt.show()
        print s, alpha, 1.0*num_extinct/num_trials