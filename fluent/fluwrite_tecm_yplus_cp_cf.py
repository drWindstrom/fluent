#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import fnmatch
import os


def find_files(top_dir, pattern):
    """Recursively finds all files in top_dir and all subdirectories which
    match pattern.

    Pattern uses unix shell-style wildcards and the following patterns are
    supported:
    *  matches everything
    ?  matches any single character
    [seq]  matches any character in seq
    [!seq]  matches any character not in seq

    Returns:
        list: full path to filename

    """
    matches = []
    for root, dirs, files in os.walk(top_dir):
        for filename in fnmatch.filter(files, pattern):
            matches.append(os.path.join(root, filename))
    return matches


def wtec_fload(tfile, fpaths):
    paths_str = ''
    for cur_path in fpaths:
        paths_str += '"{}" '.format(cur_path)

    lines = ['#!MC 1410\n']
    lines.append("$!READDATASET  ' {}'\n".format(paths_str))
    lines.append('READDATAOPTION = NEW\n')
    lines.append('RESETSTYLE = YES\n')
    lines.append('VARLOADMODE = BYPOSITION\n')
    lines.append('ASSIGNSTRANDIDS = YES\n')
    tfile.writelines(lines)


def wtec_rename_zones(tfile, fpaths):
    lines = []
    for i, cur_path in enumerate(fpaths):
        # Get zone name
        _, fname = os.path.split(cur_path)
        zone_name, ext = os.path.splitext(fname)
        # Add rename of zone to tecplot macro
        lines.append('$!RENAMEDATASETZONE\n')
        lines.append('ZONE = {}\n'.format(i + 1))
        lines.append("NAME = '{}'\n".format(zone_name))
    tfile.writelines(lines)


def wtec_rename_vars(tfile):
    line = ("$!RENAMEDATASETVAR\n"
            "  VAR = 4\n"
            "  NAME = 'yPlus'\n"
            "$!RENAMEDATASETVAR\n"
            "  VAR = 5\n"
            "  NAME = 'cp'\n"
            "$!RENAMEDATASETVAR\n"
            "  VAR = 6\n"
            "  NAME = 'cf'")
    tfile.writelines(line)


if __name__ == "__main__":
    # get command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('dir', nargs='?', default=os.getcwd(),
                        help='Top level directory from where to start '
                        'scanning for polar data')
    parser.add_argument("-n", "--name", type=str,
                        help='Specify the name of the tecplot macro.')

    args = parser.parse_args()

    # Find files
    matches_plt = find_files(args.dir, '*.plt')
    matches_plt = sorted(matches_plt)
    if args.name:
        tfile = args.name
    else:
        tfile = 'load_yplus_cp_cf.mcr'
    # Write tecplot macro
    with open(tfile, 'w') as f:
        wtec_fload(tfile=f, fpaths=matches_plt)
        wtec_rename_zones(tfile=f, fpaths=matches_plt)
        wtec_rename_vars(tfile=f)
