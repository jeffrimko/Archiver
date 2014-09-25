"""Utility for archiving files.

An archive is simply a zip file containing the archived
files plus an optional log file. The standard used for the
log file is a text file named `__archive_info__.txt`.
The log is always in the root directory of the archive.

By default, the archive filename will be prefixed with
a timestamp of the time created. The default format is the
following: `YYMMDDhhmm-<ARCHIVE_NAME>.zip`. Options are
provided to extend, shorten or remove the timestamp. If a
name for the archive is not explicitly given, the archive
name will be based on the name of the first target.

Usage:
  archiver [options] TARGET...
  archiver -h | --help
  archiver --version

Arguments:
  TARGET   Path to a file or folder to archive.

Options:
  -m LOGMSG         Archive log message.
  --outdir=OUTDIR   Directory to place generated files [default: .].
  --name=NAME       Archive name.
  --no_timestamp    Do not include timestamp in archive name.
  --short_timestamp Only timestamp to the day (hour:min otherwise).
  --long_timestamp  Timestamp to the second (hour:min otherwise).
  --delete          Delete original targets from file system after archiving.
  --flatten         Flatten directory structure in the zip archive.
  -h --help         Show this help message and exit.
  --version         Show version and exit.
"""

##==============================================================#
## DEVELOPED 2012, REVISED 2014, Jeff Rimko.                    #
##==============================================================#

##==============================================================#
## SECTION: Imports                                             #
##==============================================================#

import os
import sys

from docopt import docopt

import arcmgr

##==============================================================#
## SECTION: Global Definitions                                  #
##==============================================================#

# The version of the utility.
__version__ = "1.1.0"

##==============================================================#
## SECTION: Function Definitions                                #
##==============================================================#

# Function to write an error message to the console.
write_error = lambda s: sys.stderr.write("ERROR: " + s)

# Function to write an warning message to the console.
write_warning = lambda s: sys.stderr.write("WARNING: " + s)

def main():
    """Handles the main application logic."""
    args = docopt(__doc__, version="archiver %s" % (__version__))
    udata = parse_args(args)
    create_archive(udata)

def parse_args(args):
    """Parses command line arguments into a UtilData object."""
    arcctr = arcmgr.ArcCreator()
    arcctr.systargets = [os.path.abspath(t) for t in args['TARGET']]
    arcctr.name = args['--name']
    arcctr.logtxt = args['-m']
    if args['--long_timestamp']:
        arcctr.ts_style = "long"
    elif args['--short_timestamp']:
        arcctr.ts_style = "short"
    elif args['--no_timestamp']:
        arcctr.ts_style = "none"
    arcctr.delete = args['--delete']
    arcctr.flatten = args['--flatten']
    arcctr.outdir = args['--outdir']
    return arcctr

def main():
    args = docopt(__doc__, version="archiver %s" % (__version__))
    arcctr = parse_args(args)
    if not arcctr.create_archive():
        write_error("Archive could not be created! %s" % arcctr.errmsg)
    if arcctr.warnmsgs:
        for w in arcctr.warnmsgs:
            write_warning(w)

##==============================================================#
## SECTION: Main Body                                           #
##==============================================================#

if __name__ == "__main__":
    main()
