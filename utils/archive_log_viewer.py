"""This module is a stand-alone script that takes the path of a zip file as an
argument. If the zip file contains a text file of the same name or an archive
info file, its contents will be displayed.
"""

##==============================================================#
## DEVELOPED 2013, REVISED 2014, Jeff Rimko.                    #
##==============================================================#

##==============================================================#
## SECTION: Imports                                             #
##==============================================================#

import msvcrt   # Access to getch().
import os       # Access to path functions.
import sys      # Access to argv.
import zipfile  # Access to zip utilities.

##==============================================================#
## SECTION: Global Definitions                                  #
##==============================================================#

# Standard name for archive info files.
ARCINFO = "__archive_info__.txt"

##==============================================================#
## SECTION: Function Definitions                                #
##==============================================================#

def get_log(path):
    """Returns a list of lines from the log at the given path location."""
    log = []
    archive_name = os.path.splitext(path)[0]
    archive_name = os.path.split(archive_name)[1]
    archive = zipfile.ZipFile(path)
    for item in archive.infolist():
        root, ext = os.path.splitext(item.filename)
        if root == archive_name and ext == ".txt" or item.filename == ARCINFO:
            for line in  archive.open(item.filename).readlines():
                log.append(line)
            break
    return log

def view_log(path):
    """Displays the contents of a text file (.txt) contained in a zip file (.zip) of the same name."""
    print "Showing log from archive:"
    print "    " + path + "\n"
    print "------------------------------"
    for line in get_log(path):
        print line.rstrip()
    print "------------------------------"
    print "\nPress any key to continue..."
    block_until_keypress()

def block_until_keypress():
    """Blocks until any key is pressed. Windows only."""
    char = None
    while not char:
        char=msvcrt.getch()

##==============================================================#
## SECTION: Main Body                                           #
##==============================================================#

if __name__ == "__main__":
    if len(sys.argv) > 1:
        view_log(sys.argv[1])
