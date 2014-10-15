"""Graphical (GUI) utility for archiving files.

Target files and directories are passes as arguments to this utility.
"""

##==============================================================#
## COPYRIGHT 2014, REVISED 2014, Jeff Rimko.                    #
##==============================================================#

##==============================================================#
## SECTION: Imports                                             #
##==============================================================#

import os
import sys

import wx

import arcmgr
import garcview
from appinfo import GARCHIVER_NAME, GARCHIVER_VER

##==============================================================#
## SECTION: Global Definitions                                  #
##==============================================================#

#: Combined application name and version string.
NAMEVER = "%s %s" % (GARCHIVER_NAME, GARCHIVER_VER)

##==============================================================#
## SECTION: Class Definitions                                   #
##==============================================================#

class ArchiverApp(wx.App):
    def OnInit(self):
        self.arcctr = arcmgr.ArcCreator()
        self.mainwin = garcview.MainWindow(None, NAMEVER)

        # Local alias for main panel.
        panel = self.mainwin.mainpanel

        # Bind events to the methods containing the logic.
        self.Bind(wx.EVT_BUTTON, self.create_archive, panel.ok_button)
        self.Bind(wx.EVT_BUTTON, self.quit, panel.cancel_button)
        self.Bind(wx.EVT_CHECKBOX, self.update_ofile, panel.no_ts_cb)
        self.Bind(wx.EVT_CHECKBOX, self.update_ofile, panel.short_ts_cb)
        self.Bind(wx.EVT_TEXT, self.update_ofile, panel.name_text)
        self.Bind(wx.EVT_TEXT_ENTER, self.create_archive, panel.name_text)
        self.Bind(wx.EVT_TEXT_ENTER, self.create_archive, panel.log_text)
        self.Bind(wx.EVT_TEXT_ENTER, self.create_archive, panel.odir_text)
        return True

    def create_archive(self, event=None):
        """Create the archive and quits the application."""
        panel = self.mainwin.mainpanel

        # Update ArcMgr from view.
        self.arcctr.outdir = panel.odir_text.GetValue()
        self.arcctr.flatten = panel.flat_cb.GetValue()
        self.arcctr.delete = panel.del_cb.GetValue()
        self.arcctr.logtxt = panel.log_text.GetValue()

        # Create
        if not self.arcctr.create_archive():
            self.mainwin.show_error(NAMEVER, "Archive could not be created!")
        warning = ""
        if self.arcctr.warnmsgs:
            for w in self.arcctr.warnmsgs:
                warning += "%s\n" % w
            self.mainwin.show_warning(NAMEVER, warning)
        self.quit()

    def update_ofile(self, event=None):
        """Updates the output name TextCtrl on the main window."""
        panel = self.mainwin.mainpanel

        # Update ArcMgr from view.
        if panel.no_ts_cb.GetValue():
            self.arcctr.ts_style = "none"
        elif panel.short_ts_cb.GetValue():
            self.arcctr.ts_style = "short"
        else:
            self.arcctr.ts_style = "normal"
        self.arcctr.name = panel.name_text.GetValue()

        # Set view output name.
        outname = self.arcctr.format_outname()
        self.mainwin.mainpanel.ofile_text.ChangeValue(outname)

    def update_name(self, event=None):
        """Updates the archive name TextCtrl on the main window."""
        if not self.arcctr.name:
            self.arcctr.guess_name()
        self.mainwin.mainpanel.name_text.SetValue(self.arcctr.name)

    def guess_odir(self, event=None):
        """Guess the output directory based on the system targets."""
        panel = self.mainwin.mainpanel
        if self.arcctr.systargets:
            panel.odir_text.SetValue(os.path.dirname(os.path.abspath(self.arcctr.systargets[0])))

    def show_main(self, enabled=True):
        """Shows the main window."""
        if not enabled:
            self.mainwin.disable()
        self.update_name()
        self.guess_odir()
        self.update_ofile()
        self.mainwin.show()

    def run_loop(self):
        self.MainLoop()

    def quit(self, event=None):
        """Exit the application."""
        self.mainwin.Close()

    def show_notargets_warn(self):
        self.mainwin.show_warning(NAMEVER, "No targets provided.\nApplication will now close.")
        self.quit()

##==============================================================#
## SECTION: Main Body                                           #
##==============================================================#

if __name__ == '__main__':
    app = ArchiverApp()
    if len(sys.argv) >= 2:
        app.arcctr.systargets = sys.argv[1:]
        app.show_main()
        app.run_loop()
    else:
        app.show_main(enabled=False)
        app.show_notargets_warn()
