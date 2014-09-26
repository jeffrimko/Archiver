"""This script contains objects that manage high-level operations on
archives.
"""

##==============================================================#
## DEVELOPED 2014, REVISED 2014, Jeff Rimko.                    #
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

        #: The archive filename timestamp style.
        self.ts_style = "normal"
        #: True if the original targets should be deleted from the filesystem
        #: after archiving.
        self.delete = False
        #: True if the directory structure should be flattened.
        self.flatten = False
        #: True if no log file should be created.
        self.no_log = False
        #: True if existing archive with same name should be overwritten.
        self.overwrite = False
        #----}

        #{-- Archive post-creation attributes. --
        #: Archive file path.
        self.arcpath = ""
        #: The log file path. Should only be populated if the log file
        #: currently exists on the filesystem (which is temporary).
        self.logpath = ""
        #: List of the archive targets.
        self.arctargets = []
        #: List of archive targets successfully added to the archive.
        self.added = []
        #: List of archive targets not added to the archive.
        self.notadded = []
        #: List of targets not able to be deleted (only if requested).
        self.notdel = []
        #: True if an existing archive with the same name was overwritten
        #: during creation.
        self.overwritten = False
        #: Holds error message if creation fails.
        self.errmsg = ""
        #: Holds warning messages.
        self.warnmsgs = []
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

        :Postconditions:
          - If the `name` attribute is not set, one will be guessed.

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

    def _create_log(self):
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
        log_ts = arclib.format_ts(self.ts, "expand")
        logdoc = adoclib.format_doc(self.name, self.logtxt, date=log_ts)
        self.logpath = os.path.join(os.path.abspath(self.outdir), self.logname)
        f = open(self.logpath, "w")
        f.write(logdoc)

    def _delete_log(self):
        """Deletes the previously created log file.

        :Postconditions:
          - If a log was created on the filesystem, it will be deleted.
        """
        if self.logpath:
            os.remove(self.logpath)
            self.logpath = ""

    def create_archive(self):
        """Creates an archive file.

        :Postconditions:
          - System targets in ``systargets`` will be converted to
            ``arctargets``.
          - An archive file will be created on the filesystem.
          - The attribute ``arc`` is set to the created archive.

        :Returns:
          - (bool) True if the archive was created, false otherwise.
        """
        # Bail if no targets.
        if not self.systargets:
            self.errmsg = "No system targets specified."
            return False

        # Prepare output path.
        outname = self.format_outname()
        self.arcpath = os.path.join(os.path.abspath(self.outdir), outname)
        if os.path.exists(self.arcpath):
            if not self.overwrite:
                self.errmsg = "Archive with same name exists and overwrite flag is not set."
                return False
            else:
                os.remove(self.arcpath)
                self.overwritten = True

        # Create archive.
        self._create_log()
        self.arc = arclib.Archive(self.arcpath)
        self.arc.create()
        self.arctargets, notfound = arclib.convert_sys2arc(self.systargets, flatten=self.flatten)
        if self.logpath:
            self.arctargets.append(arclib.ArcTarget(self.logpath, self.logname))
        # Iterate only through archive targets that have valid zip file paths.
        for a in [i for i in self.arctargets if i.zippath]:
            if self.arc.add(a):
                self.added.append(a)
            else:
                self.notadded.append(a)
        self._delete_log()

        # Delete added targets from the filesystem.
        self.notdel = []
        if self.delete:
            self.notdel = arclib.delete_from_filesys(self.arctargets, self.notadded)

        # Check for warnings during creation.
        if notfound:
            self.warnmsgs.append("Some system targets not found.")
        if self.notadded:
            self.warnmsgs.append("Some system targets not added to archive.")
        if self.notdel:
            self.warnmsgs.append("Some system targets not deleted as requested.")

        # Check that the archive file exists.
        if not os.path.exists(self.arcpath):
            self.errmsg = "Archive file could not be located."
            return False
        return True

##==============================================================#
## SECTION: Main Body                                           #
##==============================================================#

if __name__ == '__main__':
    a = ArcCreator()
    a.logtxt = "Just a test."
    a.ts_style = "none"
    a.overwrite = True
    # a.flatten = True
    a.systargets.append(r"testdir2\file.txt")
    a.systargets.append(r"testdir2\subdir\file.txt")
    # a.delete = True
    print a.create_archive()
    print a.arcpath
    print a.errmsg
    print a.warnmsgs
