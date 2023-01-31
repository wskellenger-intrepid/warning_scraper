import unittest
import util
from pathlib import Path

class TestUtilGetPathFrom(unittest.TestCase):
    def test_getpathfrom1(self):
        mypath = Path(r"c:\Users\Me\Projects\fizzbuzz\Core\CoreLib\corefile.h")
        out = util.getpathfrom(mypath, "fizzbuzz")
        self.assertEqual(out, Path(r"Core\CoreLib\corefile.h"))

    def test_getpathfrom2(self):
        mypath = Path(r"c:\Users\Me\Projects\fizzbuzz\Core\CoreLib\corefile.h")
        out = util.getpathfrom(mypath, "fizzbuzz", include=True)
        self.assertEqual(out, Path(r"fizzbuzz\Core\CoreLib\corefile.h"))

    def test_getpathfrom3(self):
        mypath = Path(r"c:\Users\Me\Projects\fizzbuzz\Core\CoreLib\corefile.h")
        out = util.getpathfrom(mypath, "fiddle", include=True)
        self.assertEqual(out, mypath)

    def test_getpathfrom4(self):
        mypath = Path(r"..\..\..\Core\CoreLib\corefile.h")
        out = util.getpathfrom(mypath, "fizzbuzz")
        self.assertEqual(out, Path(r"Core\CoreLib\corefile.h"))

    def test_getpathfrom5(self):
        mypath = Path(r"..\..\..\Core\CoreLib\Foo\..\corefile.h")
        out = util.getpathfrom(mypath, "fizzbuzz")
        self.assertEqual(out, Path(r"Core\CoreLib\Foo\..\corefile.h"))


class TestUtilCleanForJson(unittest.TestCase):

    def test_cleanforjson1(self):
        text = r"W8010:Continuation character \ found in // comment"
        out = util.cleanforjson(text)
        self.assertEqual(out, r"W8010:Continuation character \\ found in // comment")

    def test_cleanforjson2(self):
        text = r"Some special escapes \r\n found in // comment"
        out = util.cleanforjson(text)
        self.assertEqual(out, r"Some special escapes \\r\\n found in // comment")

    def test_cleanforjson3(self):
        text = "Incorrect use of #pragma comment( <type>" + " [," + '"string"' + "] )"
        out = util.cleanforjson(text)
        self.assertEqual(out, "Incorrect use of #pragma comment( <type> [,'string'] )",)
