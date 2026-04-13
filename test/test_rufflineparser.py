from multiprocessing.sharedctypes import Value
import unittest
from pathlib import Path
from warning_scraper.Ruff import RuffLineParser
from warning_scraper.FileParser import FileParser

class TestRuffLines(unittest.TestCase):
    def test_line1(self):
        line = r"testers\tester.py:5:1: F403 `from testers.support.bootloaderparameters import *` used; unable to detect undefined names"
        parser = RuffLineParser()
        parser.setLine(line)
        parser.parseLine()
        warning = parser.getWarningObject()
        self.assertEqual(warning.linenumber, 5)
        self.assertEqual(warning.colnumber, 1)
        self.assertEqual(warning.warningid, "F403")
        self.assertEqual(warning.fullpath, Path(r"testers\tester.py"))
        self.assertEqual(warning.warningmessage, "`from testers.support.bootloaderparameters import *` used; unable to detect undefined names")
        self.assertEqual(warning.severity, None)

    def test_line2(self):
        line = r"testers\tester.py:457:13: F841 [*] Local variable `NEORAD_CONFIG_DISABLE` is assigned to but never used"
        parser = RuffLineParser()
        parser.setLine(line)
        parser.parseLine()
        warning = parser.getWarningObject()
        self.assertEqual(warning.linenumber, 457)
        self.assertEqual(warning.colnumber, 13)
        self.assertEqual(warning.warningid, "F841")
        self.assertEqual(warning.fullpath, Path(r"testers\tester.py"))
        self.assertEqual(warning.warningmessage,
                         "[*] Local variable `NEORAD_CONFIG_DISABLE` is assigned to but never used")
        self.assertEqual(warning.severity, None)
