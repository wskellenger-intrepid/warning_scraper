import unittest
from pathlib import Path
from VisualStudio import VisualStudioLineParser
from FileParser import FileParser

class TestVisualStudioLines(unittest.TestCase):
    #relative path
    def test_line1(self):
        line = r"C:\GitLab-runner\builds\49a93415\0\root\foo\Projects\Export\bar\..\..\..\Core\StandardLibrary/helloworld.h(236): warning C4267: 'argument' : conversion from 'size_t' to 'int', possible loss of data [C:\GitLab-runner\builds\my.vcxproj]"
        parser = VisualStudioLineParser()
        parser.setLine(line)
        parser.parseLine()
        warning = parser.getWarningObject()
        self.assertEqual(warning.linenumber, 236)
        self.assertEqual(warning.colnumber, -1)
        self.assertEqual(warning.warningid, "C4267")
        self.assertEqual(warning.fullpath, Path(r"C:\GitLab-runner\builds\49a93415\0\root\foo\Projects\Export\bar\..\..\..\Core\StandardLibrary/helloworld.h"))
        self.assertEqual(warning.warningmessage, "'argument' : conversion from 'size_t' to 'int', possible loss of data")
        self.assertEqual(warning.severity.value, 2)

    #absolute path
    def test_line2(self):
        line = r"..\..\..\..\Core\Core\fizzbuzz.cpp(1152): warning C4018: '<' : signed/unsigned mismatch [C:\GitLab-runner\builds\0db49454\0\root\foo\my.vcxproj]"
        parser = VisualStudioLineParser()
        parser.setLine(line)
        parser.parseLine()
        warning = parser.getWarningObject()
        self.assertEqual(warning.linenumber, 1152)
        self.assertEqual(warning.colnumber, -1)
        self.assertEqual(warning.warningid, "C4018")
        self.assertEqual(warning.fullpath, Path(r"..\..\..\..\Core\Core\fizzbuzz.cpp"))
        self.assertEqual(warning.warningmessage, "'<' : signed/unsigned mismatch")
        self.assertEqual(warning.severity.value, 2)

 
