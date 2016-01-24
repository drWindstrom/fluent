#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import matplotlib.pyplot as plt
import matplotlib.cm as cmx
import matplotlib.colors as colors
import os
import fluutils as futils


def get_cmap(N):
    '''Returns a function that maps each index in 0, 1, ... N-1 to a distinct
    RGB color.'''
    color_norm = colors.Normalize(vmin=0, vmax=N-1)
    scalar_map = cmx.ScalarMappable(norm=color_norm, cmap='hsv')

    def map_index_to_rgb_color(index):
        return scalar_map.to_rgba(index)
    return map_index_to_rgb_color


def plot_lift(polars_df, cmap=None):
    """Plots the lift polars."""
    i = 0
    for airf_name, polar_df in polars_df.iteritems():
        if cmap is None:
            fig_cl = plt.figure('Lift polar for {}'.format(airf_name))
            ax_cl = fig_cl.add_subplot(111)
            ax_cl.set_title('Lift polar for {}'.format(airf_name))
            ax_cl.plot(polar_df.index, polar_df.cl, '-ob', label='cl')
        else:
            fig_cl = plt.figure('Comparison of lift polars')
            ax_cl = fig_cl.add_subplot(111)
            ax_cl.set_title('Comparison of lift polars')
            ax_cl.plot(polar_df.index, polar_df.cl, color=cmap(i),
                       label=airf_name)
        ax_cl.legend()
        ax_cl.grid(True)
        fig_cl.canvas.draw()
        i += 1


def plot_drag(polars_df, cmap=None):
    """Plots the drag polars."""
    i = 0
    for airf_name, polar_df in polars_df.iteritems():
        if cmap is None:
            fig_cl = plt.figure('Drag polar for {}'.format(airf_name))
            ax_cl = fig_cl.add_subplot(111)
            ax_cl.set_title('Drag polar for {}'.format(airf_name))
            ax_cl.plot(polar_df.index, polar_df.cd, '-ob', label='cd')
        else:
            fig_cl = plt.figure('Comparison of drag polars')
            ax_cl = fig_cl.add_subplot(111)
            ax_cl.set_title('Comparison of drag polars')
            ax_cl.plot(polar_df.index, polar_df.cd, color=cmap(i),
                       label=airf_name)
        ax_cl.legend()
        ax_cl.grid(True)
        fig_cl.canvas.draw()
        i += 1


def plot_mom(polars_df, cmap=None):
    """Plots the moment polars."""
    i = 0
    for airf_name, polar_df in polars_df.iteritems():
        if cmap is None:
            fig_cl = plt.figure('Moment polar for {}'.format(airf_name))
            ax_cl = fig_cl.add_subplot(111)
            ax_cl.set_title('Moment polar for {}'.format(airf_name))
            ax_cl.plot(polar_df.index, polar_df.cm, '-ob', label='cd')
        else:
            fig_cl = plt.figure('Comparison of moment polars')
            ax_cl = fig_cl.add_subplot(111)
            ax_cl.set_title('Comparison of moment polars')
            ax_cl.plot(polar_df.index, polar_df.cm, color=cmap(i),
                       label=airf_name)
        ax_cl.legend()
        ax_cl.grid(True)
        fig_cl.canvas.draw()
        i += 1


if __name__ == "__main__":
    # get command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('dir', nargs='?', default=os.getcwd(),
        help='Top level directory from where to start scanning for polar data')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--cl', action="store_true", default=False,
        help='Plot only the lift polars')
    group.add_argument('--cd', action="store_true", default=False,
        help='Plot only the drag polars')
    group.add_argument('--cm', action="store_true", default=False,
        help='Plot only the moment polars')
    parser.add_argument('--compare', action="store_true",
        help='Plot all polars to the same figure in order to compare them')
    args = parser.parse_args()
    # Load polars
    polars_df = futils.get_clcdcm(args.dir)
    num_polars = len(polars_df)
    cmap = get_cmap(num_polars)

    if args.cl and args.compare:
        plot_lift(polars_df, cmap)
    elif args.cl and not args.compare:
        plot_lift(polars_df)
    elif args.cd and args.compare:
        plot_drag(polars_df, cmap)
    elif args.cd and not args.compare:
        plot_drag(polars_df)
    elif args.cm and args.compare:
        plot_mom(polars_df, cmap)
    elif args.cm and not args.compare:
        plot_mom(polars_df)
    else:
        plot_lift(polars_df)

    plt.show()
