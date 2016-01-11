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


def get_mod_time(fnames):
    """Returns a dict fname: last_mod_time for files in fnames."""
    mtimes = {}
    for fname in fnames:
        last_mod_time = os.stat(fname)
        mtimes[fname] = last_mod_time.st_mtime
    return mtimes


def load_pre_mod_times(pfile, fnames):
    """Loads and returns the last modification times of the fluent out files
       from the previous monitor run from the pickle file pfile. If pfile is
       not found, it returns the last modification time of all files in fnames
       as 0.0. This is required for the first iteration of the monitor loop,
       since we do have any last modification times.

    """
    if os.path.isfile(pfile):
        with open(pfile, 'rb') as f:
            return pickle.load(f)
    else:
        pre_mod_times = {}
        for fname in fnames:
            pre_mod_times[fname] = 0.0
        return pre_mod_times


def check_undefined_finish(cur_mtimes, pre_mtimes):
    """Checks if the fluent simulation has finished by comparing the last
    modification times of the fluent out file of the current monitor run
    (cur_times) with the modification times of the previous monitor run. If
    the modification did not increase in between monitor runs. The simulation
    is considered done.

    Args:
        cur_mtimes (dict): Modification times of the current monitor run. The
            dict keys are the file names of the .out files and the dict values
            are the last modification times of the .out files.
        pre_mtimes (dict): Modification times of the previous monitor run. The
            dict keys are the file names of the .out files and the dict values
            are the last modification times of the .out files.

    """
    results = {}
    for fname, cur_mtime in cur_mtimes.iteritems():
        if fname in pre_mtimes:
            if cur_mtime > pre_mtimes[fname]:
                results[fname] = False
            else:
                results[fname] = True
        else:
            results[fname] = False
    return results


def move_files(fname_fout, extensions, dest_dir):
    """Moves all files to dest_dir if they exist. Return True if files were
    moved and False if we could not find all requested files.

    """
    fname, f_ext = os.path.splitext(fname_fout)
    # Check if all requested files are present
    for ext in extensions:
        cur_file = fname + ext
        if not os.path.isfile(cur_file):
            return False
    # Create directory if it does not exist
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
    # Move files
    for ext in extensions:
        cur_file = fname + ext
        os.rename(cur_file, os.path.join(dest_dir, cur_file))
    return True


# Start of script
cwd = os.getcwd()
base_dir = '/home/winstroth/src/python/fluent/test_files'
os.chdir(base_dir)

# Get all files and folder in base directory
fnames_base_dir = os.listdir(base_dir)

# Get fluent out files
fnames_fout = get_filenames_by_ext(fnames_base_dir, '.out')
# Load last modification times of fluent out files,
pfile_mtimes = 'saved_mtimes.p'
previous_mtimes = load_pre_mod_times(pfile_mtimes, fnames_fout)
current_mtimes = get_mod_time(fnames_fout)
undef_finisher = check_undefined_finish(current_mtimes, previous_mtimes)

# Check which simulations have converged, diverged or are undefined
ext_to_move = ['.jou', '.cl', '.cd', '.cm', '.out', '.cas.gz', '.dat.gz']
conv_out = 'converged'
div_out = 'diverged'
undef_out = 'undefined'
for fname in fnames_fout:
    if check_convergence(fname):
        print('{} has converged!'.format(fname))
        move_files(fname, ext_to_move, conv_out)
    elif check_divergence(fname):
        print('{} has diverged!'.format(fname))
        move_files(fname, ext_to_move, div_out)
    elif undef_finisher[fname]:
        print('{} has finished undefined'.format(fname))
        move_files(fname, ext_to_move, undef_out)

# Find all shell script
jobs = get_filenames_by_ext(fnames_base_dir, '.qsh')
# Send all shell scripts to cluster queue and delete if successful
for job in jobs:
    try:
        subprocess.check_call(['qsub', job])
    except subprocess.CalledProcessError:
        pass
    except OSError:
        print('qsub command not found. Make sure qsub command is available.')
    else:
        os.remove(job)

# Get all files and folder in base directory
fnames_base_dir = os.listdir(base_dir)
# Get fluent out files
fnames_fout = get_filenames_by_ext(fnames_base_dir, '.out')
current_mtimes = get_mod_time(fnames_fout)
with open(pfile_mtimes, 'wb') as f:
    pickle.dump(current_mtimes, f)

# Change back to working directory of the beginning of the scripts
os.chdir(cwd)
