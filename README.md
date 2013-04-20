Archiver
========
Utility for archiving files. An archive consists of a zip file containing the archived files plus a log file.

Requirements
------------
This application was written in [Python](http://python.org/) and uses the [wxPython](http://wxpython.org/) GUI library. Python 2.6 is recommended although other 2.x versions may work. wxPython 2.8 is recommended.

Archive Log
-----------
Log comments are saved in an <code>\_\_archive\_info\_\_.txt</code> file located in the top-level of the archive. The log uses [Asciidoc](http://www.methods.co.nz/asciidoc/) formatting.

Timestamps
----------
Timestamps are appended to the beginning of the archive filename and separated by a hyphen. The default timestamp format is *YYYYMMDDhhmm*; the timezone used is Eastern Daylight Time and the hours and minutes are handled in 24-hour format.
