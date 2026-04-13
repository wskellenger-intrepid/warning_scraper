import unittest
from pathlib import Path
from warning_scraper.EmbarcaderoClangMsbuild import EmbarcaderoClangMsbuildLineParser
from warning_scraper.FileParser import FileParser

class TestEmbarcaderoClangMsbuildLines(unittest.TestCase):
    #relative path
    def test_line1(self):
        line = r"     1>..\..\src\foo.h(247,7): warning W6147: 'HasMACAddress' overrides a member function but is not marked 'override' [-Winconsistent-missing-override] [C:\builds\project\project.cbproj]"
        parser = EmbarcaderoClangMsbuildLineParser()
        parser.setLine(line)
        parser.parseLine()
        warning = parser.getWarningObject()
        self.assertEqual(warning.linenumber, 247)
        self.assertEqual(warning.colnumber, 7)
        self.assertEqual(warning.warningid, "inconsistent-missing-override")
        self.assertEqual(warning.fullpath, Path(r'..\..\src\foo.h'))

    def test_line2(self):
        line = r"     1>..\..\src\bar.cpp(99,26): warning W5841: using the result of an assignment as a condition without parentheses [-Wparentheses] [C:\builds\project\project.cbproj]"
        parser = EmbarcaderoClangMsbuildLineParser()
        parser.setLine(line)
        parser.parseLine()
        warning = parser.getWarningObject()
        self.assertEqual(warning.linenumber, 99)
        self.assertEqual(warning.colnumber, 26)
        self.assertEqual(warning.warningid, "parentheses")
        self.assertEqual(warning.warningmessage, "using the result of an assignment as a condition without parentheses")
        self.assertEqual(warning.fullpath, Path(r'..\..\src\bar.cpp'))

    def test_line3(self):
        line = r"     1>..\..\src\baz.cpp(186,10): warning W6205: enumeration values 'NM_STATE_BUS_SLEEP', 'NM_STATE_READY_SLEEP', and 'NM_STATE_SYNCHRONIZE' not handled in switch [-Wswitch] [C:\builds\project\project.cbproj]"
        parser = EmbarcaderoClangMsbuildLineParser()
        parser.setLine(line)
        parser.parseLine()
        warning = parser.getWarningObject()
        self.assertEqual(warning.linenumber, 186)
        self.assertEqual(warning.colnumber, 10)
        self.assertEqual(warning.warningid, "switch")
        self.assertEqual(warning.warningmessage, "enumeration values 'NM_STATE_BUS_SLEEP', 'NM_STATE_READY_SLEEP', and 'NM_STATE_SYNCHRONIZE' not handled in switch")
        self.assertEqual(warning.fullpath, Path(r'..\..\src\baz.cpp'))

    def test_line4_ignored(self):
        line = r"     1>..\..\include\qux.h(94,9): Hint warning H104: previous definition is here [C:\builds\project\project.cbproj]"
        parser = EmbarcaderoClangMsbuildLineParser()
        parser.setLine(line)
        parser.parseLine()
        warning = parser.getWarningObject()
        self.assertIsNone(warning)

