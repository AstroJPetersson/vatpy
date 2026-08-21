# -------------- Required packages
import os
import sys
import argparse
import numpy as np

# -------------- Import Vatpy TerminalPlot
from vatpy import Plot

# -------------- Vatpy Config
import configv


# -------------- Function to search for already generated frames:
def search_for_frames(output_dir, movie, format='png', skipsnapshots=0):
    # Check if vframes directory already exists or not:
    if os.path.isdir(f'{os.getcwd()}/vframes'):
        print('  * Directory for vframes detected!')
    else:
        print('  * Directory for vframes NOT detected!')
        print('    -> Creating a vframes directory')
        os.makedirs(f'{os.getcwd()}/vframes')

    # Check if some frames already have been generated or not:
    f = 0
    if skipsnapshots > 0:
        f += skipsnapshots
    frame = '000'[:3-len(str(f))] + str(f)
    if os.path.isdir(f'{os.getcwd()}/vframes/{movie}'):
        while os.path.isfile(f'{os.getcwd()}/vframes/{movie}/' +
                             f'{movie}_{frame}.{format}'):
            f += 1
            frame = '000'[:3-len(str(f))] + str(f)
        f_print = f
        if skipsnapshots > 0:
            f_print -= skipsnapshots
        print(f'  * Found {f_print} already generated frames in' +
              f' \'vframes/{movie}\'')
    else:
        print(f'  * Creating a \'{movie}\' subdirectory in vframes')
        os.makedirs(f'{os.getcwd()}/vframes/{movie}')

    # Seach for available snapshots:
    snapshot_nr_list = []
    for file in os.listdir(output_dir):
        if file.startswith('snap_'):
            file_split1 = file.split('.')
            file_split2 = file_split1[0].split('_')
            snapshot_nr_list.append(int(file_split2[1]))

    # Snapshots left to analyse:
    if np.max(snapshot_nr_list) > f:
        snapshots_left = ['000'[:3-len(str(s))] + str(s) for s in
                          np.arange(f, np.max(snapshot_nr_list)+1, 1)]
        snapshots_to_read = [f'snap_{s}.hdf5' for s in snapshots_left]

    # TODO
    save = f'{os.getcwd()}/vframes/{movie}/'
    name = f'{movie}'
    show = False

    return snapshots_to_read, save, name, show


# -------------- Snapshot or output directory argument
# Initialize argparse:
formatter_class = argparse.RawDescriptionHelpFormatter
parser = argparse.ArgumentParser(description='Script for Vatpy Plot',
                                 usage='vplot [options]',
                                 formatter_class=formatter_class)
parser._actions[0].help = 'Show this help message'
# Snapshot:
parser.add_argument('-s', '--snapshot', action='store',
                    help='''
                    Snapshot to analyse
                    ''')
# Output directory:
parser.add_argument('-o', '--outputdir', action='store',
                    help='''
                    Output directory to analyse
                    ''')

# -------------- Main arguments
parser.add_argument('-info', '--information', action='store_true',
                    help='''
                    Provide some general information about the given data
                    ''')
parser.add_argument('-checkrad', '--checkradiation', action='store_true',
                    help='''
                    Check the radiation output from stars and black holes in
                    the given data
                    ''')
parser.add_argument('-dens', '--density', action='store_true',
                    help='''
                    Generate a gas surface density map, either as a column
                    density, or as a slice through a given z-value (see -cut
                    for more details)
                    ''')
parser.add_argument('-temp', '--temperature', action='store_true',
                    help='''
                    Generate a density-weighted gas temperature map, either as
                    a projection, or as a slice through a given z-value (see
                    -cut for more details)
                    ''')
parser.add_argument('-bfield', '--magneticfield', action='store_true',
                    help='''
                    TODO
                    ''')
parser.add_argument('-res', '--resolution', action='store_true',
                    help='''
                    Generate a resolution plot, showing the mass and typical
                    cell radius, as a function of gas density, for all the gas
                    cells in the simulation domain
                    ''')
parser.add_argument('-stellar', '--stellarmaterial', action='store_true',
                    help='''
                    Generate a stellar surface density map
                    ''')
parser.add_argument('-dm', '--darkmatter', action='store_true',
                    help='''
                    Generate a dark matter surface density map
                    ''')
parser.add_argument('-sf', '--starformation', action='store_true',
                    help='''
                    Generate a star formation rate surface density map (plus
                    an underlying gas column density map or gas surface density
                    map sliced at a given z-value)
                    ''')
parser.add_argument('-sa', '--stellarage', action='store_true',
                    help='''
                    Generate a map highlighting the stellar age of newly formed
                    star particles (plus an underlying gas column density map
                    or gas surface density map sliced at a given z-value)
                    ''')
parser.add_argument('-sfr', '--starformationrate', action='store_true',
                    help='''
                    TODO
                    ''')
parser.add_argument('-bhevol', '--blackholeevolution', action='store_true',
                    help='''
                    Generate a collection of plots showing the time evolution
                    of various (sub-grid) properties for the central black hole
                    sink particle
                    ''')
parser.add_argument('-ffmpeg', '--ffmpeg', action='store', type=str,
                    help='''
                    TODO
                    ''')

# -------------- Technical arguments
parser.add_argument('-interpolation', '--interpolation', action='store',
                    default='kdtree', type=str,
                    help='Interpolation technique (default: kdtree)')
parser.add_argument('-xrange', '--xrange', action='store', default=None,
                    nargs=2, type=float,
                    help='Interpolation xrange (default: 0 to boxsize)')
parser.add_argument('-yrange', '--yrange', action='store', default=None,
                    nargs=2, type=float,
                    help='Interpolation yrange (default: 0 to boxsize)')
parser.add_argument('-zrange', '--zrange', action='store', default=None,
                    nargs=2, type=float,
                    help='Interpolation zrange (default: 0 to boxsize)')
parser.add_argument('-box', '--box', action='store', default=None, nargs=2,
                    type=float,
                    help='Interpolation box (default: 0 to boxsize)')
parser.add_argument('-bins', '--bins', action='store', default=100, type=int,
                    help='Number of bins in x, y and z (default: 100)')
parser.add_argument('-sfbins', '--starformationbins', action='store',
                    default=100, type=int, help='''
                    Number of bins in x and y when calculating the star
                    formation rate surface density (default: 100)
                    ''')
parser.add_argument('-levels', '--levels', action='store', default=5, type=int,
                    help='''
                    Number of contour levels (used by -res/--resolution)
                    ''')
parser.add_argument('-smooth', '--smooth', action='store', default=0, type=int,
                    help='''
                    Gaussian smooth level (used by -res/--resolution)
                    ''')
parser.add_argument('-vcr', '--variablecircradius', action='store_true',
                    default=False, help='''
                    Whether the flags for a variable circularisation radius is
                    active or not (important for -bhevol/--blackholeevolution)
                    ''')

# -------------- Specific plot arguments
parser.add_argument('-qty', '--quantity', action='store', default='mass',
                    type=str, help='''
                    Gas quantity [mass/n/HI/HII/H2/CO/He/e] (default: mass)
                    ''')
parser.add_argument('-ul', '--ulength', action='store',
                    default=configv.unit_for_length, type=str,
                    help='Unit length [kpc/pc] (default: see configv.py)')
parser.add_argument('-axis', '--axis', action='store', default='z', type=str,
                    help='Axis of rotation (default: z)')
parser.add_argument('-rotate', '--rotate', action='store', default=0,
                    type=float,
                    help='Amount of rotation [degrees] (default: 0)')
parser.add_argument('-cut', '--cut', action='store', default=None, type=float,
                    help='''
                    Cut in the gas surface density / temperature map
                    [coordinate in z] (default: none)
                    ''')
parser.add_argument('-bc', '--boxcenter', action='store_true', default=False,
                    help='Centre the data on middle point of the box')
parser.add_argument('-bf', '--bhfocus', action='store_true', default=False,
                    help='Centre the data on the BH')
parser.add_argument('-bs', '--bhshow', action='store_true', default=False,
                    help='Show the position(s) of the BH(s)')
parser.add_argument('-age', '--maxstellarage', action='store', default=100,
                    type=float, help='''
                    Maximum stellar age of newly formed star particles
                    ''')
parser.add_argument('-skip', '--skipsnapshots', action='store',
                    default=0, type=int,
                    help='Skip the first X snapshots when generating a movie')
parser.add_argument('-compare', '--comparetosnapshot', action='store',
                    default=None, nargs='+', type=str, help='''
                    TBD
                    ''')

# -------------- Common arguments
parser.add_argument('-vmin', '--vmin', action='store', default=None,
                    type=float, help='Colorbar vmin value (default: none)')
parser.add_argument('-vmax', '--vmax', action='store', default=None,
                    type=float, help='Colorbar vmax value (default: none)')
parser.add_argument('-xlim', '--xlim', action='store', default=None,
                    nargs=2, type=float, help='Axis xlim (default: xrange)')
parser.add_argument('-ylim', '--ylim', action='store', default=None,
                    nargs=2, type=float, help='Axis ylim (default: yrange)')
parser.add_argument('-movie', '--movie', action='store', default=False,
                    type=str, help='''
                    Generate a movie up to the given snapshot
                    ''')
parser.add_argument('-noxylabels', '--noxylabels', action='store_true',
                    default=False, help='Turn off X/Y labels')
parser.add_argument('-noxyticks', '--noxyticks', action='store_true',
                    default=False, help='Turn off X/Y ticks, and include' +
                    ' an information text above the figure instead')

# -------------- General arguments
parser.add_argument('-save', '--save', action='store',
                    default=f'{os.getcwd()}/vplots', help='''
                    Path to save generated figure at (default: current working
                    directory)
                    ''')
parser.add_argument('-name', '--name', action='store', default=None,
                    help='''
                    Name to save generated figure as (default: name of the
                    plotting function)
                    ''')
parser.add_argument('-format', '--format', action='store', default='png',
                    type=str, help='''
                    Format to save generated figure as (default: png)
                    ''')
parser.add_argument('-style', '--style', action='store',
                    default=configv.mplstyle, type=str, help='''
                    Matplotlib style sheet (default: see configv.py)
                    ''')
parser.add_argument('-show', '--show', action='store',
                    default=True, type=bool, help='''
                    Show generated figure or not (default: True)
                    ''')

# -------------- Read arguments (from the command line):
print('\nWelcome to VATPY Plot')
args = parser.parse_args()

# Check for possible conflicts:
if (args.snapshot is None) and (args.outputdir is None):
    sys.exit('  * Error: Missing snapshot (-s) or output directory (-o) to ' +
             'analyse\n  * Terminating script...\n')

if (args.snapshot is not None) and (args.outputdir is not None):
    sys.exit('  * Error: Both snapshot (-s) and output directory (-o) ' +
             'provided\n  * Terminating script...\n')

# 
if (args.outputdir is not None) and (args.movie is True):
    # print('  * Starting to generate movie frames up to snapshot: ' +
    #       f'{args.snapshot}')
    snapshots_to_read, save, name, show = search_for_frames(
        output_dir=args.outputdir, movie=args.movie, format=args.format,
        skipsnapshots=args.skipsnapshots)
elif (args.snapshot is not None) and (args.movie is False):
    snapshots_to_read = [args.snapshot]
    save = args.save
    name = args.name
    show = args.show
elif (args.snapshot is not None) and (args.movie is True):
    sys.exit('  * Warning: -movie argument was provided but can not be used ' +
             'with a snapshot argument, please provide an output directory ' +
             'instead (-o)')

# Loop over snapshot(s):
for snap in snapshots_to_read:
    plot = Plot(file=snap, style=args.style, save=save, name=name,
                format=args.format, vmin=args.vmin, vmax=args.vmax,
                xlim=args.xlim, ylim=args.ylim, ulengthselect=args.ulength,
                noxylabels=args.noxylabels, noxyticks=args.noxyticks,
                show=show)

    if args.information:
        plot.info()

    if args.checkradiation:
        plot.check_radiation()

    if args.density:
        plot.density(axis=args.axis, rotate=args.rotate,
                     quantity=args.quantity, bins=args.bins,
                     boxcenter=args.boxcenter, bhfocus=args.bhfocus,
                     bhshow=args.bhshow, xrange=args.xrange,
                     yrange=args.yrange, zrange=args.zrange, box=args.box,
                     cut=args.cut)

    if args.temperature:
        plot.temperature(axis=args.axis, rotate=args.rotate, bins=args.bins,
                         bhfocus=args.bhfocus, xrange=args.xrange,
                         yrange=args.yrange, zrange=args.zrange, box=args.box,
                         cut=args.cut)

    if args.magneticfield:
        plot.magneticfield(axis=args.axis, rotate=args.rotate, bins=args.bins,
                           bhfocus=args.bhfocus, xrange=args.xrange,
                           yrange=args.yrange, zrange=args.zrange,
                           box=args.box, cut=args.cut)

    if args.resolution:
        plot.resolution(bins=args.bins, levels=args.levels, smooth=args.smooth)

    if args.stellarmaterial:
        plot.stellarmaterial(axis=args.axis, rotate=args.rotate,
                             bins=args.bins, xrange=args.xrange,
                             yrange=args.yrange, zrange=args.zrange,
                             box=args.box)

    if args.darkmatter:
        plot.darkmatter(axis=args.axis, rotate=args.rotate, bins=args.bins,
                        xrange=args.xrange, yrange=args.yrange,
                        zrange=args.zrange, box=args.box)

    if args.starformation:
        plot.star_formation(axis=args.axis, rotate=args.rotate, bins=args.bins,
                            sfb=args.starformationbins, bhfocus=args.bhfocus,
                            xrange=args.xrange, yrange=args.yrange,
                            zrange=args.zrange, box=args.box, cut=args.cut)

    if args.stellarage:
        plot.stellar_age(axis=args.axis, rotate=args.rotate, bins=args.bins,
                         age=args.maxstellarage, bhfocus=args.bhfocus,
                         xrange=args.xrange, yrange=args.yrange,
                         zrange=args.zrange, box=args.box, cut=args.cut)

    if args.starformationrate:
        plot.star_formation_rate(
            compare_to_snapshot=args.comparetosnapshot)

    if args.blackholeevolution:
        plot.black_hole_evolution(vcr=args.variablecircradius)

    if args.ffmpeg:
        plot.ffmpeg(framedir=args.ffmpeg, skip=args.skipsnapshots)

print('  * Run completed!\n')

# -------------- End of file
