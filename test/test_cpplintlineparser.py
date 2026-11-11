from multiprocessing.sharedctypes import Value
import unittest
from pathlib import Path
from warning_scraper.Cpplint import CpplintLineParser
from warning_scraper.FileParser import FileParser
from warning_scraper.Warning import Severity

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

    def severity_of(self, category, confidence):
        parser = CpplintLineParser()
        parser.setLine("Core/a.cpp:10:  Some message  [%s] [%d]" % (category, confidence))
        parser.parseLine()
        return parser.getWarningObject().severity

    #cpplint's [1-5] is how sure it is, so it does not set the severity
    def test_severity_comes_from_the_category(self):
        self.assertEqual(self.severity_of("runtime/printf", 2), Severity.major)
        self.assertEqual(self.severity_of("whitespace/ending_newline", 5), Severity.info)
        self.assertEqual(self.severity_of("readability/namespace", 5), Severity.info)
        self.assertEqual(self.severity_of("build/include", 4), Severity.minor)

    def test_a_category_not_listed_takes_its_groups_severity(self):
        self.assertEqual(self.severity_of("runtime/new_check", 5), Severity.minor)
        self.assertEqual(self.severity_of("whitespace/new_check", 5), Severity.info)
        self.assertEqual(self.severity_of("unheard_of/thing", 5), Severity.minor)
