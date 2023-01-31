import unittest
from pathlib import Path
from Gcc import GccLineParser
from FileParser import FileParser

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

