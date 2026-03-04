import unittest
import json
import os
import tempfile
from pathlib import Path
from types import SimpleNamespace
from warning_scraper.Borland import BorlandLineParser
from warning_scraper.FileParser import FileParser
from warning_scraper.warning_scraper import writeReport
from warning_scraper import util
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
        self.assertEqual(warning.fullpath, Path(r"..\..\..\Core\Stuff/file.h"))
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
        
    def test_gitlab_json_output(self):
        # Parse a few real warning lines to get fully-populated Warning objects
        raw_lines = [
            r"          ..\..\.\Core\Stuff/file.h(331,2): C++ warning W8104: Local Static with constructor dangerous for multi-threaded apps",
            r"          C:\GitLab-runner\builds\0db49454\0\root\v3\UI\Embarcadero\unitFrmView.cpp(843,1): C++ warning W8004: 'iEndianType' is assigned a value that is never used",
            r"..\..\.\Core\Hardware/FTD3XX.h(93,9): C++ warning W8017: Redefinition of 'FT_OPEN_BY_SERIAL_NUMBER' is not identical",
        ]
        fp = FileParser("borland")
        for line in raw_lines:
            parser = BorlandLineParser()
            parser.setLine(line)
            parser.parseLine()
            w = parser.getWarningObject()
            fp.discoveredwarnings.add(w)

        # Write the gitlab_code_quality.jinja output to a temp file
        tmp = tempfile.NamedTemporaryFile(suffix=".json", delete=False)
        tmp.close()
        self.addCleanup(os.unlink, tmp.name)

        args = SimpleNamespace(format="gitlab_json", outputfile=Path(tmp.name), urlrelativeto=None)
        writeReport(args, fp)

        # Validate JSON is well-formed
        self.assertTrue(util.validate_json(Path(tmp.name)))

        with open(tmp.name, encoding="utf-8") as f:
            data = json.load(f)

        # Should have one entry per unique warning
        self.assertEqual(len(data), 3)

        # Spot-check the W8104 entry
        w8104 = next((e for e in data if e["check_name"] == "W8104"), None)
        self.assertIsNotNone(w8104)
        self.assertEqual(w8104["check_name"], "W8104")
        self.assertTrue(w8104["description"].startswith("W8104:"))
        self.assertEqual(w8104["severity"], "minor")
        self.assertEqual(w8104["location"]["lines"]["begin"], 331)
        self.assertIsInstance(w8104["fingerprint"], str)
        self.assertGreater(len(w8104["fingerprint"]), 0)

        # Spot-check check_name == warningid for all entries
        for entry in data:
            self.assertEqual(entry["check_name"], entry["description"].split(":")[0])