import pyparsing as pp
from pathlib import Path
from .Warning import Warning, OfficialWarningDesc, Severity
from .LineParser import LineParser
from . import pp_defs
from linecache import getline
from .util import getpathfrom

#cpplint ends each message with a number from 1 to 5, how sure it is that this is a problem, not how bad the problem is,
#so the severity comes from the category: the ones listed here, else the group's (the part before the /), else minor
all_warnings = {
    "runtime/printf": OfficialWarningDesc("runtime/printf", r"a printf-family call that can overflow", Severity.major),
    "runtime/printf_format": OfficialWarningDesc("runtime/printf_format", r"a printf format that is not safe", Severity.major),
    "build/printf_format": OfficialWarningDesc("build/printf_format", r"a printf format that is not safe", Severity.major),
    "runtime/memset": OfficialWarningDesc("runtime/memset", r"memset with its arguments swapped", Severity.major),
    "runtime/arrays": OfficialWarningDesc("runtime/arrays", r"a variable-length array", Severity.major),
    "runtime/invalid_increment": OfficialWarningDesc("runtime/invalid_increment", r"an increment that does not do what it looks like", Severity.major),
    "runtime/threadsafe_fn": OfficialWarningDesc("runtime/threadsafe_fn", r"a function that is not thread safe", Severity.major),
    "runtime/init": OfficialWarningDesc("runtime/init", r"a member initialised with itself", Severity.major),
    "build/include_order": OfficialWarningDesc("build/include_order", r"includes in the wrong order", Severity.info),
    "build/include_alpha": OfficialWarningDesc("build/include_alpha", r"includes not in alphabetical order", Severity.info),
    "build/include_subdir": OfficialWarningDesc("build/include_subdir", r"an include without its directory", Severity.info),
    "runtime/indentation_namespace": OfficialWarningDesc("runtime/indentation_namespace", r"a namespace body is indented", Severity.info),
}
group_severity = {
    "runtime": Severity.minor,
    "build": Severity.minor,
    "readability": Severity.info,
    "whitespace": Severity.info,
    "legal": Severity.info,
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
                if warningobj.warningid in all_warnings:
                    warningobj.severity = all_warnings[warningobj.warningid].severity
                else:
                    warningobj.severity = group_severity.get(warningobj.warningid.split("/")[0], Severity.minor)
            except:
                warningobj.severity = Severity.info

        return warningobj

