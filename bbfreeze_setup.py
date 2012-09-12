"""Builds the application to an executable."""

from bbfreeze import Freezer

includes = []
excludes = ['_gtkagg', '_tkagg', 'bsddb', 'curses', 'email', 'pywin.debugger',
            'pywin.debugger.dbgcon', 'pywin.dialogs', 'tcl',
            'Tkconstants', 'Tkinter']
bbFreeze_Class = Freezer('dist', includes=includes, excludes=excludes)
bbFreeze_Class.addScript("gui.pyw", gui_only=True)
bbFreeze_Class.use_compression = 1
bbFreeze_Class.include_py = True
bbFreeze_Class()
