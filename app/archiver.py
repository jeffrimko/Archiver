"""Utility for archiving files.

An archive is simply a zip file containing a log file plus
any additional files to archive. The standard used for the
log file is a text file named '__archive_info__.txt'.
The log is always in the root directory of the archive.

Usage:
  archiver  TARGET... [-m LOGMSG] [-n NAME]
  archiver -h | --help
  archiver --version

Arguments:
  TARGET   Path to a file or folder to archive.

Options:
  -m LOGMSG  Archive log message.
  -n NAME    Archive name.
  -h --help  Show this help message and exit.
  --version  Show version and exit.
"""

##==============================================================#
## COPYRIGHT 2012, REVISED 2013, Jeff Rimko.                    #
##==============================================================#

##==============================================================#
## SECTION: Imports                                             #
##==============================================================#

import os, shutil, sys, time
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
        self['files'] = []     # Path of files to archive.
        self['log_text'] = ""  # Text for log.
        self['name'] = ""      # Name of the archive.

        # True if a timestamp should be added to the archive name.
        self['add_timestamp'] = True
        # True if the original files should be deleted after archiving.
        self['del_originals'] = False
        # True if the timestamp should include time down to the second, otherwise to the day.
        self['precise_time'] = True

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

def create_archive(udata):
    """This function creates a new archive zip file. The archive file
    will be placed in the parent directory that is common to all target
    files.

    By default, the zip file will take the name of the first argument
    plus a time-stamp. For example, running the script using
    `python archiver.py  my_fileA.txt  my_fileB.doc` on 2 January 2010
    at 1:30pm will result in a zip archive named
    '201001021330-my_fileA.zip'.

    Parameters:
     - targets - Paths to the files and folders to add to the archive.
     - log_text - The text that will be written to the archive log.
     - name - The name of the archive. If an empty string, the default name will be used.
     - add_timestamp - True if a timestamp should be added to the archive name.
     - del_originals - True if the original files should be deleted after archiving.
     - precise_time - True if the timestamp should include time down to the second, otherwise to the day.
    """
    if not udata['targets']:
        sys.exit("ERROR: Must provide at least one target!")

    for t in udata['targets']:
        if (not os.path.isdir(t)) and (not os.path.isfile(t)):
            sys.exit("ERROR: Could not locate '%s'!" % (t))

    print "OK"
    exit()

    # Get the current time-stamp to be applied to the archive and the log.
    if precise_time:
        archive_time_stamp = time.strftime("%Y%m%d%H%M")
        log_time_stamp = time.strftime("%d %B %Y, ")
        log_time_stamp += ("%s") % (time.strftime("%I:%M%p (%Z)")).lstrip('0')
    else:
        archive_time_stamp = time.strftime("%Y%m%d")
        log_time_stamp = time.strftime("%d %B %Y")

    # Get the archive root directory.
    dir = os.path.dirname(targets[0])

    # If the archive name has not been explicitly defined, generate one from the
    # first target file name and the current timestamp.
    if not name:
        archive_name = os.path.splitext(os.path.basename(targets[0]))[0]
    else:
        archive_name = name

    # Determine the path of the log file for creation.
    log_name = "__archive_info__.txt"
    log_path = os.path.join(dir, log_name)

    # If a file exists that would conflict in name with the log, the log file is not created.
    if not os.path.exists(log_path):

        # Create the log file.
        log_file = open(log_path, 'w')
        log_file.write(archive_name + '\n')
        for _ in range(len(archive_name)):
            log_file.write("=")
        log_file.write("\n")
        log_file.write(":date: " + log_time_stamp + '\n\n')

        # Column correct the text of the log.
        for log_line in log_text:
            log_file.write(log_line)
        log_file.write("\n")
        log_file.close()

        # Add the log to the target files.
        targets.insert(0, log_path)
    else:
        status = "Cannot create log file due to name conflict."

    # Expand the relative paths of the target files and folder.
    base_targets = []
    for target in targets:
        base_targets.append(os.path.basename(target))
    files = _get_base_files(dir, base_targets)

    # Create the zip file for the archive.
    zip_name = archive_name + ".zip"
    if add_timestamp:
        zip_name = archive_time_stamp + '-' + zip_name
    zip_file = ZipFile(os.path.join(dir, zip_name), 'w', compression=ZIP_DEFLATED)

    # Add the files to the archive.
    for file in files:
        zip_file.write(os.path.join(dir, file), file)

    # Delete original files if the option is selected.
    # Otherwise, delete only the log file.
    try:
        if del_originals:
            # Delete files first.
            for file in files:
                os.remove(os.path.join(dir, file))

            # Delete folders once files are gone.
            for target in targets:
                if os.path.exists(target) and os.path.isdir(target):
                        shutil.rmtree(target)
        else:
            os.remove(log_path)
    except:
        status = str(sys.exc_info()[1])
    return status

def parse_args(args):
    print args
    udata = UtilData()
    udata['targets'] = args['TARGET']
    udata['log_text'] = args['-m']
    print udata
    return udata

def main():
    args = docopt(__doc__, version=__version__)
    udata = parse_args(args)
    create_archive(udata)

    if len(sys.argv) > 1:
        if "--version" == sys.argv[1]:
            print "archiver %s" % (__version__)
            sys.exit()
        elif "--help" == sys.argv[1]:
            print USAGE
            sys.exit()
        elif "-h" == sys.argv[1]:
            print USAGE
            sys.exit()
        # log_text = raw_input("Enter log contents: ")
        log_text = "BLAH"
        create_archive(sys.argv[1:], log_text)
    else:
        print USAGE

##==============================================================#
## SECTION: Main Body                                           #
##==============================================================#

if __name__ == "__main__":
    main()
