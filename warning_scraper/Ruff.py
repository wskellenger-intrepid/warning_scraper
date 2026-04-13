import pyparsing as pp
from pathlib import Path
from .Warning import Warning
from .LineParser import LineParser
from . import pp_defs
from linecache import getline
from .util import getpathfrom

#TODO: IMPLEMENT


all_warnings = {
}

class RuffLineParser(LineParser):

    grammar = pp.SkipTo(pp_defs.RUFFPOSITIONINFO)("file") + pp_defs.RUFFPOSITIONINFO("pos") \
            + pp.Word(pp.alphas + pp.nums)("warningid") + pp.White() \
            + pp.SkipTo(pp.LineEnd(), include=True)("message")


    def setGrammar(self, grammar):
        self.grammar = grammar

    def setLine(self, rawline):
        self.rawline = rawline

    def parseLine(self):
        try:
            self.matches = self.grammar.parseString(self.rawline)
        except Exception:
            self.matches = None

    def getWarningObject(self):
        warningobj = None
        if (self.matches is not None):
            warningobj = Warning()
            try:
                pos = self.matches["pos"]
                warningobj.linenumber = int(pos[0])
                if len(self.matches["pos"]) == 2:
                    warningobj.colnumber = int(pos[1])
            except Exception:
                print("Error: Parser failed to match on line: {0}".format(self.rawline))

            try:
                warningobj.warningid = self.matches["warningid"].strip()
            except Exception:
                warningobj.warningid = ""
            
            try:
                warningobj.warningmessage = self.matches["message"].strip()
            except Exception:
                warningobj.warningmessage = ""

            try:
                warningobj.fullpath = Path(self.matches["file"])
            except Exception:
                warningobj.fullpath = ""

        return warningobj

