Archiver
========
Utility for archiving files. An archive consists of a zip file containing the archived files plus a log file.

This application was written in Python and uses the wxPython GUI library. To run the application from source, the following dependencies are required:

  - [Python](http://python.org/) 2.7 (although other 2.x version may work)
  - [wxPython](http://wxpython.org/) 3.0.0.0
  - [Docopt](https://github.com/docopt/docopt) 0.6.2

Log comments are saved in an <code>\_\_archive\_info\_\_.txt</code> file located in the top-level of the archive. The log uses [Asciidoc](http://www.methods.co.nz/asciidoc/) formatting.

Timestamps are appended to the beginning of the archive filename and separated by a hyphen. The default timestamp format is *YYYYMMDDhhmm*.
