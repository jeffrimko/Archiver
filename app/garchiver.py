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

CASELABEL = "Update Name Case"
NAMECASE = {
        "lower_case": lambda x: x.lower().replace(" ", "_").replace("-", "_"),
        "UPPER_CASE": lambda x: x.upper().replace(" ", "_").replace("-", "_"),
        "spinal-case": lambda x: x.lower().replace(" ", "-").replace("_", "-"),
    }

##==============================================================#
## SECTION: Class Definitions                                   #
##==============================================================#

class ArchiverApp(wx.App):
    def OnInit(self):
        self.arcctr = arcmgr.ArcCreator()
        cases = [CASELABEL] + list(NAMECASE.keys())
        self.mainwin = garcview.MainWindow(None, NAMEVER, cases)

        # Local alias for main panel.
        self.panel = self.mainwin.mainpanel

        # Bind events to the methods containing the logic.
        self.Bind(wx.EVT_BUTTON, self.create_archive, self.panel.ok_button)
        self.Bind(wx.EVT_BUTTON, self.quit, self.panel.cancel_button)
        self.Bind(wx.EVT_CHECKBOX, self.update_ofile, self.panel.no_ts_cb)
        self.Bind(wx.EVT_CHECKBOX, self.update_ofile, self.panel.short_ts_cb)
        self.Bind(wx.EVT_TEXT, self.update_ofile, self.panel.name_text)
        self.Bind(wx.EVT_COMBOBOX, self.update_case, self.panel.name_cbox)
        self.Bind(wx.EVT_KEY_DOWN, self.handle_keydown)
        return True

    def handle_keydown(self, event):
        """Handles key down event."""
        keycode = event.GetKeyCode()
        if keycode == wx.WXK_RETURN and not event.AltDown() and not event.ControlDown():
            self.create_archive()
        else:
            event.Skip()

    def create_archive(self, event=None):
        """Create the archive and quits the application."""
        # Update ArcMgr from view.
        self.arcctr.outdir = self.panel.odir_text.GetValue()
        self.arcctr.flatten = self.panel.flat_cb.GetValue()
        self.arcctr.flatten_ld = self.panel.flatld_cb.GetValue()
        self.arcctr.delete = self.panel.del_cb.GetValue()
        self.arcctr.logtxt = self.panel.log_text.GetValue()

        # Create archive.
        self.mainwin.disable()
        wait = wx.BusyInfo("Creating archive, please wait...")
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
        # Update ArcMgr from view.
        if self.panel.no_ts_cb.GetValue():
            self.arcctr.ts_style = "none"
        elif self.panel.short_ts_cb.GetValue():
            self.arcctr.ts_style = "short"
        else:
            self.arcctr.ts_style = "normal"
        self.arcctr.name = self.panel.name_text.GetValue()

        # Set view output name.
        outname = self.arcctr.format_outname()
        self.panel.ofile_text.ChangeValue(outname)

    def update_case(self, event=None):
        """Updates the case of the archive name."""
        sel = self.panel.name_cbox.GetStringSelection()
        name = self.panel.name_text.GetValue()
        if sel in NAMECASE.keys():
            name = NAMECASE[sel](name)
        self.panel.name_text.SetValue(name)
        self.panel.name_cbox.SetValue(CASELABEL)

    def update_name(self, event=None):
        """Updates the archive name TextCtrl on the main window."""
        if not self.arcctr.name:
            self.arcctr.guess_name()
        self.panel.name_text.SetValue(self.arcctr.name)

    def guess_odir(self, event=None):
        """Guess the output directory based on the system targets."""
        if self.arcctr.systargets:
            self.panel.odir_text.SetValue(os.path.dirname(os.path.abspath(self.arcctr.systargets[0])))

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

        # Only enable flatten leading directory if there is one target and it is
        # a directory.
        if 1 == len(app.arcctr.systargets) and os.path.isdir(app.arcctr.systargets[0]):
            pass
        else:
            app.mainwin.mainpanel.flatld_cb.Disable()

        app.show_main()
        app.run_loop()

    else:
        app.show_main(enabled=False)
        app.show_notargets_warn()
