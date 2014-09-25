"""This script contains a base library for the Archiver project."""

##==============================================================#
## DEVELOPED 2014, REVISED 2014, Jeff Rimko.                    #
##==============================================================#

##==============================================================#
## SECTION: Imports                                             #
##==============================================================#

import datetime
import os
import shutil
import time
import zipfile

##==============================================================#
## SECTION: Global Definitions                                  #
##==============================================================#

#: Default filename for the archive log.
DEFAULT_LOGNAME = "__archive_info__.txt"

##==============================================================#
## SECTION: Class Definitions                                   #
##==============================================================#

class Archive:
    """Base archive object."""
    def __init__(self, path):
        #: Path on the filesystem where the archive exists or will be created.
        self.path = path
        #: Zip file object of the archive.
        self.zfile = None

        # Open archive zip file if already exists.
        if self.exists():
            self.zfile = zipfile.ZipFile(self.path, "a")

    def exists(self):
        """Returns true if the archive file exists on the filesystem, false
        otherwise.
        """
        return os.path.exists(self.path)

    def create(self):
        """Creates the archive file on the filesystem.

        :Postconditions:
          - If the archive file already existed, it will not be overwritten.
        """
        if self.exists():
            return
        self.zfile = zipfile.ZipFile(self.path, "w")

    def contents(self):
        """Returns a list of archive contents."""
        if not self.zfile:
            return []
        return self.zfile.namelist()

    def logname(self):
        """Returns the archives log filename, if any."""
        # Determine the base name of the archive and derivatives in case
        # default log does not exist.
        base = os.path.splitext(os.path.basename(self.path))[0]
        base_txt = base + ".txt"
        base_log = base + ".log"
        base_md = base + ".md"

        log = ""
        c = self.contents()
        if DEFAULT_LOGNAME in c:
            log = DEFAULT_LOGNAME
        elif base_txt in c:
            log = base_txt
        elif base_log in c:
            log = base_log
        elif base_md in c:
            log = base_md
        return log

    def read_log(self):
        """Returns the text from the archive log, if one exists."""
        log = self.logname()
        if log:
            return self.zfile.read(log)
        return ""

    def add(self, arctarget):
        """Adds an archiver target to the archive.

        :Returns:
          - (bool) True if the target was successfully added, false otherwise.
        """
        if not self.zfile:
            return False
        if not arctarget.zippath:
            return True
        if not arctarget.syspath:
            return False
        if not os.path.exists(arctarget.syspath):
            return False
        if arctarget.zippath in self.contents():
            return False
        else:
            self.zfile.write(arctarget.syspath, arctarget.zippath)
        return True

class ArcTarget:
    """Object which maps a system target path to an archive target path."""
    def __init__(self, syspath="", zippath=""):
        #: The filesystem path of the system target which will be copied to the
        #: archive.
        self.syspath = syspath
        #: The archive path for the system target.
        self.zippath = zippath

    def __repr__(self):
        return "syspath=%s  zippath=%s" % (self.syspath, self.zippath)

##==============================================================#
## SECTION: Function Definitions                                #
##==============================================================#

def format_ts(ts, style="normal"):
    """Formats the given Unix timestamp.

    :param style: The requested format style (normal|none|short|long|expand).
    """
    ts = time.localtime(ts)
    if "none" == style:
        return ""
    elif "short" == style:
        return time.strftime("%Y%m%d", ts)
    elif "long" == style:
        return time.strftime("%Y%m%d%H%M%S", ts)
    elif "expand" == style:
        return time.strftime("%d %B %Y %I:%M%p (%Z)", ts).lstrip('0')
    return time.strftime("%Y%m%d%H%M", ts)

def delete_from_filesys(arctargets, ignore=[]):
    """Deletes the system target referenced by each archiver target from the
    filesystem.

    :param arctargets: List of archiver targets.

    :Returns:
      - List of system targets that were not deleted.
    """
    notdel = []

    # Delete files first.
    for a in arctargets:
        if a in ignore:
            continue
        if os.path.exists(a.syspath) and os.path.isfile(a.syspath):
            try:
                os.remove(a.syspath)
            except:
                pass
            if os.path.exists(a.syspath):
                notdel.append(a.syspath)

    # Delete directories last.
    for a in arctargets:
        if a in ignore:
            continue
        if os.path.exists(a.syspath) and os.path.isdir(a.syspath):
            # Do not delete directories that contain subfiles.
            if [] == expand_systarget(a.syspath, nodirs=True):
                try:
                    shutil.rmtree(a.syspath)
                except:
                    pass
            if os.path.exists(a.syspath):
                notdel.append(a.syspath)

    return notdel

def convert_sys2arc(targets, flatten=False):
    """Converts list of system targets to equivalent archiver targets.

    :param targets: List of system targets.
    :param flatten: (bool) If true, the archiver targets will all be placed in
        the archive root. If false, the archive structure will reflect the
        system structure.

    :Returns:
      - Tuple with the following:
          - List of archiver targets.
          - List of system targets not found.
    """
    # Determine the zippath for each file.
    # Zipfile names are determined by removing the common prefix.
    arctargets = []
    notfound = []

    sysexpand = []
    for s in targets:
        if os.path.exists(s):
            sysexpand.extend(expand_systarget(s))
        else:
            notfound.append(s)

    # Determine the common path prefix (cpp) for the system targets. This prefix
    # will be used as the basis of the relative path that will be used for the
    # zip path.
    if 1 == len(targets) and os.path.isdir(targets[0]):
        # NOTE: If only a single directory was provided as a system target, use
        # the parent directory as the prefix. Otherwise, the given directory
        # will be used for the prefix resulting in the child subs being in the
        # archive root rather than the directory itself.
        cpp = os.path.abspath(os.path.dirname(targets[0]))
    else:
        cpp = os.path.dirname(os.path.commonprefix(sysexpand))

    # Populate list of archiver targets from the expanded system targets.
    for s in sysexpand:
        a = ArcTarget(syspath=s)
        if flatten:
            if os.path.isfile(a.syspath):
                a.zippath = os.path.basename(a.syspath)
            else:
                a.zippath = None
        else:
            # If common path prefix is empty, it typically means that there are
            # targets are separate drives.
            if not cpp:
                a.zippath = os.path.splitdrive(a.syspath)[1]
            else:
                a.zippath = os.path.relpath(a.syspath, cpp)
        arctargets.append(a)
    return (arctargets, notfound)

def expand_systarget(target, nofiles=False, nodirs=False):
    """Expands the given system target. For files, the result will be the
    absolute path. For directories, the result will be the absolute paths of
    all subfiles and subdirectories.

    :param nofiles: If true, no files will be returned.
    :param nodirs: If true, no directories will be returned.

    :Returns:
      - List of expanded system targets.
    """
    expanded = []
    abspath = os.path.abspath(target)

    # Handle files.
    if os.path.isfile(abspath) and not nofiles:
        return [abspath]

    # Handle directories.
    if os.path.isdir(abspath):
        if not nodirs:
            expanded.append(abspath)
        for i in os.listdir(abspath):
            ipath = os.path.join(abspath, i)
            expanded.extend(expand_systarget(ipath, nofiles=nofiles, nodirs=nodirs))

    return expanded

##==============================================================#
## SECTION: Main Body                                           #
##==============================================================#

if __name__ == '__main__':
    print expand_systarget("testdir2")
