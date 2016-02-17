#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import matplotlib.pyplot as plt
import os
import fluutils as futils


def plot_convergence(fnames, fpaths, label):
    """Plots the convergence history of the files in matches."""
    for fname, fpath in zip(fnames, fpaths):
        _, cl_hist = futils.get_st_coeff(fpath)
        # Plot the convergence history
        fig = plt.figure(fname)
        ax_cl = fig.add_subplot(111)
        ax_cl.set_title(fname)
        ax_cl.plot(cl_hist, label=label)
        ax_cl.legend()
        ax_cl.grid(True)
        fig.canvas.draw()


if __name__ == "__main__":
    # get command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'dir', nargs='?', default=os.getcwd(),
        help='Top level directory from where to start scanning for polar data')
    args = parser.parse_args()

    # Find files
    fnames_cl, fpasths_cl = futils.find_files(args.dir, '*.cl')
    fnames_cd, fpasths_cd = futils.find_files(args.dir, '*.cd')

    plot_convergence(fnames=fnames_cl, fpaths=fpasths_cl, label='cl_hist')
    plot_convergence(fnames=fnames_cd, fpaths=fpasths_cd, label='cd_hist')

    plt.show()
