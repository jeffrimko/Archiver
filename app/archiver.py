"""Utility for archiving files.

An archive is simply a zip file containing a log file plus
any additional files to archive. The standard used for the
log file is a text file named `__archive_info__.txt`.
The log is always in the root directory of the archive.

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
  --no_name_ts      Do not include timestamp in archive name.
  --short_ts        Only timestamp to the day (min:sec otherwise).
  --delete          Delete original targets from file system after archiving.
  -h --help         Show this help message and exit.
  --version         Show version and exit.
"""

##==============================================================#
## COPYRIGHT 2012, REVISED 2013, Jeff Rimko.                    #
##==============================================================#

##==============================================================#
## SECTION: Imports                                             #
##==============================================================#

import os
import shutil
import tempfile
import sys
import time
from zipfile import ZipFile, ZIP_DEFLATED

from docopt import docopt

##==============================================================#
## SECTION: Global Definitions                                  #
##==============================================================#

# The version of the utility.
__version__ = "1.0.0"

##==============================================================#
## SECTION: Class Definitions                                   #
##==============================================================#

class UtilData(dict):
    """Object used to organize data within the utility."""
    def __init__(self):
        self['targets'] = []   # Path of targets to archive.
        self['log_text'] = ""  # Text for log.
        self['name'] = ""      # Name of the archive.
        self['outdir'] = "."   # Output directory for the archive.

        # False if a timestamp should not be added to the archive name.
        self['no_name_ts'] = False
        # True if the original targets should be deleted from the file system after archiving.
        self['delete'] = False
        # False if the timestamp should only go to the day (min:sec otherwise).
        self['short_ts'] = True

##==============================================================#
## SECTION: Function Definitions                                #
##==============================================================#

def _get_base_files(root_dir, base_targets):
    """Returns an expanded list of files starting from the root
    directory.

    Parameters:
     - root_dir - The absolute path of the root directory.
     - base_targets - A list of files or folders that exist in
       the root directory. Directories will be expanded.
    """
    files = []
    for target in base_targets:
        if os.path.isfile(os.path.join(root_dir, target)):
            files.append(target)
        elif os.path.isdir(os.path.join(root_dir, target)):
            dir_files = _get_base_files(os.path.join(root_dir, target), os.listdir(os.path.join(root_dir, target)))
            for file in dir_files:
                files.append(os.path.join(target, file))
    return files

def get_files(rootdir):
    """Returns a list of files contained in the given root directory and all
    subdirectories. List is returned as absolute paths of fies.
    """
    files = []
    for i in os.listdir(rootdir):
        ipath = os.path.join(rootdir, i)
        if os.path.isdir(ipath):
            files += get_files(ipath)
        elif os.path.isfile(ipath):
            files.append(ipath)
    return files

def zip_targets(zippath, targets, top_targets=[]):
    """Creates a zip file containing the given target files or directories."""
    # Gather the list of files to zip; expand directories.
    files = []
    for t in targets:
        t = os.path.abspath(t)
        if os.path.isdir(t):
            files += get_files(t)
        elif os.path.isfile(t):
            files.append(t)
        else:
            sys.exit("ERROR: Could not locate '%s'!" % (t))

    # Determine the zipfile name for each file.
    # Zipfile names are determined by removing the common prefix.
    zfiles = []
    cpf = os.path.commonprefix(files)
    for t in files:
        zfiles.append(os.path.splitdrive(t[len(cpf):])[1])

    # Create zip archive and write files.
    z = zipfile.ZipFile(zippath, "w")
    for a,b in zip(files, zfiles):
        z.write(a,b)

def get_timestamps(short_ts=False):
    """Get the current timestamp to be applied to the archive and the log."""
    if not short_ts:
        archive_ts = time.strftime("%Y%m%d%H%M")
        log_ts = time.strftime("%d %B %Y, ")
        log_ts += ("%s") % (time.strftime("%I:%M%p (%Z)")).lstrip('0')
    else:
        archive_ts = time.strftime("%Y%m%d")
        log_ts = time.strftime("%d %B %Y")
    return archive_ts, log_ts

def create_logfile(name, txt, ts=None):
    tmpdir = tempfile.mkdtemp()
    logpath = os.path.join(tmpdir, "__archive_info__.txt")

    # Create the log file.
    logfile = open(logpath, 'w')
    logfile.write(name + '\n')
    for _ in range(len(name)):
        logfile.write("=")
    logfile.write("\n")
    logfile.write(":date: " + ts + '\n\n')

    # Write text to file.
    for l in txt:
        logfile.write(l)
    logfile.write("\n")
    logfile.close()
    return logpath

def create_archive(udata):
    """This function creates a new archive zip file. The archive file
    will be placed in the parent directory that is common to all target
    files.

    By default, the zip file will take the name of the first argument
    plus a time-stamp. For example, running the script using
    `python archiver.py  my_fileA.txt  my_fileB.doc` on 2 January 2010
    at 1:30pm will result in a zip archive named
    '201001021330-my_fileA.zip'.
    """
    if not udata['targets']:
        sys.exit("ERROR: Must provide at least one target!")
    archive_ts, log_ts = get_timestamps(short_ts=udata['short_ts'])

    logpath = create_logfile(udata['name'], udata['log_text'])

    print zippath
    return status

def parse_args(args):
    udata = UtilData()
    udata['targets'] = [os.path.abspath(t) for t in args['TARGET']]
    udata['name'] = args['--name']
    udata['log_text'] = args['-m']
    udata['short_ts'] = args['--short_ts']
    udata['no_name_ts'] = args['--no_name_ts']
    udata['delete'] = args['--delete']
    return udata

def main():
    args = docopt(__doc__, version=__version__)
    udata = parse_args(args)

    # If the archive name has not been explicitly defined, generate one from the
    # first target file name and the current timestamp.
    if not udata['name']:
        udata['name'] = os.path.splitext(os.path.basename(udata['targets'][0]))[0]

    create_archive(udata)

##==============================================================#
## SECTION: Main Body                                           #
##==============================================================#

if __name__ == "__main__":
    main()
