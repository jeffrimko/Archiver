##==============================================================#
## SECTION: Imports                                             #
##==============================================================#

import datetime
import os
import shutil
import time
import zipfile

##==============================================================#
## SECTION: Class Definitions                                   #
##==============================================================#

class Archive:
    def __init__(self, path):
        self.path = path
        self.zfile = None

    def exists(self):
        return os.path.exists(self.path)

    def create(self):
        if self.exists():
            return
        self.zfile = zipfile.ZipFile(self.path, "w")

    def contents(self):
        if not self.zfile:
            return []
        return self.zfile.namelist()

    def read_log(self):
        pass

    def add(self, arctarget):
        if not self.zfile:
            return False
        if not arctarget.zippath:
            return False
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
    def __init__(self, syspath="", zippath=""):
        self.syspath = syspath
        self.zippath = zippath

    def __repr__(self):
        return "syspath=%s  zippath=%s" % (self.syspath, self.zippath)

##==============================================================#
## SECTION: Function Definitions                                #
##==============================================================#

def format_ts(ts, style="normal"):
    ts = time.localtime(ts)
    if "none" == style:
        return ""
    elif "short" == style:
        return time.strftime("%Y%m%d", ts)
    elif "long" == style:
        return time.strftime("%Y%m%d%H%M%S", ts)
    elif "formatted" == style:
        return time.strftime("%d %B %Y %I:%M%p (%Z)", ts).lstrip('0')
    return time.strftime("%Y%m%d%H%M", ts)

def delete_systargets(systargets):
    notdel = []
    for s in systargets:
        if os.path.exists(s):
            if os.path.isfile(s):
                os.remove(s)
            elif os.path.isdir(s):
                shutil.rmtree(s)
            if os.path.exists(s):
                notdel.append(s)
    return notdel

def convert_systargets(targets, flatten=False):
    # Determine the zippath for each file.
    # Zipfile names are determined by removing the common prefix.
    arctargets = []

    sysexpand = []
    for s in targets:
        sysexpand.extend(expand_systarget(s))

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
    return arctargets

def expand_systarget(target, nofiles=False, nodirs=False):
    """FIXME Returns a list of files contained in the given root directory and all
    subdirectories. List is returned as absolute paths of fies.
    """
    if not os.path.isdir(target) and os.path.isfile(target):
        return [os.path.abspath(target)]
    subs = []
    for i in os.listdir(target):
        ipath = os.path.join(target, i)
        if os.path.isdir(ipath):
            if not nodirs:
                subs.append(os.path.abspath(ipath))
            subs += expand_systarget(ipath, nofiles=nofiles, nodirs=nodirs)
        elif os.path.isfile(ipath):
            if not nofiles:
                subs.append(os.path.abspath(ipath))
    return subs

##==============================================================#
## SECTION: Main Body                                           #
##==============================================================#

if __name__ == '__main__':
    print format_ts(time.time(), style="short")
    print format_ts(time.time(), style="normal")
    print format_ts(time.time(), style="long")
    print format_ts(time.time(), style="formatted")
    exit()
    name = "test.zip"
    if os.path.exists(name):
        os.remove(name)

    logpath = "__archive_info__.txt"
    create_log(logpath, "Test log.\nMore info!")

    systargets = []
    systargets.append(r"testdir\c_bitmanip")
    # systargets.append("testdir")
    # systargets.append("testdir2")
    # systargets.append(r"C:\Python27\Tools")

    arctargets = convert_systargets(systargets)
    arctargets.append(ArcTarget("__archive_info__.txt", "__archive_info__.txt"))

    arc = Archive(name)
    if not arc.exists():
        arc.create()
        for a in arctargets:
            arc.add(a)

    print arc.contents()

    # create_archive(name, arctargets, flatten=True)
    # print create_archive(name, arctargets)
    os.remove("__archive_info__.txt")
