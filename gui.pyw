"""
This script provides a GUI front-end for the Archiver module.
"""

##==============================================================#
## COPYRIGHT 2012, REVISED 2012, Jeff Rimko.                    #
##==============================================================#

##==============================================================#
## SECTION: Imports                                             #
##==============================================================#

import os
import sys
from time import sleep

import wx

from archiver import create_archive

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
        cb_sizer = wx.BoxSizer(wx.VERTICAL)
        button_sizer = wx.BoxSizer(wx.HORIZONTAL)

        # Create text input for the archive name.
        name_label = wx.StaticText(self, label="Archive Name:")
        self.name_text = wx.TextCtrl(self, size=(300,-1), style=wx.TE_MULTILINE | wx.HSCROLL | wx.TE_RICH)
        archive_name = os.path.splitext(os.path.basename(sys.argv[1]))[0]
        self.name_text.ChangeValue(archive_name)

        # Create text input for the archive log.
        log_label = wx.StaticText(self, label="Log Text:")
        self.log_text = wx.TextCtrl(self, size=(300,200), style=wx.TE_MULTILINE | wx.TE_RICH | wx.TE_PROCESS_ENTER )

        # Create control checkboxes and add to sizer.
        self.date_cb = wx.CheckBox(self, -1, "Do not include timestamp in archive name.")
        self.prec_cb = wx.CheckBox(self, -1, "Only timestamp to the day (min:sec otherwise).")
        self.del_cb = wx.CheckBox(self, -1, "Delete original files after archiving.")
        cb_sizer.Add(self.date_cb, 0)
        cb_sizer.Add(self.prec_cb, 0, wx.TOP, 10)
        cb_sizer.Add(self.del_cb, 0, wx.TOP, 10)

        # Create main control buttons and add to sizer.
        ok_button = wx.Button(self, wx.ID_OK)
        cancel_button = wx.Button(self, wx.ID_CANCEL)
        button_sizer.Add(ok_button, 0, wx.LEFT, 30)
        button_sizer.Add(cancel_button, 0, wx.LEFT, 90)

        # Add items to main sizer.
        main_sizer.Add(name_label, 0, wx.TOP | wx.LEFT, 20)
        main_sizer.Add(self.name_text, 0, wx.LEFT, 20)
        main_sizer.Add(log_label, 0, wx.TOP | wx.LEFT, 20)
        main_sizer.Add(self.log_text, 0, wx.LEFT | wx.BOTTOM, 20)
        main_sizer.Add(cb_sizer, 0, wx.LEFT, 60)
        main_sizer.Add(button_sizer, 0, wx.TOP | wx.LEFT, 20)
        self.SetSizerAndFit(main_sizer)

        # Bind events to the methods containing the logic.
        self.Bind(wx.EVT_BUTTON, self.create_new_archive, ok_button)
        self.Bind(wx.EVT_TEXT_ENTER, self.create_new_archive, self.log_text)
        self.Bind(wx.EVT_BUTTON, self.quit, cancel_button)

        # This sets initial focus to the log text input.
        self.log_text.SetFocus()

    def quit(self, event):
        """Exit the application."""
        self.parent.Close()

    def create_new_archive(self, event):
        """Create a new archive."""
        if len(sys.argv) > 1:
            # Gather information for creation of archive.
            log_text = self.log_text.GetValue()
            archive_name = self.name_text.GetValue()
            add_timestamp = not self.date_cb.GetValue()
            del_originals = self.del_cb.GetValue()
            precise_time = not self.prec_cb.GetValue()

            # Set the mouse cursor to waiting.
            wx.BeginBusyCursor()

            # Create archive.
            status = create_archive(sys.argv[1:], log_text, archive_name, add_timestamp, del_originals, precise_time)

            # Return the mouse cursor to normal.
            wx.EndBusyCursor()

            if status != "success":
                # Display error dialog box if the archive creation was unsuccessful.
                dlg = wx.MessageDialog(self, status, "Archiver: Encountered Error", wx.OK | wx.ICON_ERROR)
                dlg.ShowModal()
                dlg.Destroy()

        # Exit the application.
        self.quit(event)

class MainWindow(wx.Frame):
    """This class defines the main window."""

    def __init__(self, parent, title):
        """This function defines initialization logic of the main window."""
        wx.Frame.__init__(self,
                          parent,
                          title=title,
                          size=(350, 470),
                          # This style disables the ability to resize the window.
                          style=wx.DEFAULT_FRAME_STYLE & ~(wx.RESIZE_BORDER | wx.RESIZE_BOX | wx.MAXIMIZE_BOX))
        panel = MainPanel(self)
        self.Show(True)

##==============================================================#
## SECTION: Main Body                                           #
##==============================================================#

if __name__ == "__main__":
    if len(sys.argv) >= 2:
        app = wx.App(False)
        frame = MainWindow(None, "Archiver")
        app.MainLoop()
