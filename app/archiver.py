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
import zipfile
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
    """Object used to organize data within the archiver utility."""
    def __init__(self):
        self['targets'] = []   # Path of targets to archive.
        self['log_text'] = ""  # Text for log.
        self['name'] = ""      # Name of the archive.
        self['outdir'] = "."   # Output directory for the archive.

        # False if a timestamp should not be added to the archive name.
        self['no_ts'] = False
        # True if the original targets should be deleted from the file system after archiving.
        self['delete'] = False
        # True if the timestamp should only go to the day (hour:min otherwise).
        self['short_ts'] = False
        # True if the timestamp should go to the second (min:sec otherwise).
        self['long_ts'] = False
        # True if the directory structure should be flattened.
        self['flatten'] = False

##==============================================================#
## SECTION: Function Definitions                                #
##==============================================================#

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

def zip_targets(zippath, targets=[], top_files=[], flatten=False, delete=False):
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
    cpf = os.path.dirname(os.path.commonprefix(files))
    for f in files:
        zfiles.append(os.path.splitdrive(f[len(cpf):])[1])

    # Add top files to lists; top files will always be at the root of the zip archive.
    for f in top_files:
        f = os.path.abspath(f)
        if os.path.isfile(f):
            f = os.path.abspath(f)
            files.append(f)
            zfiles.append(os.path.basename(f))

    # Create zip archive and write files.
    archive = zipfile.ZipFile(zippath, "w")
    for f,z in zip(files, zfiles):
        if not flatten:
            archive.write(f, z)
        else:
            archive.write(f, os.path.basename(z))
        if delete:
            os.remove(f)

def create_archive(udata):
    """This function creates a new archive from the provided data."""
    if not udata['targets']:
        sys.exit("ERROR: Must provide at least one target!")

    # If the archive name has not been explicitly defined, generate one from the
    # first target file name and the current timestamp.
    if not udata['name']:
        udata['name'] = os.path.splitext(os.path.basename(udata['targets'][0]))[0]
    name = udata['name']
    name += ".zip"

    # Add timestamp to archive name.
    if not udata['no_ts']:
        if udata['long_ts']:
            name = "%s-%s" % (time.strftime("%Y%m%d%H%M%S"), name)
        elif udata['short_ts']:
            name = "%s-%s" % (time.strftime("%Y%m%d"), name)
        else:
            name = "%s-%s" % (time.strftime("%Y%m%d%H%M"), name)

    # Check that file with same name doesn't already exist.
    if os.path.isfile(name):
        sys.exit("ERROR: Archive named '%s' already exists!" % (name))

    # Create temporary directory.
    tmpdir = tempfile.mkdtemp()

    # Create archive info file.
    top_files = []
    if udata['log_text']:
        logpath = os.path.join(tmpdir, "__archive_info__.txt")
        if not create_notefile(logpath, udata['name'], udata['log_text']):
            shutil.rmtree(tmpdir)
            sys.exit("ERROR: Could not create archive info file!")
        top_files.append(logpath)

    # Create archive and zip targets.
    zip_targets(name, udata['targets'], top_files, udata['flatten'], udata['delete'])

    # Remove temporary directory.
    shutil.rmtree(tmpdir)

def create_notefile(path, title, txt="", attrs={}):
    """Creates an Asciidoc note file.

    **Parameters**:
      - path (str) - Path of the file to create.
      - title (str) - Title of the note file.
      - txt (str) - Text content of the note file.
      - attrs (dict) - Additional attributes to add to the file;
        by default only the `:date:` attribute is created.
    """
    # Generate timestamp.
    ts = time.strftime("%I:%M%p (%Z)").lstrip('0')

    # Check that path directory exists.
    path = os.path.abspath(path)
    if not os.path.isdir(os.path.dirname(path)):
        return None

    # Create the log file; write title and metadata.
    logfile = open(path, 'w')
    logfile.write(title + '\n')
    for _ in range(len(title)):
        logfile.write("=")
    logfile.write("\n")
    logfile.write(":date: " + ts + '\n')
    for key in attrs:
        logfile.write(":%s: %s\n" % (key, attrs[key]))
    logfile.write("\n")

    # Write text to file.
    logfile.write(txt)
    logfile.write("\n")
    logfile.close()
    return path

def parse_args(args):
    """Parses command line arguments into a UtilData object."""
    udata = UtilData()
    udata['targets'] = [os.path.abspath(t) for t in args['TARGET']]
    udata['name'] = args['--name']
    udata['log_text'] = args['-m']
    udata['short_ts'] = args['--short_timestamp']
    udata['long_ts'] = args['--long_timestamp']
    udata['no_ts'] = args['--no_timestamp']
    udata['delete'] = args['--delete']
    udata['flatten'] = args['--flatten']
    return udata

def main():
    args = docopt(__doc__, version=__version__)
    udata = parse_args(args)
    create_archive(udata)

##==============================================================#
## SECTION: Main Body                                           #
##==============================================================#

if __name__ == "__main__":
    main()
