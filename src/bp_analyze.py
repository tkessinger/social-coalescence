#!/usr/bin/env python
'''
bp_analyze.py
Author: Taylor Kessinger
Date: July 18, 2016
Description: Analysis and visualization of branching process outputs: comparison with analytical results.
'''

import numpy as np
import matplotlib.pyplot as plt
import argparse
import math
import glob
import cPickle as pickle

date = '160717'

filelist = glob.glob('output/branching_process_sims_'+date+'/*')
filelist.remove('output/branching_process_sims_'+date+'/branching_cluster.py')

bp_data = {}
max_times = {}
s_vals = []
alpha_vals = []
filelist.sort()
for filename in filelist:
    parsed_name = filename.split('_')
    filetype = parsed_name[7]+'_'+parsed_name[8]
    s = float(parsed_name[4])
    alpha = float(parsed_name[6])
    if not s in s_vals:
        s_vals.append(s)
    if not alpha in alpha_vals:
        alpha_vals.append(alpha)
    if not (filetype, s, alpha) in bp_data.keys():
        bp_data[(filetype,s,alpha)] = []
    with open(filename, 'r') as infile:
        datalist = pickle.load(infile)
    print filetype, s, alpha, len(datalist)
    for data in datalist:
        bp_data[(filetype,s,alpha)].append(data)
for key in bp_data.keys():
    if (key[0] == 'fixed_times' or key[0] == 'extinct_times') and len(bp_data[key]) > 0:
        max_times[key] = max([data[-1] for data in bp_data[key]])

extinct_pdfs = {}
fixed_pdfs = {}
extinct_times = {}
fixed_times = {}

for s in s_vals:
    for alpha in alpha_vals:
        time_key = ('fixed_times', s, alpha)
        traj_key = ('fixed_traj', s, alpha)
        if len(bp_data[traj_key]) > 0:
            fixed_times[(s, alpha)]=np.zeros([len(bp_data[traj_key]),np.int(max_times[time_key])])
            fixed_pdfs[(s,alpha)] = np.zeros([len(bp_data[traj_key]),np.int(max_times[time_key])])
            timepoints = bp_data[time_key]
            traj = bp_data[traj_key]
            for ti, timepoints in enumerate(bp_data[time_key]):
                int_times = [int(np.ceil(time)) for time in timepoints]
                indices = []
                #[indices.append(x) for x in unique(int_times+[max_times[time_key]])]
                [indices.append(x) for x in np.unique(int_times)]
                for ii, time_index in enumerate(indices[:-1]):
                    fixed_pdfs[(s,alpha)][ti,indices[ii]:indices[ii+1]] = bp_data[traj_key][ti][ii]
                    fixed_times[(s,alpha)][ti,indices[ii]:indices[ii+1]] = bp_data[time_key][ti][ii]
                fixed_pdfs[(s,alpha)][ti,indices[-1]:] = bp_data[traj_key][ti][ii+1]
                fixed_times[(s,alpha)][ti,indices[-1]:] = bp_data[time_key][ti][ii+1]

def df_approx(s,timepoints):
    nmax = 10.0/s
    avg_val = np.zeros(len(timepoints))
    for n in np.arange(nmax):
        df_dist = 1.0*s/((1+s)*np.exp(s*timepoints)-1-s)*np.exp(-1.0*s*n/((1+s)*np.exp(s*timepoints)-1))
        avg_val += n*df_dist
    return avg_val

for key in fixed_pdfs.keys():
    if key[1] == 0:
        plt.figure()
        plt.title(key)
        for ti,traj in enumerate(fixed_pdfs[key]):
            plt.plot(fixed_times[key][ti],traj,ls = '--')
        plt.plot(np.arange(np.max(fixed_times[key])),df_approx(s,np.arange(np.max(fixed_times[key]))))
        ax=plt.gca()
        ax.set_yscale('log')
        plt.ylim([1,1.0/key[0]])


'''
for key in bp_data.keys():
    if key[0] == 'extinct_times':
        extinct_times[key] = np.zeros(max_times[key])
        extinct_pdfs[key] = []
        for data in bp_data[key]:
            int_times = [int(ceil(time)) for time in data]
'''