import pyparsing as pp
from pathlib import Path
from .Warning import Warning, OfficialWarningDesc, Severity
from .LineParser import LineParser
from . import pp_defs
from linecache import getline
from .util import getpathfrom

all_warnings = {
#TODO: IMPLEMENT
# GCC warnings don't have an official severity level, so no point in mapping them. 
# The warning message contains the location, a message, and a warning ID in brackets at the end i.e. [-Wunused-variable].
}

#examples
#   /full/path/to/helloworld.h:230:7: warning: 'DiagnosticJobImpl' has a field 'DiagnosticJobImpl::m_eCANTxType' whose type uses the anonymous namespace [enabled by default]
# ../../../src/spectral/phasevoc.c:112:36: warning: passing argument 1 of 'new_aubio_window' discards 'const' qualifier from pointer target type [-Wdiscarded-qualifiers]

class GccLineParser(LineParser):

    grammar = pp.SkipTo(pp_defs.GCCPOSITIONINFO)("file") + pp_defs.GCCPOSITIONINFO("pos") \
            + pp.Literal("warning:") + pp.White() \
            + pp.restOfLine("fullmessage")

    def setGrammar(self, grammar):
        self.grammar = grammar

    def setLine(self, rawline):
        self.rawline = rawline

    def parseLine(self):
        try:
            self.matches = self.grammar.parse_string(self.rawline)
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

            # Parse warning ID and message from fullmessage
            try:
                fullmessage = self.matches["fullmessage"].strip()
            except:
                fullmessage = ""
            
            # Set defaults
            warningobj.warningid = ""
            warningobj.warningmessage = fullmessage
            
            # Try to extract bracketed warning ID at the end
            if fullmessage.endswith(']'):
                bracket_start = fullmessage.rfind('[')
                if bracket_start != -1:
                    warningobj.warningid = fullmessage[bracket_start+1:-1].strip()
                    warningobj.warningmessage = fullmessage[:bracket_start].strip()

            try:
                warningobj.fullpath = Path(self.matches["file"])
            except:
                warningobj.fullpath = ""

            # treat all warnings as minor, since GCC does not have an official mapping
            warningobj.severity = Severity.minor

        return warningobj

