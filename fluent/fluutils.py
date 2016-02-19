# -*- coding: utf-8 -*-
import fnmatch
import numpy as np
import os
import pandas as pd
import pickle
import re
import sys
from math import sqrt


def get_fnames_by_ext(fnames, ext):
    """Returns a list with all the files in fnames which have ext extension."""
    found_fnames = []
    for fname in fnames:
        if ext in fname:
            found_fnames.append(fname)
    return found_fnames


# def check_convergence(fout):
#     """Returns True if Fluent simulation has converged and False
#     otherwise."""
#     with open(fout, 'r') as f:
#         fout_txt = f.read()
#     if 'solution is converged' in fout_txt:
#         return True
#     else:
#         return False


# def check_divergence(fout):
#     """Returns True if Fluent simulation has diverged and False otherwise."""
#     with open(fout, 'r') as f:
#         fout_txt = f.read()
#     if ('Divergence detected' in fout_txt and
#             'Halting due to end of file on input' not in fout_txt):
#         return True
#     else:
#         return False

def check_convergence(fout):
    """Returns the convergence state of the fluent simulation."""
    state = 'running'
    with open(fout, 'r') as f:
        fout_txt = f.read()
    if 'solution is converged' in fout_txt:
        state = 'converged'
        return state
    if ('Divergence detected' in fout_txt and
            'Halting due to end of file on input' not in fout_txt):
        state = 'diverged'
        return state
    if 'Halting due to end of file on input' in fout_txt:
        state = 'outOfIterations'
    return state


def check_sim_done(cur_mtimes, pre_mtimes):
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
    results = []
    for fname, cur_mtime in cur_mtimes.iteritems():
        if fname in pre_mtimes:
            if not cur_mtime > pre_mtimes[fname]:
                results.append(fname)
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


def move_files_checked(fname_fout, extensions, dest_dir):
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

    # Move files
    for ext in extensions:
        cur_file = fname + ext
        os.renames(cur_file, os.path.join(dest_dir, cur_file))
    return True


def move_files(fname_fout, root_dir, dest_dir):
    """Moves all files with same filename (excluding extension) as fname_out to
    dest_dir. This function will create a new folder inside dest_dir which is
    based on the filename of fname_out. The new folder will be called
    nairfoil_nsetup.

    """
    fname, f_ext = os.path.splitext(fname_fout)
    # Find files which filename of fname_fout
    matches = []
    pattern = fname + '*'
    root_fnames = os.listdir(root_dir)
    for filename in fnmatch.filter(root_fnames, pattern):
        matches.append([filename, os.path.join(root_dir, filename)])
    # Extract new folder name based on fname_fout
    new_folder_name = reshape_fname(fname_fout, ['nairfoil', 'nsetup'])
    dest_dir = os.path.join(dest_dir, new_folder_name)
    # Move files
    for cur_file in matches:
        os.renames(cur_file[1], os.path.join(dest_dir, cur_file[0]))


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
    f_ext = f_ext.replace('.', '')
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
    if fname_split[3][0] == 'm':
        aoa = -float(fname_split[3][1:6])
    elif fname_split[3][0] == 'p':
        aoa = float(fname_split[3][1:6])
    else:
        raise ValueError('The definition of aoa in the fname must be of format'
                         ' "m00.00" or "p00.00"')
    splits['ext'] = f_ext
    return splits, aoa


def create_sim_name(nairfoil, ntype, nsetup, aoa, optional=None):
    """ Returns the full name of the simulation. """
    # Take care of optional string
    if optional is None:
        optional = ''
    else:
        optional = '_{}'.format(optional)
    # Construct sim_name
    if aoa < 0:
        sim_name = '{}_{}_{}_m{:0=5.2f}{}'.format(nairfoil, nsetup, ntype,
                                                  abs(aoa), optional)
    else:
        sim_name = '{}_{}_{}_p{:0=5.2f}{}'.format(nairfoil, nsetup, ntype,
                                                  abs(aoa), optional)
    return sim_name


def walklevel(top_dir, level=None):
    """Extensions of os.walk() where we can provide a maximum recursion depth
    by level."""
    top_dir = top_dir.rstrip(os.path.sep)
    assert os.path.isdir(top_dir)
    num_sep = top_dir.count(os.path.sep)
    for root, dirs, files in os.walk(top_dir):
        yield root, dirs, files
        if level is not None:
            num_sep_this = root.count(os.path.sep)
            if num_sep + level <= num_sep_this:
                del dirs[:]


def find_files(top_dir, pattern, level=None):
    """Recursively finds all files in top_dir and all subdirectories which
    match pattern.

    Pattern uses unix shell-style wildcards and the following patterns are
    supported:
    *  matches everything
    ?  matches any single character
    [seq]  matches any character in seq
    [!seq]  matches any character not in seq

    Returns:
        tuple(list): ([filenames], [full path to files])

    """
    fnames = []
    fpaths = []
    for root, dirs, files in walklevel(top_dir=top_dir, level=level):
        for filename in fnmatch.filter(files, pattern):
            fnames.append(filename)
            fpaths.append(os.path.join(root, filename))
    return fnames, fpaths


def get_st_coeff(fname, skiprows=2, usecols=(1,)):
        """Loads the convergence history of the (cd, cl, cm depending on fname)
        coefficient from fname and return the convergence history and last
        entry from convergence history.

        """
        hist = np.loadtxt(fname, skiprows=skiprows, usecols=usecols)
        # Last entry in numpy array is the correct value
        last_entry = hist[-1]
        return last_entry, hist


def peak_det(v, delta, x=None):
    """Detects peaks in a vector.

    Finds the local maxima and minima ("peaks") in the vector v. A point is
    considered a maximum peak if it has the maximal value, and was preceded
    (to the left) by a value lower by delta. If the optional argument x is
    given, the indices in maxtab and mintab are replaced with the
    corresponding x-values.

    Args:
    v (List): Vector of the signal
    delta (float): Minimum delta between peaks and valley to be considered
        maxima or minima
    x (Optional[List]): Corresponding x values to the vector v

    Returns:
        tuple: (maxtab, mintab) maxtab and mintab consist of two columns.
        Column 1 contains indices of v, and column 2 the found values.

    Notes:
        Eli Billauer, 3.4.05 (Explicitly not copyrighted).
        This function is released to the public domain; Any use is allowed.

    """
    maxtab = []
    mintab = []

    if x is None:
        x = np.arange(len(v))

    v = np.asarray(v)

    if len(v) != len(x):
        sys.exit('Input vectors v and x must have same length')

    if not np.isscalar(delta):
        sys.exit('Input argument delta must be a scalar')

    if delta <= 0:
        sys.exit('Input argument delta must be positive')

    mn, mx = np.Inf, -np.Inf
    mnpos, mxpos = np.NaN, np.NaN

    lookformax = True

    for i in np.arange(len(v)):
        this = v[i]
        if this > mx:
            mx = this
            mxpos = x[i]
        if this < mn:
            mn = this
            mnpos = x[i]

        if lookformax:
            if this < mx - delta:
                maxtab.append((mxpos, mx))
                mn = this
                mnpos = x[i]
                lookformax = False
        else:
            if this > mn + delta:
                mintab.append((mnpos, mn))
                mx = this
                mxpos = x[i]
                lookformax = True

    return np.array(maxtab), np.array(mintab)


def get_tr_coeff(fname, skiprows=2, usecols=(1,), delta=1.0e-04, frac=5):
        """Loads the convergence history of the (cd, cl, cm depending on fname)
        coefficient from fname and return the convergence history and last
        entry from convergence history.

        """
        hist = np.loadtxt(fname, skiprows=skiprows, usecols=usecols)
        num_last = hist.size/frac
        hist_last = hist[-num_last:]
        maxtab, mintab = peak_det(v=hist_last, delta=delta)
        if maxtab.size == 0 or mintab.size == 0:
            # Return if no peaks or valleys are found
            return hist[-1], 0.0, hist
        else:
            # Get last peak and valley, calc amplitude and return mean, amp and
            # history
            coeff_max = maxtab[-1, 1]
            coeff_min = mintab[-1, 1]
            amp = (coeff_max - coeff_min)/2.0
            coeff = coeff_min + amp
            return coeff, amp, hist


def get_polar(top_dir, npolar='cl', pattern='*.cl'):
    """Returns polars extracted from fluent files which match pattern.

    This functions recursively scans the directory top_dir and all it's
    subdirectories for files that match pattern. From these files the last
    value of the data series is extracted and returned. The corresponding
    angle of attack is extracted from the filename. The data is organized in
    a dictionary. The keys identify the different simulations/polars and the
    values are pandas DataFrames which hold the polar data.

    Args:
        top_dir (str): Path to the root directory from where to start scanning
            for files that match pattern.
        npolar (str): Column name used for the pandas DataFrame to represent
            the data from the files.
        pattern (str): Unix shell-style wildcards to match file pattern. The
            following patterns are supported:
                *  matches everything
                ?  matches any single character
                [seq]  matches any character in seq
                [!seq]  matches any character not in seq

    Returns:
        dict(pd.DataFrame): The key identifies the simulation setup and the
            value holds the polar data inside a pandas DataFrame.

    """
    # Recursively find all files that match pattern
    fnames, fpaths = find_files(top_dir, pattern)
    # Loop over all matched files and extract the aoa and the coefficient
    polars = {}
    for fname, fpath in zip(fnames, fpaths):
        fname_parts, aoa = split_fname(fname)
        polar_id = '{}_{}'.format(fname_parts['nairfoil'],
                                  fname_parts['nsetup'])
        if polar_id not in polars:
            polars[polar_id] = []
        if fname_parts['ntype'].lower() == 'st':
            coeff_val, coeff_hist = get_st_coeff(fpath)
            # Since this is a steady simulation our coeff_val shoult be steady
            # without oscillations. Therefore we set the amplitutde to 0.0
            polars[polar_id].append([aoa, coeff_val, 0.0])
        elif fname_parts['ntype'].lower() == 'tr':
            coeff_val, amp, coeff_hist = get_tr_coeff(
                fname=fpath, skiprows=2, usecols=(1,), delta=1.0e-04, frac=5)
            polars[polar_id].append([aoa, coeff_val, amp])
    # Convert data to pandas Dataframe
    polars_df = {}
    for polar_id, polar_data in polars.iteritems():
        polars_df[polar_id] = pd.DataFrame(
            data=polar_data, columns=['aoa', npolar, npolar + '_amp'])
        # Order by aoa
        polars_df[polar_id].sort_values('aoa', inplace=True, ascending=True)
        # Set ordered column of aoa as index
        polars_df[polar_id].index = polars_df[polar_id].aoa
    return polars_df


def get_clcdcm(top_dir):
    """Returns all polars found in top_dir and it's subdirectories.

    This function uses get_polar() to find all files containing simulation
    data for cl, cd and cm. We start at top_dir and also include all
    subdirectories. The returned polars are organized in a pandas DataFrames.

    Args:
        top_dir (str): Path to root directory from where to start scanning

    Returns:
        dict(pd.DataFrame): The keys are the names of the simulation setups and
            the values are pandas Dataframes.
    """
    # Get all polars for cl, cd and cm
    cl_polars = get_polar(top_dir, npolar='cl', pattern='*.cl')
    cd_polars = get_polar(top_dir, npolar='cd', pattern='*.cd')
    cm_polars = get_polar(top_dir, npolar='cm', pattern='*.cm')
    # Get all keys and put them in a set
    cl_keys = cl_polars.keys()
    cd_keys = cd_polars.keys()
    cm_keys = cm_polars.keys()
    keys = set(cl_keys)
    keys.update(cd_keys)
    keys.update(cm_keys)
    # Combine polars of cl, cd and cm which have the same simulation setup
    polars_df = {}
    for polar_id in keys:
        # Define a new sorted index which includes all angles of attack.
        # This is necessary to handle missing data.
        index_set = set(cl_polars[polar_id].index)
        index_set.update(cd_polars[polar_id].index)
        index_set.update(cm_polars[polar_id].index)
        new_index = list(index_set)
        new_index = sorted(new_index)
        # Create new DataFrame which includes cl, cd and cm
        polars_df[polar_id] = pd.DataFrame(index=new_index)
        polars_df[polar_id]['aoa'] = new_index
        if polar_id in cl_polars:
            polars_df[polar_id]['cl'] = cl_polars[polar_id].cl
            polars_df[polar_id]['cl_amp'] = cl_polars[polar_id].cl_amp
        if polar_id in cd_polars:
            polars_df[polar_id]['cd'] = cd_polars[polar_id].cd
            polars_df[polar_id]['cd_amp'] = cd_polars[polar_id].cd_amp
        if polar_id in cm_polars:
            polars_df[polar_id]['cm'] = cm_polars[polar_id].cm
            polars_df[polar_id]['cm_amp'] = cm_polars[polar_id].cm_amp
    return polars_df


def write_journals(airfoils, jou_template, nsetup, ntype, out_dir,
                   kappa=1.4, Rs=287.102, T=288.15, nu=1.7984E-5, c=1.0):
    """Loads the template journal, updates the parameters and writes it to
    out_dir."""
    for nairfoil, sim_setup in airfoils.iteritems():
        # Calculate pressure
        Ma = sim_setup['mach']
        Re = sim_setup['reno']
        V = Ma*sqrt(kappa*Rs*T)
        rho = Re*nu/(V*c)
        p = rho*Rs*T
        t1step = 1.0/(V*10)
        t2step = 1.0/(V*100)

        for aoa in sim_setup['aoas']:
            # Create simulation name
            sim_name = create_sim_name(nairfoil, ntype, nsetup, aoa)
            # Create fluent journal file
            with open(jou_template, 'r') as f:
                jtxt = f.read()
            # Start to replace parameters inside the journal
            jtxt = jtxt.replace('AOA', str(aoa))
            jtxt = jtxt.replace('MACH', str(sim_setup['mach']))
            jtxt = jtxt.replace('PRESSURE', str(p))
            jtxt = jtxt.replace('T1STEP', str(t1step))
            jtxt = jtxt.replace('T2STEP', str(t2step))
            jtxt = jtxt.replace('CASE_FILE', '{}.cas'.format(nairfoil))
            jtxt = jtxt.replace('OUT.CL', '{}.cl'.format(sim_name))
            jtxt = jtxt.replace('OUT.CD', '{}.cd'.format(sim_name))
            jtxt = jtxt.replace('OUT.CM', '{}.cm'.format(sim_name))
            jtxt = jtxt.replace('OUT_TECPLOT', '{}.plt'.format(sim_name))
            jtxt = jtxt.replace('OUT_RESULTS', '{}.cas.gz'.format(sim_name))
            jtxt = jtxt.replace('AUTO_ROOT', '{}'.format(sim_name))
            # Write new journal to out_dir
            jname = sim_name + '.jou'
            if not os.path.exists(out_dir):
                os.makedirs(out_dir)
            with open(os.path.join(out_dir, jname), 'w') as f:
                f.write(jtxt)
    return True


def write_shell_scripts(airfoils, qsh_template, nsetup, ntype, out_dir):
    """Loads the template shell script, updates the parameters and writes it to
    out_dir."""
    for nairfoil, sim_setup in airfoils.iteritems():
        for aoa in sim_setup['aoas']:
            # Create simulation name
            sim_name = create_sim_name(nairfoil, ntype, nsetup, aoa)
            # Create fluent journal file
            with open(qsh_template, 'r') as f:
                qtxt = f.read()
            # Start to replace parameters inside the journal
            qtxt = qtxt.replace('SIMNAME', sim_name)
            qtxt = qtxt.replace('in.jou', sim_name + '.jou')
            qtxt = qtxt.replace('fluent.out', sim_name + '.out')
            # Write new shell script to out_dir
            qout = sim_name + '.qsh'
            if not os.path.exists(out_dir):
                os.makedirs(out_dir)
            with open(os.path.join(out_dir, qout), 'w') as f:
                f.write(qtxt)
    return True




# def restart_scan(top_dir, ext='*.jou'):
#     """Recursively scans top_dir and subdirectories for fluent journals and
#     returns the parameters needed to restart these simulations."""
#     # Find all files
#     jou_files, jou_paths = find_files(top_dir, ext)
#     # Define regular expressions
#     mach_pattern = re.compile(r'\(define *mach *([\+\-]*\d*\.\d*)\)')
#     chord_pattern = re.compile(r'\(define *chord *([\+\-]*\d*\.\d*)\)')
#     airfoils = {}
#     for jou_file, fout_path in zip(jou_files, jou_paths):
#         fname_parts, aoa = split_fname(jou_file)
#         nairfoil = fname_parts['nairfoil']
#         # Prepare data structure for airfoils
#         if nairfoil not in airfoils:
#             airfoils[nairfoil] = {}
#         if 'aoas' not in airfoils[nairfoil]:
#             airfoils[nairfoil]['aoas'] = []
#         # Start adding data to airfoils
#         airfoils[nairfoil]['aoas'].append(aoa)
#         with open(fout_path, 'r') as f:
#             txt = f.read()
#         # Find matches and convert to float
#         mach_matches = re.findall(mach_pattern, txt)
#         chord_matches = re.findall(chord_pattern, txt)
#         if len(mach_matches) > 1 or len(chord_matches) > 1:
#             raise IndexError('Found more than one match. This should not '
#                              'happen. Make sure each variable is only '
#                              'defined once in the journal.')
#         mach = float(mach_matches[0])
#         chord = float(chord_matches[0])
#         airfoils[nairfoil]['mach'] = mach
#         airfoils[nairfoil]['chord'] = chord
#     return airfoils
