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


def wtec_first(tfile, fpath):
    # Get zone name
    _, fname = os.path.split(fpath)
    zone_name, ext = os.path.splitext(fname)
    # Start adding lines
    lines = ['#!MC 1410\n']
    lines.append('$!READDATASET  \'"M" "F{}" "I1" "D,"\'\n'.format(fpath))
    lines.append("  DATASETREADER = 'Text Spreadsheet Loader'\n")
    lines.append("  READDATAOPTION = NEW\n")
    lines.append("  RESETSTYLE = YES\n")
    lines.append("  ASSIGNSTRANDIDS = NO\n")
    lines.append("  INITIALPLOTTYPE = XYLINE\n")
    lines.append("  INITIALPLOTFIRSTZONEONLY = NO\n")
    lines.append("  ADDZONESTOEXISTINGSTRANDS = NO\n")
    lines.append("$!RENAMEDATASETZONE\n")
    lines.append("  ZONE = 1\n")
    lines.append("  NAME = '{}'\n".format(zone_name))
    tfile.writelines(lines)


def wtec_append(tfile, fpath, zone_num):
    # Get zone name
    _, fname = os.path.split(fpath)
    zone_name, ext = os.path.splitext(fname)
    # Start adding lines
    lines = []
    lines.append('$!READDATASET  \'"M" "F{}" "I1" "D,"\'\n'.format(fpath))
    lines.append("  DATASETREADER = 'Text Spreadsheet Loader'\n")
    lines.append("  READDATAOPTION = APPEND\n")
    lines.append("  RESETSTYLE = NO\n")
    lines.append("  ASSIGNSTRANDIDS = NO\n")
    lines.append("  INITIALPLOTTYPE = XYLINE\n")
    lines.append("  INITIALPLOTFIRSTZONEONLY = NO\n")
    lines.append("  ADDZONESTOEXISTINGSTRANDS = NO\n")
    lines.append("$!RENAMEDATASETZONE\n")
    lines.append("  ZONE = {}\n".format(zone_num))
    lines.append("  NAME = '{}'\n".format(zone_name))
    tfile.writelines(lines)


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
    matches_txt = find_files(args.dir, '*.txt')
    matches_txt = sorted(matches_txt)
    if args.name:
        tfile = args.name
    else:
        tfile = 'load_polars.mcr'
    # Write tecplot macro
    with open(tfile, 'w') as f:
        for zone_num, fpath in enumerate(matches_txt):
            zone_num += 1
            if zone_num == 1:
                wtec_first(tfile=f, fpath=fpath)
            else:
                wtec_append(tfile=f, fpath=fpath, zone_num=zone_num)
