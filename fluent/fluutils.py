# -*- coding: utf-8 -*-
import os
import pickle


def get_fnames_by_ext(fnames, ext):
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


def check_undef(cur_mtimes, pre_mtimes):
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


def get_mtime(fnames):
    """Returns a dict fname: last_mod_time for files in fnames."""
    mtimes = {}
    for fname in fnames:
        last_mod_time = os.stat(fname)
        mtimes[fname] = last_mod_time.st_mtime
    return mtimes


def load_pre_mtimes(pfile, fnames):
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


def move_files(fname_fout, extensions, dest_dir):
    """Moves all files to dest_dir if they exist. This function will create
    a new folder inside dest_dir which is based on the filename of fname_out.
    The new folder will be called nairfoil_nsetup.

    Returns:
        True: if files were moved
        False: if we could not find all requested files. In this case no files
            will be moved.

    """
    fname, f_ext = os.path.splitext(fname_fout)
    # Check if all requested files are present
    for ext in extensions:
        cur_file = fname + ext
        if not os.path.isfile(cur_file):
            return False
    # Extract new folder name based on fname_fout
    new_folder_name = reshape_fname(fname_fout, ['nairfoil', 'nsetup'])
    dest_dir = os.path.join(dest_dir, new_folder_name)
    # Create directory if it does not exist
    # if not os.path.exists(dest_dir):
    #     os.makedirs(dest_dir)
    # Move files
    for ext in extensions:
        cur_file = fname + ext
        os.renames(cur_file, os.path.join(dest_dir, cur_file))
    return True


def reshape_fname(fname, order):
    """Splits fname at every '_' and returns a new file name based on order.

    Args:
        fname (string): Should be delimited by '_'
        order (list(str)): Defines the new order of the returned filename

    Returns:
        (str): Reordered filename

    """
    splits, _ = split_fname(fname)
    new_name = splits[order[0]]
    for key in order[1:]:
        new_name += '_{}'.format(splits[key])
    return new_name


def split_fname(fname):
    """Splits fname by '_' and returns a dictionary. The aoa contained in fname
    is also return as a float.

    """
    fname, f_ext = os.path.splitext(fname)
    fname_split = fname.split('_', 4)
    if len(fname_split) < 4:
        raise ValueError('The supplied string is not in the right format!')
    splits = {}
    splits['nairfoil'] = fname_split[0]
    splits['nsetup'] = fname_split[1]
    splits['ntype'] = fname_split[2]
    splits['aoa'] = fname_split[3]
    if len(fname_split) == 5:
        splits['optional'] = fname_split[4]
    aoa = float(fname_split[3][1:6])
    return splits, aoa
