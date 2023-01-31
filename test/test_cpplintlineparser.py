from multiprocessing.sharedctypes import Value
import unittest
from pathlib import Path
from Cpplint import CpplintLineParser
from FileParser import FileParser

class TestCpplintLines(unittest.TestCase):
    def test_line1(self):
        line = r"Core/test/cicstesttest32Bit.h:427:  Is this a non-const reference? If so, make const or use a pointer: testMessageFilter_32bit& stMsgFilter  [runtime/references] [2]"
        parser = CpplintLineParser()
        parser.setLine(line)
        parser.parseLine()
        warning = parser.getWarningObject()
        self.assertEqual(warning.linenumber, 427)
        self.assertEqual(warning.warningid, "runtime/references")
        self.assertEqual(warning.fullpath, Path(r"Core/test/cicstesttest32Bit.h"))
        self.assertEqual(warning.warningmessage, "Is this a non-const reference? If so, make const or use a pointer: testMessageFilter_32bit& stMsgFilter")
        self.assertEqual(warning.severity.value, 2)
