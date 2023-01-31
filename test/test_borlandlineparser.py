import unittest
from pathlib import Path
from Borland import BorlandLineParser
from FileParser import FileParser
import copy

class TestBorlandLines(unittest.TestCase):
    #relative path
    def test_line1(self):
        line = r"          ..\..\..\Core\Stuff/file.h(331,2): C++ warning W8104: Local Static with constructor dangerous for multi-threaded apps"
        parser = BorlandLineParser()
        parser.setLine(line)
        parser.parseLine()
        warning = parser.getWarningObject()
        self.assertEqual(warning.linenumber, 331)
        self.assertEqual(warning.colnumber, 2)
        self.assertEqual(warning.warningid, "W8104")
        self.assertEqual(warning.fullpath, Path(r"..\..\..\Core\Stuff\file.h"))
        self.assertEqual(warning.warningmessage, "Local Static with constructor dangerous for multi-threaded apps")
        self.assertEqual(warning.severity.value, 2)

    #absolute path
    def test_line2(self):
        line = r"          C:\GitLab-runner\builds\0db49454\0\root\v3\UI\Embarcadero\unitFrmView.cpp(843,1): C++ warning W8004: 'iEndianType' is assigned a value that is never used"
        parser = BorlandLineParser()
        parser.setLine(line)
        parser.parseLine()
        warning = parser.getWarningObject()
        self.assertEqual(warning.linenumber, 843)
        self.assertEqual(warning.colnumber, 1)
        self.assertEqual(warning.warningid, "W8004")
        self.assertEqual(warning.fullpath, Path(r"C:\GitLab-runner\builds\0db49454\0\root\v3\UI\Embarcadero\unitFrmView.cpp"))
        self.assertEqual(warning.warningmessage, "'iEndianType' is assigned a value that is never used")
        self.assertEqual(warning.severity.value, 2)

    #relative path
    def test_line3(self):
        line = r"          ..\..\..\Core\Messages/cicsFoo.h(353,2): C++ warning W8012: Comparing signed and unsigned values"
        parser = BorlandLineParser()
        parser.setLine(line)
        parser.parseLine()
        warning = parser.getWarningObject()
        self.assertEqual(warning.linenumber, 353)
        self.assertEqual(warning.colnumber, 2)
        self.assertEqual(warning.warningid, "W8012")
        self.assertEqual(warning.fullpath, Path(r"..\..\..\Core\Messages/cicsFoo.h"))
        self.assertEqual(warning.warningmessage, "Comparing signed and unsigned values")
        self.assertEqual(warning.severity.value, 2)

    #discovered location has only line number
    def test_line4(self):
        line = r"          ..\..\..\Core\StandardLibrary\helloworld.h(128): C++ warning W8012: Comparing signed and unsigned values"
        parser = BorlandLineParser()
        parser.setLine(line)
        parser.parseLine()
        warning = parser.getWarningObject()
        self.assertEqual(warning.linenumber, 128)
        self.assertEqual(warning.colnumber, -1)
        self.assertEqual(warning.warningid, "W8012")
        self.assertEqual(warning.fullpath, Path(r"..\..\..\Core\StandardLibrary\helloworld.h"))
        self.assertEqual(warning.warningmessage, "Comparing signed and unsigned values")
        self.assertEqual(warning.severity.value, 2)

    #file path has spaces
    def test_line5(self):
        line = r"C:\GitLab-runner\builds\0db49454\0\root\foo\Components\XE4\FastMM\CPP Builder Support\FastMM4BCB.cpp(1991,6): C++ warning W8111: Accessing deprecated entity '_fastcall GetMemoryManager(TMemoryManager &)'"
        parser = BorlandLineParser()
        parser.setLine(line)
        parser.parseLine()
        warning = parser.getWarningObject()
        self.assertEqual(warning.linenumber, 1991)
        self.assertEqual(warning.colnumber, 6)
        self.assertEqual(warning.warningid, "W8111")
        self.assertEqual(warning.fullpath, Path(r"C:\GitLab-runner\builds\0db49454\0\root\foo\Components\XE4\FastMM\CPP Builder Support\FastMM4BCB.cpp"))
        self.assertEqual(warning.warningmessage, "Accessing deprecated entity '_fastcall GetMemoryManager(TMemoryManager &)'")
        self.assertEqual(warning.severity.value, 2)

    #file path has parenthesis
    def test_line6(self):
        line = r"c:\program files (x86)\embarcadero\rad studio\11.0\include\windows\sdk\amvideo.h(370,1): C++ warning W8012: Comparing signed and unsigned values"
        parser = BorlandLineParser()
        parser.setLine(line)
        parser.parseLine()
        warning = parser.getWarningObject()
        self.assertEqual(warning.linenumber, 370)
        self.assertEqual(warning.colnumber, 1)
        self.assertEqual(warning.warningid, "W8012")
        self.assertEqual(warning.fullpath, Path(r"c:\program files (x86)\embarcadero\rad studio\11.0\include\windows\sdk\amvideo.h"))
        self.assertEqual(warning.warningmessage, "Comparing signed and unsigned values")
        self.assertEqual(warning.severity.value, 2)

    def test_line7(self):
        line = r'          C:\GitLab-runner\builds\0db49454\0\test\test\Core\Hardware\cicsspyTestDialog.cpp(56,9): C++ warning W8094: Incorrect use of #pragma comment( <type> [,"string"] )'
        parser = BorlandLineParser()
        parser.setLine(line)
        parser.parseLine()
        warning = parser.getWarningObject()
        self.assertEqual(warning.linenumber, 56)
        self.assertEqual(warning.colnumber, 9)
        self.assertEqual(warning.warningid, "W8094")
        self.assertEqual(warning.fullpath, Path(r"C:\GitLab-runner\builds\0db49454\0\test\test\Core\Hardware\cicsspyTestDialog.cpp"))
        self.assertEqual(warning.warningmessage, 'Incorrect use of #pragma comment( <type> [,"string"] )')        
        self.assertEqual(warning.severity.value, 2)

    def test_line8(self):
        line = r"..\..\..\Core\Hardware/FTD3XX.h(93,9): C++ warning W8017: Redefinition of 'FT_OPEN_BY_SERIAL_NUMBER' is not identical"
        parser = BorlandLineParser()
        parser.setLine(line)
        parser.parseLine()
        warning = parser.getWarningObject()
        self.assertEqual(warning.linenumber, 93)
        self.assertEqual(warning.colnumber, 9)
        self.assertEqual(warning.warningid, "W8017")
        self.assertEqual(warning.fullpath, Path(r"..\..\..\Core\Hardware/FTD3XX.h"))
        self.assertEqual(warning.warningmessage, "Redefinition of 'FT_OPEN_BY_SERIAL_NUMBER' is not identical")
        self.assertEqual(warning.severity.value, 3)
