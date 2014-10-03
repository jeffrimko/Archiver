"""This script provides a GUI front-end for the Archiver utility."""

##==============================================================#
## DEVELOPED 2012, REVISED 2014, Jeff Rimko.                    #
##==============================================================#

##==============================================================#
## SECTION: Imports                                             #
##==============================================================#

import wx

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
        style = wx.TE_PROCESS_ENTER
        self.name_text = wx.TextCtrl(self, size=(300,-1), style=style)


        # Create text input for the archive log.
        log_label = wx.StaticText(self, label="Log Text:")
        style = wx.TE_MULTILINE | wx.TE_PROCESS_ENTER
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
        self.oname_text = wx.TextCtrl(self, size=(300,-1))

        # Create main control buttons and add to sizer.
        self.ok_button = wx.Button(self, wx.ID_OK)
        self.cancel_button = wx.Button(self, wx.ID_CANCEL)
        bttn_sizer.Add(self.ok_button, 0, wx.LEFT, 30)
        bttn_sizer.Add(self.cancel_button, 0, wx.LEFT, 90)

        prev_sizer.Add(prev_label, 0, wx.LEFT, 20)
        prev_sizer.Add(self.oname_text, 0, wx.LEFT, 20)

        # Add items to main sizer.
        main_sizer.Add(name_label, 0, wx.TOP | wx.LEFT, 20)
        main_sizer.Add(self.name_text, 0, wx.LEFT, 20)
        main_sizer.Add(log_label, 0, wx.TOP | wx.LEFT, 20)
        main_sizer.Add(self.log_text, 0, wx.LEFT | wx.BOTTOM, 20)
        main_sizer.Add(opts_sizer, 0, wx.LEFT, 20)
        main_sizer.Add(prev_sizer, 0, wx.TOP, 20)
        main_sizer.Add(bttn_sizer, 0, wx.TOP | wx.LEFT, 20)
        self.SetSizerAndFit(main_sizer)

        # This sets initial focus to the log text input.
        self.log_text.SetFocus()

class MainWindow(wx.Frame):
    """This class defines the main window."""

    def __init__(self, parent, title):
        """This function defines initialization logic of the main window."""
        self.parent = parent

        # This style disables the ability to resize the window.
        style = wx.DEFAULT_FRAME_STYLE
        style &= ~(wx.RESIZE_BORDER | wx.RESIZE_BOX | wx.MAXIMIZE_BOX)
        wx.Frame.__init__(self,
                parent,
                title=title,
                size=(350, 540),
                style=style)
        self.mainpanel = MainPanel(self)

    def disable(self):
        """Disables (grays out) the main window."""
        self.Disable()
        for widget in self.mainpanel.GetChildren():
            widget.Disable()

    def show(self):
        """Shows the main window."""
        self.Show(True)

    def show_warning(self, caption, message):
        """Shows a warning dialog."""
        dlg = wx.MessageDialog(self.parent, message, caption, wx.OK | wx.ICON_EXCLAMATION)
        dlg.ShowModal()
        dlg.Destroy()

    def show_error(self, caption, message):
        """Shows a error dialog."""
        dlg = wx.MessageDialog(self.parent, message, caption, wx.OK | wx.ICON_ERROR)
        dlg.ShowModal()
        dlg.Destroy()

##==============================================================#
## SECTION: Main Body                                           #
##==============================================================#

if __name__ == "__main__":
    app = wx.App(False)
    frame = MainWindow(None, "%s %s" % ("debug", "debug"))
    frame.show()
    frame.disable()
    # app.MainLoop()
    frame.show_warning("Foo", "Bar")
