"""This script provides a GUI front-end for the Archiver utility."""

##==============================================================#
## DEVELOPED 2012, REVISED 2014, Jeff Rimko.                    #
##==============================================================#

##==============================================================#
## SECTION: Imports                                             #
##==============================================================#

import os
import sys
from time import sleep

import wx

import archiver
from archiver import create_archive, make_outname

##==============================================================#
## SECTION: Global Definitions                                  #
##==============================================================#

# The app name.
APPNAME = "gArchiver"

##==============================================================#
## SECTION: Class Definitions                                   #
##==============================================================#

class MainPanel(wx.Panel):
    """This class defines the main panel."""

    def __init__(self, parent):
        """This function defines initialization logic of the main panel."""
        wx.Panel.__init__(self, parent)

        # The parent is needed to make calls to close().
        self.parent = parent

        # Create the Sizers used for this panel.
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        opts_sizer = wx.BoxSizer(wx.VERTICAL)
        prev_sizer = wx.BoxSizer(wx.VERTICAL)
        bttn_sizer = wx.BoxSizer(wx.HORIZONTAL)

        # Create text input for the archive name.
        name_label = wx.StaticText(self, label="Archive Name:")
        style = wx.TE_MULTILINE | wx.HSCROLL | wx.TE_RICH
        self.name_text = wx.TextCtrl(self, size=(300,-1), style=style)
        archive_name = os.path.splitext(os.path.basename(sys.argv[1]))[0]
        self.name_text.ChangeValue(archive_name)

        # Create text input for the archive log.
        log_label = wx.StaticText(self, label="Log Text:")
        style = wx.TE_MULTILINE | wx.TE_RICH | wx.TE_PROCESS_ENTER
        self.log_text = wx.TextCtrl(self, size=(300,200), style=style)

        # Create option check boxes and add to sizer.
        self.no_ts_cb = wx.CheckBox(self, -1,
                "Do not include timestamp in archive name.")
        self.short_ts_cb = wx.CheckBox(self, -1,
                "Only timestamp to the day (hour:min otherwise).")
        self.del_cb = wx.CheckBox(self, -1,
                "Delete original files after archiving.")
        opts_sizer.Add(self.no_ts_cb, 0)
        opts_sizer.Add(self.short_ts_cb, 0, wx.TOP, 10)
        opts_sizer.Add(self.del_cb, 0, wx.TOP, 10)

        # Create output filename preview.
        prev_label = wx.StaticText(self, label="Output File Name:")
        style = wx.TE_MULTILINE | wx.HSCROLL | wx.TE_RICH
        self.prev_text = wx.TextCtrl(self, size=(300,-1), style=style)

        # Create main control buttons and add to sizer.
        ok_button = wx.Button(self, wx.ID_OK)
        cancel_button = wx.Button(self, wx.ID_CANCEL)
        bttn_sizer.Add(ok_button, 0, wx.LEFT, 30)
        bttn_sizer.Add(cancel_button, 0, wx.LEFT, 90)

        prev_sizer.Add(prev_label, 0, wx.LEFT, 20)
        prev_sizer.Add(self.prev_text, 0, wx.LEFT, 20)

        # Add items to main sizer.
        main_sizer.Add(name_label, 0, wx.TOP | wx.LEFT, 20)
        main_sizer.Add(self.name_text, 0, wx.LEFT, 20)
        main_sizer.Add(log_label, 0, wx.TOP | wx.LEFT, 20)
        main_sizer.Add(self.log_text, 0, wx.LEFT | wx.BOTTOM, 20)
        main_sizer.Add(opts_sizer, 0, wx.LEFT, 20)
        main_sizer.Add(prev_sizer, 0, wx.TOP, 20)
        main_sizer.Add(bttn_sizer, 0, wx.TOP | wx.LEFT, 20)
        self.SetSizerAndFit(main_sizer)

        # Bind events to the methods containing the logic.
        self.Bind(wx.EVT_BUTTON, self.create_new_archive, ok_button)
        self.Bind(wx.EVT_BUTTON, self.quit, cancel_button)
        self.Bind(wx.EVT_CHECKBOX, self.update_prev, self.no_ts_cb)
        self.Bind(wx.EVT_CHECKBOX, self.update_prev, self.short_ts_cb)
        self.Bind(wx.EVT_TEXT, self.update_prev, self.name_text)
        self.Bind(wx.EVT_TEXT_ENTER, self.create_new_archive, self.log_text)

        # Prepare the utility data.
        self.udata = archiver.UtilData()

        # Update output filename preview.
        self.update_prev()

        # This sets initial focus to the log text input.
        self.log_text.SetFocus()

    def quit(self, event):
        """Exit the application."""
        self.parent.Close()

    def update_prev(self, event=None):
        """Updates the output filename preview."""
        self.update_udata()
        self.prev_text.ChangeValue(make_outname(self.udata))

    def update_udata(self, event=None):
        """Updates the archiver utility data."""
        if len(sys.argv) > 1:
            # Since the typical use case for the GUI utility is to call it from
            # the Windows SendTo prompt, the archive should be created in the
            # directory where the call is made.
            if os.path.isfile(sys.argv[1]):
                self.udata['outdir'] = os.path.dirname(sys.argv[1])
                if not self.udata['outdir']:
                    # NOTE: During testing, if the current directory was the
                    # output directory, the output directory would be blank
                    # which would cause issues with the archiver module.
                    self.udata['outdir'] = "."
            elif os.path.isdir(sys.argv[1]):
                self.udata['outdir'] = os.path.normpath(
                        os.path.join(sys.argv[1], ".."))
            else:
                sys.exit("ERROR: Unknown target type!")
            self.udata['log_text'] = self.log_text.GetValue()
            self.udata['name'] = self.name_text.GetValue()
            self.udata['targets'] = sys.argv[1:]
            self.udata['no_ts'] = self.no_ts_cb.GetValue()
            self.udata['short_ts'] = self.short_ts_cb.GetValue()
            self.udata['delete'] = self.del_cb.GetValue()

    def create_new_archive(self, event):
        """Create a new archive."""
        self.update_udata()
        if self.udata['targets']:
            # Set the mouse cursor to waiting.
            wx.BeginBusyCursor()
            # Create archive.
            create_archive(self.udata, self.prev_text.GetValue())
            # Return the mouse cursor to normal.
            wx.EndBusyCursor()
        # Exit the application.
        self.quit(event)

class MainWindow(wx.Frame):
    """This class defines the main window."""

    def __init__(self, parent, title):
        """This function defines initialization logic of the main window."""
        # This style disables the ability to resize the window.
        style = wx.DEFAULT_FRAME_STYLE
        style &= ~(wx.RESIZE_BORDER | wx.RESIZE_BOX | wx.MAXIMIZE_BOX)
        wx.Frame.__init__(self,
                          parent,
                          title=title,
                          size=(350, 540),
                          style=style)
        panel = MainPanel(self)
        self.Show(True)

##==============================================================#
## SECTION: Main Body                                           #
##==============================================================#

if __name__ == "__main__":
    if len(sys.argv) >= 2:
        app = wx.App(False)
        frame = MainWindow(None, "%s %s" % (APPNAME, archiver.__version__))
        app.MainLoop()
