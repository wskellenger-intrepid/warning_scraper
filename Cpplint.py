import pyparsing as pp
from pathlib import Path
from Warning import Warning, OfficialWarningDesc, Severity
from LineParser import LineParser
import pp_defs
from linecache import getline
from util import getpathfrom

all_warnings = {
}

#example
#Some/Path/filename.cpp:7728:  Almost always, snprintf is better than strcpy  [runtime/printf] [4]
class CpplintLineParser(LineParser):

    grammar = pp.SkipTo(pp_defs.CPPLINTPOSITIONINFO)("file") + pp_defs.CPPLINTPOSITIONINFO("pos") \
            + pp.White() \
            + pp.SkipTo(pp_defs.BRACKETED)("message") + pp_defs.BRACKETED("warningid") + pp_defs.BRACKETED("severity")

    def setGrammar(self, grammar):
        self.grammar = grammar

    def setLine(self, rawline):
        self.rawline = rawline

    def parseLine(self):
        try:
            self.matches = self.grammar.parseString(self.rawline)
        except:
            self.matches = None

    def getWarningObject(self):
        warningobj = None
        if (self.matches != None):
            warningobj = Warning()
            try:
                pos = self.matches["pos"]
                warningobj.linenumber = int(pos[0])
            except:
                print("Error: Parser failed to match on line: {0}".format(self.rawline))

            try:
                warningobj.warningid = self.matches["warningid"].strip()
            except:
                warningobj.warningid = ""
            
            try:
                warningobj.warningmessage = self.matches["message"].strip()
            except:
                warningobj.warningmessage = ""

            try:
                warningobj.fullpath = Path(self.matches["file"])
            except:
                warningobj.fullpath = ""

            try:
                warningobj.severity = Severity(int(self.matches["severity"]))
            except:
                warningobj.severity = Severity.info

        return warningobj

