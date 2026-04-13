import pyparsing as pp
from pathlib import Path
from .Warning import Warning, OfficialWarningDesc, Severity
from .LineParser import LineParser
from .pp_defs import *
from linecache import getline
from .util import getpathfrom

#warning, description, and severity (using gitlab severity levels: info, minor, major, critical, blocker)
all_warnings = {
    }

#example
#     1>..\..\..\Core\Hardware/DevicePort.h(94,15): Hint warning H5413: overridden virtual function is here [C:\GitLab-Runner\builds\MQUm8zU1z\0\ics\Projects\project.cbproj]
class EmbarcaderoClangMsbuildLineParser(LineParser):

    grammar = pp.Optional(pp.Word(pp.nums) + pp.Literal(">")) + pp.SkipTo(POSITIONINFO)("file") + POSITIONINFO("pos") \
            + pp.Literal("warning") + pp.Suppress(pp.Combine(pp.one_of(['H', 'E', 'W']) + NUMBERS)) + COLON + pp.White() \
            + pp.SkipTo(pp.Literal("[-W"))("message") + CLANGWARNINGGROUP("warningid") \
            + pp.SkipTo(BRACKETED + pp.LineEnd(), include=True)("project")
        
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

                warningobj.warningid = self.matches["warningid"].strip()
                warningobj.warningmessage = self.matches["message"].strip()

                warningobj.fullpath = Path(self.matches["file"])
            except:
                print("Error: Parser failed to match on line: {0}".format(self.rawline))

            try:
                warningobj.severity = all_warnings[warningobj.warningid].severity
            except:
                warningobj.severity = Severity.info

        return warningobj

