import unittest
from pathlib import Path
from warning_scraper.Gcc import GccLineParser
from warning_scraper.FileParser import FileParser

class TestGccLines(unittest.TestCase):
    def test_line1(self):
        line = r"/Projects/Export/vsbexport/../../../Core/Messages/helloworld.h:503:7: warning: 'foo' has a field 'foo::m_type' whose type uses the anonymous namespace [enabled by default]"
        parser = GccLineParser()
        parser.setLine(line)
        parser.parseLine()
        warning = parser.getWarningObject()
        self.assertEqual(warning.linenumber, 503)
        self.assertEqual(warning.colnumber, 7)
        self.assertEqual(warning.warningid, "enabled by default")
        self.assertEqual(warning.fullpath, Path(r"/Projects/Export/vsbexport/../../../Core/Messages/helloworld.h"))
        self.assertEqual(warning.warningmessage, "'foo' has a field 'foo::m_type' whose type uses the anonymous namespace")

    # test a line with a relative path and no warning ID in brackets at the end of the message
    # created with: #pragma GCC warning "This is a test warning for the warning scraper tool."
    def test_line_with_relative_path(self):        
        line = r"../../../components/poco-core/src/poco_main.c:527:21: warning: This is a test warning for the warning scraper tool."
        parser = GccLineParser()
        parser.setLine(line)
        parser.parseLine()
        warning = parser.getWarningObject()
        self.assertEqual(warning.linenumber, 527)
        self.assertEqual(warning.colnumber, 21)
        self.assertEqual(warning.warningid, "")
        self.assertEqual(warning.fullpath, Path(r"../../../components/poco-core/src/poco_main.c"))
        self.assertEqual(warning.warningmessage, "This is a test warning for the warning scraper tool.")
