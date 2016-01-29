#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import os
import fluutils as futils


if __name__ == "__main__":
    # get command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('dir', nargs='?', default=os.getcwd(),
                        help='Top level directory from where to start '
                        'scanning for polar data')
    parser.add_argument("-t", "--ftype", type=str,
                        help='In what data file do we want our polars?')
    args = parser.parse_args()

    # Load polars
    polars_df = futils.get_clcdcm(args.dir)
    # Write each polar to disc
    for airf_name, polar_df in polars_df.iteritems():
        # If no output is defined write as csv
        if args.ftype is None:
            fout = airf_name + '.txt'
            polar_df.to_csv(fout, index=False)
        else:
            if args.ftype.lower() == 'txt':
                fout = airf_name + '.txt'
                polar_df.to_csv(fout, index=False)
