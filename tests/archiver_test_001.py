"""This script provides a unit test of the Archiver utility."""

##==============================================================#
## COPYRIGHT 2013, REVISED 2013, Jeff Rimko.                    #
##==============================================================#

import os
import time
import unittest
import zipfile

##==============================================================#
## SECTION: Class Definitions                                   #
##==============================================================#

class TestCases(unittest.TestCase):
    def testcase1(test):
        """Checks for basic archive creation."""
        ts = time.strftime("%Y%m%d%H%M")
        arcpath = ts + "-foo.zip"
        test.assertFalse(os.path.exists(arcpath))

        # Create archive.
        os.system("python ../app/archiver.py foo.txt")
        test.assertTrue(os.path.exists(arcpath))

        # Check contents of archive.
        arc = zipfile.ZipFile(arcpath)
        arclist = arc.namelist()
        test.assertTrue(1 == len(arclist))
        test.assertTrue("foo.txt" in arclist)

        # Cleanup.
        arc.close()
        os.remove(arcpath)

##==============================================================#
## SECTION: Main Body                                           #
##==============================================================#

if __name__ == '__main__':
    unittest.main()
