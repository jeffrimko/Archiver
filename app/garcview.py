"""This script provides a GUI front-end for the Archiver utility."""

##==============================================================#
## DEVELOPED 2012, REVISED 2014, Jeff Rimko.                    #
##==============================================================#

##==============================================================#
## SECTION: Imports                                             #
##==============================================================#

import wx

##==============================================================#
## SECTION: Global Definitions                                  #
##==============================================================#

#: Defines the minimum X size of the main window in pixels.
MIN_X_SZ = 340
#: Defines the main window border for various UI elements in pixels.
WIN_BORDER = 20

##==============================================================#
## SECTION: Class Definitions                                   #
##==============================================================#

class MainPanel(wx.Panel):
    """This class defines the main panel."""

    def __init__(self, parent, cases=[]):
        """This function defines initialization logic of the main panel."""
        wx.Panel.__init__(self, parent)

        # The parent is needed to make calls to close().
        self.parent = parent

        # Create the Sizers used for this panel.
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        name_sizer = wx.BoxSizer(wx.VERTICAL)
        ltxt_sizer = wx.BoxSizer(wx.VERTICAL)
        opts_sizer = wx.BoxSizer(wx.VERTICAL)
        oprv_sizer = wx.BoxSizer(wx.VERTICAL)
        bttn_sizer = wx.BoxSizer(wx.HORIZONTAL)

        # Create text input for the archive name.
        name_label = wx.StaticText(self, label="Archive Name:")
        self.name_text = wx.TextCtrl(self, size=(-1,-1), style=wx.TE_PROCESS_ENTER)
        cases = cases or [""]
        self.name_cbox = wx.ComboBox(self, value=cases[0], choices=cases, style=wx.CB_READONLY)
        name_sizer.Add(name_label)
        name_sizer.Add(self.name_text, flag=wx.EXPAND)
        name_sizer.Add(self.name_cbox, flag=wx.EXPAND)

        # Create text input for the archive log.
        log_label = wx.StaticText(self, label="Log Text:")
        style = wx.TE_MULTILINE | wx.TE_PROCESS_ENTER | wx.TE_RICH2
        self.log_text = wx.TextCtrl(self, size=(-1,-1), style=style)
        ltxt_sizer.Add(log_label)
        ltxt_sizer.Add(self.log_text, 1, wx.EXPAND)

        # Create option check boxes and add to sizer.
        self.no_ts_cb = wx.CheckBox(self, -1,
                "Do not include timestamp in archive name.")
        self.short_ts_cb = wx.CheckBox(self, -1,
                "Only timestamp to the day (hour:min otherwise).")
        self.flat_cb = wx.CheckBox(self, -1,
                "Flatten archive file structure.")
        self.flatld_cb = wx.CheckBox(self, -1,
                "Flatten leading directory.")
        self.del_cb = wx.CheckBox(self, -1,
                "Delete original files after archiving.")
        opts_sizer.Add(self.no_ts_cb)
        opts_sizer.Add(self.short_ts_cb)
        opts_sizer.Add(self.flat_cb)
        opts_sizer.Add(self.flatld_cb)
        opts_sizer.Add(self.del_cb)

        # Create output preview.
        odir_label = wx.StaticText(self, label="Output Directory:")
        self.odir_text = wx.TextCtrl(self, size=(-1,-1), style=wx.TE_PROCESS_ENTER)
        ofile_label = wx.StaticText(self, label="Output File Name:")
        self.ofile_text = wx.TextCtrl(self, size=(-1,-1), style=wx.TE_READONLY)
        oprv_sizer.Add(odir_label)
        oprv_sizer.Add(self.odir_text, flag=wx.EXPAND)
        oprv_sizer.Add(ofile_label)
        oprv_sizer.Add(self.ofile_text, flag=wx.EXPAND)

        # Create main control buttons and add to sizer.
        self.ok_button = wx.Button(self, wx.ID_OK)
        self.cancel_button = wx.Button(self, wx.ID_CANCEL)
        bttn_sizer.Add(self.ok_button, 1)
        bttn_sizer.AddSpacer(WIN_BORDER)
        bttn_sizer.Add(self.cancel_button, 1)

        # Add items to main sizer.
        sflags = wx.TOP | wx.LEFT | wx.RIGHT | wx.EXPAND
        main_sizer.Add(name_sizer, 0, sflags, WIN_BORDER)
        main_sizer.Add(ltxt_sizer, 5, sflags, WIN_BORDER)
        main_sizer.Add(opts_sizer, 0, sflags, WIN_BORDER)
        main_sizer.Add(oprv_sizer, 0, sflags, WIN_BORDER)
        main_sizer.Add(bttn_sizer, 1, sflags, WIN_BORDER)
        main_sizer.AddSpacer(WIN_BORDER)
        self.SetSizerAndFit(main_sizer)

        #: The dynamic X size of the main window based on UI elements.
        self.dyn_x_size = main_sizer.GetSize()[0]
        #: The dynamic Y size of the main window based on UI elements.
        self.dyn_y_size = main_sizer.GetSize()[1]

        # This sets initial focus to the log text input.
        self.log_text.SetFocus()

class MainWindow(wx.Frame):
    """The main window of the application."""

    def __init__(self, parent, title, cases=[]):
        """This function defines initialization logic of the main window."""
        self.parent = parent

        # This style disables the ability to resize the window.
        style = wx.DEFAULT_FRAME_STYLE | wx.WANTS_CHARS
        style &= ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX)
        wx.Frame.__init__(self,
                self.parent,
                title=title,
                style=style)
        self.mainpanel = MainPanel(self, cases)

        # Set window size based on dynamically calculated size.
        x = self.mainpanel.dyn_x_size
        if x < MIN_X_SZ:
            x = MIN_X_SZ
        self.SetSize((x, self.mainpanel.dyn_y_size))

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
    frame = MainWindow(None, "debug")
    frame.mainpanel.flatld_cb.Disable()
    frame.show()
    app.MainLoop()
