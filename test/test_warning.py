import weakref
from Borland import BorlandLineParser
import unittest
from Warning import Warning
from pathlib import Path
from VisualStudio import VisualStudioLineParser
from Gcc import GccLineParser

class TestWarning(unittest.TestCase):
    def test_warning_hash(self):
        w1 = Warning()
        w2 = Warning()

        w1.linenumber = 110
        w1.fullpath = Path("fizzbuzz.c")
        w1.warningid = "some warning"
        w1.colnumber = 0
        w1.warningline = "if(false == true) {"
        w1.fileopened = True

        w2.linenumber = 110
        w2.fullpath = Path("fizzbuzz.c")
        w2.warningid = "some warning"
        w2.colnumber = 0
        w2.warningline = "if(false == true) {"
        w2.fileopened = True

        self.assertEqual(w1.md5(), w2.md5())
        w2.linenumber = 100
        w2.fileopened = False
        self.assertNotEqual(w1.md5(uselinenumber=True), w2.md5())

        #add column number to w2
        w2.colnumber = 1
        self.assertNotEqual(w1.md5(), w2.md5(usecolnumber=True))
        
        w1.linenumber = 110
        w1.fullpath = Path("fizzbuzz.c")
        w1.warningid = "some warning"
        w1.colnumber = 0
        w1.warningline = "if(false == true) {"
        w1.fileopened = True

        w2.linenumber = 110
        w2.fullpath = Path("fizzbuzz.c")
        w2.warningid = "some warning"
        w2.colnumber = 0
        w2.warningline = "if(something = nothing) {"
        w2.fileopened = True

        self.assertNotEqual(w1.md5(), w2.md5())
    