#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""This script is used to monitor the base directory of the fluent simulations.

Example:


For support please contact Jan Winstroth
Email (winstroth@tfd.uni-hannover.de)

"""
import glob
import os
import pickle
import subprocess
import fluutils as futils


# Variable declaration
# mon_dir = '/home/winstroth/src/python/fluent/test_files'
mon_dir = '/bigwork/nhkcjwin/CFD/fluent/monitored_dir'
conv_dir = 'finished/converged'
div_dir = 'finished/diverged'
undef_dir = 'finished/undefined'
qsh_dir = 'qsh_backup'
pbs_dir = 'pbs_logs'
pfile_mtimes = 'saved_mtimes.p'
st_ext_res = ['.jou', '.cl', '.cd', '.cm', '.out', '.cas.gz', '.dat.gz',
              '.plt']


# Start of script
cwd = os.getcwd()
os.chdir(mon_dir)

# Get all files and folder in base directory
fnames_mon_dir = os.listdir(mon_dir)

# Get fluent out files
fnames_fout = futils.get_fnames_by_ext(fnames_mon_dir, '.out')

# Load last modification times of fluent out files,
prev_mtimes = futils.load_pre_mtimes(pfile_mtimes, fnames_fout)
cur_mtimes = futils.get_mtime(fnames_fout)
undef_finisher = futils.check_undef(cur_mtimes, prev_mtimes)

# Check which simulations have converged, diverged or are undefined
for fname in fnames_fout:
    state = futils.check_convergence(fname)
    if state == 'converged':
        # print('{} has converged!'.format(fname))
        futils.move_files_checked(fname, st_ext_res, conv_dir)
    elif state == 'diverged':
        # print('{} has diverged!'.format(fname))
        futils.move_files(fname, './', div_dir)
    elif state == 'outOfIterations':
        # print('{} has finished ran out of iterations'.format(fname))
        futils.move_files_checked(fname, st_ext_res, undef_dir)
    elif state == 'running' and undef_finisher[fname]:
        # print('{} has finished undefined'.format(fname))
        futils.move_files(fname, './', undef_dir)

# Get all pbs queue shell scripts
jobs = futils.get_fnames_by_ext(fnames_mon_dir, '.qsh')
# Send all shell scripts to cluster queue and move them if successful
for job in jobs:
    try:
        subprocess.check_call(['qsub', job])
    except subprocess.CalledProcessError:
        pass
    except OSError:
        print('qsub command not found. Make sure qsub command is available.')
    else:
        nfolder = futils.reshape_fname(job, ['nairfoil', 'nsetup'])
        njob = os.path.join(qsh_dir, nfolder, job)
        os.renames(job, njob)

# Move pbs logs to pbs_logs directory
pbs_lfiles = glob.glob('*.o????*')
for pbs_file in pbs_lfiles:
    nfolder = futils.reshape_fname(pbs_file, ['nairfoil', 'nsetup'])
    npbs = os.path.join(pbs_dir, nfolder, pbs_file)
    os.renames(pbs_file, npbs)

# Remove fluent cleanup shell scripts
flu_cleanup_files = glob.glob('cleanup-fluent*')
for cleanup_file in flu_cleanup_files:
    os.remove(cleanup_file)

# Save last modification times for all fluent out files in pickle file
fnames_mon_dir = os.listdir(mon_dir)
fnames_fout = futils.get_fnames_by_ext(fnames_mon_dir, '.out')
current_mtimes = futils.get_mtime(fnames_fout)
with open(pfile_mtimes, 'wb') as f:
    pickle.dump(current_mtimes, f)

# Change back to working directory of the beginning of the scripts
os.chdir(cwd)
