#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import os
import fluutils as futils
import pandas as pd


if __name__ == "__main__":
    # get command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('dir', nargs='?', default=os.getcwd(),
                        help='Top level directory from where to start '
                        'scanning for polar data. Defaults to CWD.')
    parser.add_argument('-t', '--ftype', type=str, default='txt',
                        choices=['txt', 'excel', 'pickle'],
                        help='In what file type do we want our polars?. '
                        'Defaults to "txt" which is a csv file.')
    parser.add_argument('-n', '--nout', type=str, default='polars',
                        help='In case of ftype "excel" you can '
                        'specify the name of the output file without '
                        'extension with this flag.')
    args = parser.parse_args()

    # Load polars
    polars_df = futils.get_clcdcm(args.dir)
    # Ouput to csv
    if args.ftype.lower() == 'txt':
        for airf_name, polar_df in polars_df.iteritems():
            fout = airf_name + '.txt'
            polar_df.to_csv(fout, index=False)
    # Output to pickle
    if args.ftype.lower() == 'pickle':
        for airf_name, polar_df in polars_df.iteritems():
            fout = airf_name + '.p'
            polar_df.to_pickle(fout)
    # Output to excel
    if args.ftype.lower() == 'excel':
        fout = args.nout + '.xlsx'
        writer = pd.ExcelWriter(path=fout)
        for airf_name, polar_df in polars_df.iteritems():
            polar_df.to_excel(writer, airf_name, index=False)
        writer.save()
