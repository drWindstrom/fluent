#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import matplotlib.pyplot as plt
import os
import fluutils as futils


def plot_convergence(matches, label):
    """Plots the convergence history of the files in matches."""
    for cur_file in matches:
        fname = cur_file[0]
        fpath = cur_file[1]
        _, cl_hist = futils.get_coeff(fpath)
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
    parser.add_argument('dir', nargs='?', default=os.getcwd(),
        help='Top level directory from where to start scanning for polar data')
    args = parser.parse_args()

    # Find files
    matches_cl = futils.find_files(args.dir, '*.cl')
    matches_cd = futils.find_files(args.dir, '*.cd')

    plot_convergence(matches_cl, label='cl_hist')
    plot_convergence(matches_cd, label='cd_hist')

    plt.show()
