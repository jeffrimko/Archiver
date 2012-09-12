"""Builds the application to a Windows executable."""

from distutils.core import setup
import py2exe, sys, os

sys.argv.append('py2exe')
setup(
    options = {'py2exe': {'bundle_files': 1, 'dll_excludes': ["w9xpopen.exe"]}},
    windows = [{'script': "gui.pyw", 'dest_base':"archiver"}],
    zipfile = None,
)
