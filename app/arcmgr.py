"""FIXME..."""

##==============================================================#
## COPYRIGHT 2014, REVISED 2014, Jeff Rimko.                    #
##==============================================================#

##==============================================================#
## SECTION: Imports                                             #
##==============================================================#

import os
import time

import arclib
import adoclib

##==============================================================#
## SECTION: Class Definitions                                   #
##==============================================================#

class ArcCreator:
    """Manages the creation of archives."""

    def __init__(self):
        #: The managed archive object.
        self.arc = None

        #: The archive's timestamp.
        self.ts = time.time()

        #{-- Archive setup attributes. --
        self.systargets = []   #: Path of system targets to archive.
        self.logtxt = ""       #: Text for log.
        self.name = ""         #: Name of the archive.
        self.outdir = "."      #: Output directory for the archive.
        self.logname = "__archive_info__.txt"  #: Filename of log.

        # The archive filename timestamp style.
        self.ts_style = "normal"
        # True if the original targets should be deleted from the filesystem
        # after archiving.
        self.delete = False
        # True if the directory structure should be flattened.
        self.flatten = False
        # True if no log file should be created.
        self.no_log = False
        #----}

        #{-- Archive post-creation attributes. --
        self.logpath = ""
        self.arctargets = []
        self.added = []
        self.notadded = []
        self.notdel = []
        #----}

    def guess_name(self):
        """Guesses an archive name if one was not explicitly given.

        :Postconditions:
          - Attribute ``name`` is set if empty.
        """
        if self.name:
            return
        if self.systargets:
            self.name = os.path.splitext(os.path.basename(self.systargets[0]))[0]
        else:
            self.name = "archive"

    def format_outname(self):
        """Formats an output filename.
        :Returns:
          - (str) The output filename (not full path) for the archive.
        """
        formatted = ""

        # Format timestamp.
        ts = arclib.format_ts(self.ts, self.ts_style)

        # Handle formatted name.
        if not self.name:
            self.guess_name()
        formatted = self.name
        if ts:
            formatted = "%s-%s" % (ts, formatted)
        return formatted + ".zip"

    def create_log(self):
        """Creates a log file.

        :Postconditions:
          - Log file will be created on the filesystem.
          - Attribute `logpath`` will be populated with the path to the created
            file, empty if no log created.
        """
        # Bail if log already exists.
        if self.logpath:
            return
        # Bail if log is not requested or there is no log text.
        if not self.logtxt:
            return
        if self.no_log:
            return

        # Create archive log file.
        log_ts = arclib.format_ts(self.ts, "formatted")
        logdoc = adoclib.format_doc(self.name, self.logtxt, date=log_ts)
        self.logpath = os.path.join(os.path.abspath(self.outdir), self.logname)
        f = open(self.logpath, "w")
        f.write(logdoc)

    def delete_log(self):
        """Deletes the previously created log file.

        :Postconditions:
          - If a log was created on the filesystem, it will be deleted.
        """
        if self.logpath:
            os.remove(self.logpath)

    def create_archive(self):
        """Creates an archive file.

        :Postconditions:
          - System targets in ``systargets`` will be converted to
            ``arctargets``.
          - An archive file will be created on the filesystem.
          - The attribute ``arc`` is set to the created archive.
        """
        # Bail if no targets.
        if not self.systargets:
            return

        outname = self.format_outname()
        self.create_log()

        # Prepare archive targets.
        self.arctargets = arclib.convert_systargets(self.systargets, flatten=self.flatten)
        if self.logpath:
            self.arctargets.append(arclib.ArcTarget(self.logpath, self.logname))

        # Create archive.
        arcpath = os.path.join(os.path.abspath(self.outdir), outname)
        self.arc = arclib.Archive(arcpath)
        self.arc.create()
        for a in self.arctargets:
            if self.arc.add(a):
                self.added.append(a)
            else:
                self.notadded.append(a)

        # TODO: Could check notadded to prevent deleting files that were
        # not archived.
        notdel = []
        if self.delete:
            notdel = arclib.delete_systargets(self.systargets)

##==============================================================#
## SECTION: Main Body                                           #
##==============================================================#

if __name__ == '__main__':
    a = ArcMgr()
    a.logtxt = "Just a test."
    # a.flatten = True
    a.systargets.append("brainstorm.txt")
    a.systargets.append("testdir")
    a.systargets.append(r"C:\Python27\Tools")
    # a.ts_style = "none"
    # a.no_ts = True
    # a.short_ts = True
    # a.long_ts = True
    # a.delete = True
    # print a.create_archive()
    print a.format_name()
