#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""This script is used to monitor the base directory of the fluent simulations.

Example:


For support please contact Jan Winstroth
Email (winstroth@tfd.uni-hannover.de)

"""


import os
import pickle
import subprocess


def get_filenames_by_ext(fnames, ext):
    """Returns a list with all the files in fnames which have ext extension."""
    found_fnames = []
    for fname in fnames:
        if ext in fname:
            found_fnames.append(fname)
    return found_fnames


def check_convergence(fout):
    """Returns True if Fluent simulation has converged and False otherwise."""
    with open(fout, 'r') as f:
        fout_txt = f.read()
    if 'solution is converged' in fout_txt:
        return True
    else:
        return False


def check_divergence(fout):
    """Returns True if Fluent simulation has diverged and False otherwise."""
    with open(fout, 'r') as f:
        fout_txt = f.read()
    if 'Divergence detected' in fout_txt:
        return True
    else:
        return False


def get_last_mod_time(fnames):
    """Returns a dict fname: last_mod_time for files in fnames."""
    mtimes = {}
    for fname in fnames:
        last_mod_time = os.stat(fname)
        mtimes[fname] = last_mod_time.st_mtime
    return mtimes

def check_undefined_finish(fout):
    """Returns True if Fluent simulation has undefined (not converged nor 
       diverged) and False otherwise."""
    # Load modification times from last check if they exist
    pfile_mtimes = 'saved_mtimes.p'
    if os.path.isfile(pfile_mtimes):
        with open(pfile_mtimes, 'rb') as f:
            saved_mtimes = pickle.load(f)
    else:
        cur_mtimes = get_last_mod_time(fnames_fout)
        with open(pfile_mtimes, 'wb') as f:
            pickle.dump(cur_mtimes, f)
        return F


base_dir = '/home/fred/src/python/fluent'
os.chdir(base_dir)

# Get all files and folder in base directory
fnames_base_dir = os.listdir(base_dir)

# Find all shell script
jobs = get_filenames_by_ext(fnames_base_dir, '.sh')

# Send all shell scripts to cluster queue and delete if successfull
for job in jobs:
    try:
        subprocess.check_call(['qsub', job])
    except subprocess.CalledProcessError:
        pass
    except OSError:
        print('qsub command not found. Make sure qsub command is available.')
    else:
        os.remove(job)

# Check which simulations have converged, diverged or are undefined
fnames_fout = get_filenames_by_ext(fnames_base_dir, '.out')
# Start with convergence and divergence checks
for fname in fnames_fout:
    if check_convergence(fname):
        print('{} has converged!'.format(fname))
    if check_divergence(fname):
        print('{} has diverged!'.format(fname))






