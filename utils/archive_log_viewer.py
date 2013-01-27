"""This module is a stand-alone script that takes
the path of a zip file as an argument. If the zip file
contains a text file of the same name, its contents will be displayed.
"""

##==============================================================#
## COPYRIGHT 2013, REVISED 2013, Jeff Rimko.                    #
##==============================================================#

##==============================================================#
## SECTION: Imports                                             #
##==============================================================#

import msvcrt   # Access to getch().
import os       # Access to path functions.
import sys      # Access to argv.
import zipfile  # Access to zip utilites.

##==============================================================#
## SECTION: Function Definitions                                #
##==============================================================#

def getLog(path):
    """Returns a list of lines from the log at the given path location."""
    log = []
    archive_name = os.path.splitext(path)[0]
    archive_name = os.path.split(archive_name)[1]
    archive = zipfile.ZipFile(path)
    for item in archive.infolist():
        root, ext = os.path.splitext(item.filename)
        if root == archive_name and ext == ".txt" or item.filename == "__archive_info__.txt":
            for line in  archive.open(item.filename).readlines():
                log.append(line)
            break
    return log

def viewLog(path):
    """Displays the contents of a text file (.txt) contained in a zip file (.zip) of the same name."""
    print "Showing log from archive:"
    print "    " + path + "\n"
    print "------------------------------"
    for line in getLog(path):
        print line.rstrip()
    print "------------------------------"
    print "\nPress any key to continue..."
    blockUntilKeypress()

def blockUntilKeypress():
    """Blocks until any key is pressed. Windows only."""
    char = None
    while not char:
        char=msvcrt.getch()

##==============================================================#
## SECTION: Main Body                                           #
##==============================================================#

if __name__ == "__main__":
    if len(sys.argv) > 1:
        viewLog(sys.argv[1])
