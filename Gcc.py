import pyparsing as pp
from pathlib import Path
from Warning import Warning
from LineParser import LineParser
import pp_defs
from linecache import getline
from util import getpathfrom

#TODO: IMPLEMENT


all_warnings = {
}

#example
#   /full/path/to/helloworld.h:230:7: warning: 'DiagnosticJobImpl' has a field 'DiagnosticJobImpl::m_eCANTxType' whose type uses the anonymous namespace [enabled by default]
class GccLineParser(LineParser):

    grammar = pp.SkipTo(pp_defs.GCCPOSITIONINFO)("file") + pp_defs.GCCPOSITIONINFO("pos") \
            + pp.Literal("warning:") + pp.White() \
            + pp.SkipTo(pp_defs.BRACKETED("warningid") + pp.LineEnd(), include=True)("message")

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
                if len(self.matches["pos"]) == 2:
                    warningobj.colnumber = int(pos[1])
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

        return warningobj

