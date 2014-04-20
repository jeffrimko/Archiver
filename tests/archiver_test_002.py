"""This script provides a unit test of the Archiver utility."""

##==============================================================#
## DEVELOPED 2013, REVISED 2013, Jeff Rimko.                    #
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
        """Checks for proper `--flatten` option behavior."""
        ts = time.strftime("%Y%m%d%H%M")
        arcpath = ts + "-foo.zip"
        test.assertFalse(os.path.exists(arcpath))

        # Create archive using option.
        os.system("python ../app/archiver.py --flatten foo.txt bar/baz.txt")
        test.assertTrue(os.path.exists(arcpath))

        # Check contents of archive.
        arc = zipfile.ZipFile(arcpath)
        arclist = arc.namelist()
        test.assertTrue(2 == len(arclist))
        test.assertTrue("foo.txt" in arclist)
        test.assertTrue("baz.txt" in arclist)

        # Cleanup.
        arc.close()
        os.remove(arcpath)

    def testcase2(test):
        """Checks for proper `--delete` option behavior."""
        ts = time.strftime("%Y%m%d%H%M")
        arcpath = ts + "-temp.zip"
        test.assertFalse(os.path.exists(arcpath))

        # Create temp file.
        with open("temp.txt", "w") as f:
            f.write("temp file here")

        # Create archive using option.
        os.system("python ../app/archiver.py --delete temp.txt")
        test.assertTrue(os.path.exists(arcpath))

        # Check contents of archive.
        arc = zipfile.ZipFile(arcpath)
        arclist = arc.namelist()
        test.assertTrue(1 == len(arclist))
        test.assertTrue("temp.txt" in arclist)

        # Check temp file is gone.
        test.assertFalse(os.path.exists("temp.txt"))

        # Cleanup.
        arc.close()
        os.remove(arcpath)

    def testcase3(test):
        """Checks for proper `--flatten` and `--delete` option behavior."""
        ts = time.strftime("%Y%m%d%H%M")
        arcpath = ts + "-temp1.zip"
        test.assertFalse(os.path.exists(arcpath))

        # Create temp files.
        with open("temp1.txt", "w") as f:
            f.write("temp file here")
        with open("bar/temp2.txt", "w") as f:
            f.write("temp file here")

        # Create archive using option.
        os.system("python ../app/archiver.py --flatten --delete temp1.txt bar/temp2.txt")
        test.assertTrue(os.path.exists(arcpath))

        # Check contents of archive.
        arc = zipfile.ZipFile(arcpath)
        arclist = arc.namelist()
        test.assertTrue(2 == len(arclist))
        test.assertTrue("temp1.txt" in arclist)
        test.assertTrue("temp2.txt" in arclist)

        # Check temp file is gone.
        test.assertFalse(os.path.exists("temp1.txt"))
        test.assertFalse(os.path.exists("bar/temp2.txt"))

        # Cleanup.
        arc.close()
        os.remove(arcpath)

    def testcase4(test):
        """Checks for proper `--flatten` and `--delete` option behavior."""
        ts = time.strftime("%Y%m%d%H%M")
        arcpath = ts + "-temp1.zip"
        test.assertFalse(os.path.exists(arcpath))

        # Create temp files.
        with open("temp1.txt", "w") as f:
            f.write("temp file here")
        with open("bar/temp1.txt", "w") as f:
            f.write("temp file here")

        # Create archive using option.
        os.system("python ../app/archiver.py --flatten --delete temp1.txt bar/temp1.txt")
        test.assertTrue(os.path.exists(arcpath))

        # Check contents of archive.
        arc = zipfile.ZipFile(arcpath)
        arclist = arc.namelist()
        test.assertTrue(1 == len(arclist))
        test.assertTrue("temp1.txt" in arclist)

        # Check temp file is gone.
        test.assertFalse(os.path.exists("temp1.txt"))

        # Check temp file not added exists.
        test.assertTrue(os.path.exists("bar/temp1.txt"))

        # Cleanup.
        arc.close()
        os.remove(arcpath)
        os.remove("bar/temp1.txt")

##==============================================================#
## SECTION: Main Body                                           #
##==============================================================#

if __name__ == '__main__':
    unittest.main()
