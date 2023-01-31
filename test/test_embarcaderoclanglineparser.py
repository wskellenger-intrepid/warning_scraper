import unittest
from pathlib import Path
from EmbarcaderoClang import EmbarcaderoClangLineParser
from Warning import Severity
from FileParser import FileParser
import copy

class TestEmbarcaderoClangLines(unittest.TestCase):
    #relative path
    def test_line1(self):
        line = r"..\..\..\Core\test/testECU.h(357,8): C++ warning : 'dllimport' attribute only applies to variables, functions and classes [-Wignored-attributes]"
        parser = EmbarcaderoClangLineParser()
        parser.setLine(line)
        parser.parseLine()
        warning = parser.getWarningObject()
        self.assertEqual(warning.linenumber, 357)
        self.assertEqual(warning.colnumber, 8)
        self.assertEqual(warning.fullpath, Path(r"..\..\..\Core\test/testECU.h"))
        self.assertEqual(warning.warningmessage, "'dllimport' attribute only applies to variables, functions and classes")
        self.assertEqual(warning.warningid, "ignored-attributes")

    #absolute path
    def test_line2(self):
        line = r"        C:\GitLab-Runner\builds\ws9oib44\0\test\test\Core\FunctionBlocks\cicsspyFunctionBlock.cpp(3052,11): C++ warning : enumeration value 'eicsspyFBCollectTypeManualStop' not handled in switch"
        parser = EmbarcaderoClangLineParser()
        parser.setLine(line)
        parser.parseLine()
        warning = parser.getWarningObject()
        self.assertEqual(warning.linenumber, 3052)
        self.assertEqual(warning.colnumber, 11)
        self.assertEqual(warning.fullpath, Path(r"C:\GitLab-Runner\builds\ws9oib44\0\test\test\Core\FunctionBlocks\cicsspyFunctionBlock.cpp"))
        self.assertEqual(warning.warningmessage, "enumeration value 'eicsspyFBCollectTypeManualStop' not handled in switch")

    def test_line3(self):
        line = r"        ..\..\..\Core\test/testECU.h(357,8): C++ warning : 'dllimport' attribute only applies to variables, functions and classes [-Wignored-attributes]"
        parser = EmbarcaderoClangLineParser()
        parser.setLine(line)
        parser.parseLine()
        warning = parser.getWarningObject()
        self.assertEqual(warning.linenumber, 357)
        self.assertEqual(warning.colnumber, 8)
        self.assertEqual(warning.fullpath, Path(r"..\..\..\Core\test/testECU.h"))
        self.assertEqual(warning.warningmessage, "'dllimport' attribute only applies to variables, functions and classes")
        self.assertEqual(warning.warningid, "ignored-attributes")
        self.assertEqual(warning.severity, Severity.minor)

    def test_line4(self):
        line = r"        C:\GitLab-Runner\builds\ws9oib44\0\test\test\Core\Extensions\TCPIP\test_driver.cpp(319,1): C++ warning : overflow in expression; result is 0 with type 'int' [-Winteger-overflow]"
        parser = EmbarcaderoClangLineParser()
        parser.setLine(line)
        parser.parseLine()
        warning = parser.getWarningObject()
        self.assertEqual(warning.linenumber, 319)
        self.assertEqual(warning.colnumber, 1)
        self.assertEqual(warning.fullpath, Path(r"C:\GitLab-Runner\builds\ws9oib44\0\test\test\Core\Extensions\TCPIP\test_driver.cpp"))
        self.assertEqual(warning.warningmessage, "overflow in expression; result is 0 with type 'int'")
        self.assertEqual(warning.warningid, "integer-overflow")
        self.assertEqual(warning.severity, Severity.major)
