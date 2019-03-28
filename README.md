# ![Archiver](doc/logo/archiver.png)

## Introduction
Utility for archiving files. An archive consists of a zip file containing the archived files and directories plus an optional information log file named `__arc_info__.txt` (please note older versions used the file name `__archive_info__.txt`).

There are two variations of this application:

  - **Archiver** - CLI utility.
  - **gArchiver** - GUI utility.

## Status
The status of this project is **production/stable**. This project is suitable for use and new releases will maintain compatibility unless otherwise stated.

## Requirements
This application was written in Python. The CLI utility uses the Docopt library. The graphical utility uses the wxPython GUI library. To run the application from source, the following dependencies are required:

  - [Python](http://python.org/) 3.6
  - [wxPython](http://wxpython.org/) 4.0.1 (gArchiver only)
  - [Docopt](https://github.com/docopt/docopt) 0.6.2 (Archiver only)

## Installation
Windows binaries of the two utility variations are built using [PyInstaller](http://www.pyinstaller.org/) 3.x; the binaries should be standalone and do not require any additional dependencies.

  - To use the CLI Archiver utility, simply add the `archiver.exe` file to a location accessible on the PATH.
  - To use the GUI gArchiver utility, add a shortcut to `garchiver.exe` to the `shell:sendto` directory which will add the utility to the Windows Explorer "Send to" menu.

## Usage
For more information on how to use the CLI utility, run `archiver --help` in a command prompt. The simplest example usage is `archiver myfile.txt`.

To use the GUI utility once added to the "Send to" menu, select files/directories to be archived then open the context menu (right click) and select `Send to->gArchiver`. A demo of gArchiver in action is shown below:

![gArchiver Demo](doc/demos/garchiver_demo.gif)

Log comments are saved in the `__arc_info__.txt` file located in the top-level of the archive. The log uses [Asciidoc](http://asciidoc.org/) formatting.

Timestamps are appended to the beginning of the archive filename and separated by a hyphen. The default timestamp format is *YYYYMMDDhhmm*.

## Q&A
### Who is this project for?
Anyone that could use a method of quickly archiving files while adding some optional notes. Received a document via email? Create an archive and include the sender's information in the log!
