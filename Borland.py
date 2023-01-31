from re import A
import pyparsing as pp
from pathlib import Path
from Warning import Warning, OfficialWarningDesc, Severity
from LineParser import LineParser
from pp_defs import *
from linecache import getline
from util import getpathfrom

#warning, description, and severity (using gitlab severity levels: info, minor, major, critical, blocker)
all_warnings = {
    "W8000":OfficialWarningDesc("W8000",r"Ambiguous operators need parentheses", Severity.major),
    "W8001":OfficialWarningDesc("W8001",r"Superfluous & with function", Severity.major),
    "W8002":OfficialWarningDesc("W8002",r"Restarting compile using assembly", Severity.minor),
    "W8003":OfficialWarningDesc("W8003",r"Unknown assembler instruction", Severity.minor),
    "W8004":OfficialWarningDesc("W8004",r"'%s' is assigned a value that is never used", Severity.minor),
    "W8086":OfficialWarningDesc("W8086",r"Incorrect use of #pragma alias 'aliasName'='substituteName'", Severity.minor),
    "W8100":OfficialWarningDesc("W8100",r"'%s' attribute directive ignored", Severity.minor),
    "W8110":OfficialWarningDesc("W8110",r"Duplicate '%s' attribute directive ignored", Severity.minor),
    "W8134":OfficialWarningDesc("W8134",r"Cannot allocate arrays of Delphi style class '%s'", Severity.minor),
    "W8005":OfficialWarningDesc("W8005",r"Bit fields must be signed or unsigned int", Severity.minor),
    "W8006":OfficialWarningDesc("W8006",r"Initializing %s with %s", Severity.major),
    "W8007":OfficialWarningDesc("W8007",r"Hexadecimal value contains too many digits", Severity.major),
    "W8120":OfficialWarningDesc("W8120",r"Base class of dllexport class should also be dllexport", Severity.minor),
    "W8126":OfficialWarningDesc("W8126",r"Base class of exported class should have exported constructor", Severity.minor),
    "W8008":OfficialWarningDesc("W8008",r"Condition is always %s", Severity.minor),
    "W8009":OfficialWarningDesc("W8009",r"Constant is long", Severity.minor),
    "W8010":OfficialWarningDesc("W8010",r"Continuation character \ found in // comment", Severity.minor),
    "W8011":OfficialWarningDesc("W8011",r"Nonportable pointer comparison", Severity.minor),
    "W8012":OfficialWarningDesc("W8012",r"Comparing signed and unsigned values", Severity.minor),
    "W8093":OfficialWarningDesc("W8093",r"Incorrect use of #pragma codeseg [seg_name] ['seg_class'] [group]", Severity.minor),
    "W8108":OfficialWarningDesc("W8108",r"Constant in new expression requires an initializer", Severity.major),
    "W8013":OfficialWarningDesc("W8013",r"Possible use of '%s' before definition", Severity.major),
    "W8014":OfficialWarningDesc("W8014",r"Declaration ignored", Severity.minor),
    "W8015":OfficialWarningDesc("W8015",r"Declare '%s' prior to use in prototype", Severity.minor),
    "W8016":OfficialWarningDesc("W8016",r"Array size for 'delete' ignored", Severity.minor),
    "W8017":OfficialWarningDesc("W8017",r"Redefinition of '%s' is not identical", Severity.major),
    "W8106":OfficialWarningDesc("W8106",r"%s are deprecated", Severity.minor),
    "W8109":OfficialWarningDesc("W8109",r"Parameter '%s' is a dependent type", Severity.minor),
    "W8111":OfficialWarningDesc("W8111",r"Accessing deprecated entity '%s' %s", Severity.minor),
    "W8112":OfficialWarningDesc("W8112",r"Unresolved dependencies in expression", Severity.minor),
    "W8127":OfficialWarningDesc("W8127",r"Function defined with different linkage", Severity.minor),
    "W8128":OfficialWarningDesc("W8128",r"Can't import a function being defined", Severity.minor),
    "W8129":OfficialWarningDesc("W8129",r"Interface '%s' does not have a GUID", Severity.minor),
    "W8130":OfficialWarningDesc("W8130",r"Interface '%s' does not derive from IUnknown. (Interfaces should derive from IUnknown)", Severity.minor),
    "W8131":OfficialWarningDesc("W8131",r"Casting Delphi style class '%s' to an interface. Use 'System::interface_cast<%s>(cls)' instead", Severity.minor),
    "W8139":OfficialWarningDesc("W8139",r"Support for declspec '%s' not implemented.", Severity.minor),
    "W8018":OfficialWarningDesc("W8018",r"Assigning %s to %s", Severity.minor),
    "W8019":OfficialWarningDesc("W8019",r"Code has no effect", Severity.minor),
    "W8020":OfficialWarningDesc("W8020",r"'%s' is declared as both external and static", Severity.minor),
    "W8101":OfficialWarningDesc("W8101",r"Extern C linkage ignored", Severity.minor),
    "W8125":OfficialWarningDesc("W8125",r"dllexport overrides previous dllimport", Severity.minor),
    "W8021":OfficialWarningDesc("W8021",r"Handler for '%s' hidden by previous handler for '%s'", Severity.minor),
    "W8022":OfficialWarningDesc("W8022",r"'%s' hides virtual function '%s'", Severity.minor),
    "W8023":OfficialWarningDesc("W8023",r"Array variable '%s' is near", Severity.minor),
    "W8024":OfficialWarningDesc("W8024",r"Base class '%s' is also a base class of '%s'", Severity.minor),
    "W8025":OfficialWarningDesc("W8025",r"Ill-formed pragma", Severity.minor),
    "W8026":OfficialWarningDesc("W8026",r"Functions %s are not expanded inline", Severity.minor),
    "W8027":OfficialWarningDesc("W8027",r"Functions containing %s are not expanded inline", Severity.minor),
    "W8085":OfficialWarningDesc("W8085",r"Function '%s' redefined as non-inline", Severity.minor),
    "W8102":OfficialWarningDesc("W8102",r"Implicit conversion of '%s' to '%s'", Severity.major),
    "W8113":OfficialWarningDesc("W8113",r"Inline function was declared with 'extern template'", Severity.minor),
    "W8115":OfficialWarningDesc("W8115",r"Constant expression expected; statement ignored", Severity.minor),
    "W8118":OfficialWarningDesc("W8118",r"Inline member function in Package class", Severity.minor),
    "W8121":OfficialWarningDesc("W8121",r"Found invalid character from source code in the current text locale %s", Severity.major),
    "W8132":OfficialWarningDesc("W8132",r"Casting interface '%s' to Delphi style class. Use 'System::interface_cast<%s>(intf)' instead", Severity.minor),
    "W8136":OfficialWarningDesc("W8136",r"Initialization of TLS data is not supported on this platform.", Severity.minor),
    "W8028":OfficialWarningDesc("W8028",r"Temporary used to initialize '%s'", Severity.minor),
    "W8029":OfficialWarningDesc("W8029",r"Temporary used for parameter '%s'", Severity.minor),
    "W8030":OfficialWarningDesc("W8030",r"Temporary used for parameter '%s' in call to '%s'", Severity.minor),
    "W8031":OfficialWarningDesc("W8031",r"Temporary used for parameter %d", Severity.minor),
    "W8032":OfficialWarningDesc("W8032",r"Temporary used for parameter %d in call to '%s'", Severity.minor),
    "W8033":OfficialWarningDesc("W8033",r"Conversion to '%s' will fail for members of virtual base '%s'", Severity.major),
    "W8034":OfficialWarningDesc("W8034",r"Maximum precision used for member pointer type '%s'", Severity.minor),
    "W8035":OfficialWarningDesc("W8035",r"%s", Severity.major),
    "W8095":OfficialWarningDesc("W8095",r"Incorrect use of #pragma message( 'string' )", Severity.minor),
    "W8096":OfficialWarningDesc("W8096",r"Incorrect use of #pragma code_seg(['seg_name'[,'seg_class']])", Severity.minor),
    "W8098":OfficialWarningDesc("W8098",r"Multi-character character constant", Severity.minor),
    "W8104":OfficialWarningDesc("W8104",r"Local Static with constructor dangerous for multi-threaded apps", Severity.minor),
    "W8105":OfficialWarningDesc("W8105",r"%s member '%s' in class without constructors", Severity.minor),
    "W8119":OfficialWarningDesc("W8119",r"Alignment reduced to maximum of %d", Severity.minor),
    "W8122":OfficialWarningDesc("W8122",r"dllexport class member '%s' should be of exported type", Severity.minor),
    "W8036":OfficialWarningDesc("W8036",r"Non-ANSI keyword used: '%s'", Severity.minor),
    "W8037":OfficialWarningDesc("W8037",r"Non-const function %s called for const object", Severity.major),
    "W8038":OfficialWarningDesc("W8038",r"Constant member '%s' is not initialized", Severity.major),
    "W8039":OfficialWarningDesc("W8039",r"Constructor initializer list ignored", Severity.major),
    "W8040":OfficialWarningDesc("W8040",r"Function body ignored", Severity.major),
    "W8041":OfficialWarningDesc("W8041",r"Negating unsigned value", Severity.major),
    "W8042":OfficialWarningDesc("W8042",r"Initializer for object '%s' ignored", Severity.major),
    "W8043":OfficialWarningDesc("W8043",r"Macro definition ignored", Severity.minor),
    "W8044":OfficialWarningDesc("W8044",r"#undef directive ignored", Severity.minor),
    "W8045":OfficialWarningDesc("W8045",r"No declaration for function '%s'", Severity.major),
    "W8046":OfficialWarningDesc("W8046",r"Pragma option pop with no matching option push", Severity.minor),
    "W8047":OfficialWarningDesc("W8047",r"Declaration of static function '%s(...)' ignored", Severity.major),
    "W8048":OfficialWarningDesc("W8048",r"Use qualified name to access member type '%s'", Severity.minor),
    "W8049":OfficialWarningDesc("W8049",r"Use '> >' for nested templates instead of '>>'", Severity.major),
    "W8050":OfficialWarningDesc("W8050",r"No type OBJ file present; disabling external types option", Severity.minor),
    "W8051":OfficialWarningDesc("W8051",r"Non-volatile function %s called for volatile object", Severity.major),
    "W8083":OfficialWarningDesc("W8083",r"Pragma pack pop with no matching pack push", Severity.minor),
    "W8107":OfficialWarningDesc("W8107",r"Type name expected", Severity.major),
    "W8124":OfficialWarningDesc("W8124",r"Published method '%s' refers to an unpublishable parameter or return type", Severity.minor),
    "W8052":OfficialWarningDesc("W8052",r"Base initialization without a class name is now obsolete", Severity.minor),
    "W8053":OfficialWarningDesc("W8053",r"'%s' is obsolete", Severity.minor),
    "W8054":OfficialWarningDesc("W8054",r"Style of function definition is now obsolete", Severity.minor),
    "W8055":OfficialWarningDesc("W8055",r"Possible overflow in shift operation", Severity.major),
    "W8056":OfficialWarningDesc("W8056",r"Integer arithmetic overflow", Severity.major),
    "W8097":OfficialWarningDesc("W8097",r"Not all options can be restored at this time", Severity.minor),
    "W8057":OfficialWarningDesc("W8057",r"Parameter '%s' is never used", Severity.minor),
    "W8058":OfficialWarningDesc("W8058",r"Cannot create pre-compiled header: %s", Severity.minor),
    "W8059":OfficialWarningDesc("W8059",r"Structure packing size has changed", Severity.major),
    "W8060":OfficialWarningDesc("W8060",r"Possibly incorrect assignment", Severity.major),
    "W8061":OfficialWarningDesc("W8061",r"Initialization is only partially bracketed", Severity.minor),
    "W8062":OfficialWarningDesc("W8062",r"Previous options and warnings not restored", Severity.minor),
    "W8063":OfficialWarningDesc("W8063",r"Overloaded prefix 'operator %s' used as a postfix operator", Severity.minor),
    "W8064":OfficialWarningDesc("W8064",r"Call to function with no prototype", Severity.major),
    "W8065":OfficialWarningDesc("W8065",r"Call to function '%s' with no prototype", Severity.major),
    "W8084":OfficialWarningDesc("W8084",r"Suggest parentheses to clarify precedence", Severity.major),
    "W8094":OfficialWarningDesc("W8094",r"Incorrect use of #pragma comment( <type> [,'string'] )", Severity.minor),
    "W8099":OfficialWarningDesc("W8099",r"Static `main' is not treated as an entry point", Severity.minor),
    "W8103":OfficialWarningDesc("W8103",r"Path '%s' and filename '%s' exceed maximum size of %d", Severity.minor),
    "W8123":OfficialWarningDesc("W8123",r"Path '%s' not found - path ignored in option '%s'", Severity.minor),
    "W8135":OfficialWarningDesc("W8135",r"Unknown #pragma '%s' ignored", Severity.minor),
    "W8138":OfficialWarningDesc("W8138",r"pragma '%s' not supported on this platform.", Severity.minor),
    "W8066":OfficialWarningDesc("W8066",r"Unreachable code", Severity.minor),
    "W8067":OfficialWarningDesc("W8067",r"Both return and return with a value used", Severity.major),
    "W8068":OfficialWarningDesc("W8068",r"Constant out of range in comparison", Severity.major),
    "W8069":OfficialWarningDesc("W8069",r"Nonportable pointer conversion", Severity.minor),
    "W8070":OfficialWarningDesc("W8070",r"Function should return a value", Severity.major),
    "W8116":OfficialWarningDesc("W8116",r"Returning pointer to a local object", Severity.major),
    "W8071":OfficialWarningDesc("W8071",r"Conversion may lose significant digits", Severity.major),
    "W8072":OfficialWarningDesc("W8072",r"Suspicious pointer arithmetic", Severity.minor),
    "W8073":OfficialWarningDesc("W8073",r"Undefined structure '%s'", Severity.minor),
    "W8074":OfficialWarningDesc("W8074",r"Structure passed by value", Severity.minor),
    "W8075":OfficialWarningDesc("W8075",r"Suspicious pointer conversion", Severity.minor),
    "W8087":OfficialWarningDesc("W8087",r"'%s::operator==' must be publicly visible to be contained by a '%s'", Severity.minor),
    "W8089":OfficialWarningDesc("W8089",r"'%s::operator<' must be publicly visible to be contained by a '%s'", Severity.minor),
    "W8090":OfficialWarningDesc("W8090",r"'%s::operator<' must be publicly visible to be used with '%s'", Severity.minor),
    "W8091":OfficialWarningDesc("W8091",r"%s argument %s passed to '%s' is a %s iterator: %s iterator required", Severity.minor),
    "W8092":OfficialWarningDesc("W8092",r"%s argument %s passed to '%s' is not an iterator: %s iterator required", Severity.minor),
    "W8133":OfficialWarningDesc("W8133",r"Requested savemem exceeds amount available (%d)", Severity.minor),
    "W8076":OfficialWarningDesc("W8076",r"Template instance '%s' is already instantiated", Severity.minor),
    "W8077":OfficialWarningDesc("W8077",r"Explicitly specializing an explicitly specialized class member makes no sense", Severity.minor),
    "W8078":OfficialWarningDesc("W8078",r"Throw expression violates exception specification", Severity.major),
    "W8137":OfficialWarningDesc("W8137",r"Deprecated #import directive encountered. Please use the TLIBIMP utility instead.", Severity.minor),
    "W8079":OfficialWarningDesc("W8079",r"Mixing pointers to different 'char' types", Severity.minor),
    "W8080":OfficialWarningDesc("W8080",r"'%s' is declared but never used", Severity.minor),
    "W8114":OfficialWarningDesc("W8114",r"Character represented by universal-character-name '____' cannot be represented in the current ansi locale %s", Severity.minor),
    "W8081":OfficialWarningDesc("W8081",r"void functions may not return a value", Severity.major),
    "W8117":OfficialWarningDesc("W8117",r"NOT IN USE - DO NOT TRANSLATE", Severity.minor),
    "W8082":OfficialWarningDesc("W8082",r"Division by zero", Severity.critical)}

#example
#   ..\..\..\Core\Stuff/file.h(331,2): C++ warning W8104: Local Static with constructor dangerous for multi-threaded apps
#   c:\Whatever\Core\Stuff\file.h(331,2): C++ warning W8104: Local Static with constructor dangerous for multi-threaded apps
class BorlandLineParser(LineParser):
    grammar = pp.SkipTo(POSITIONINFO)("file") \
            + POSITIONINFO("pos") + pp.Literal("C++ warning") \
            + pp.Combine('W' + NUMBERS)("warningid") + COLON + pp.White() \
            + pp.restOfLine()("message")

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

    #given a warningID, get the severity
    def getWarningSeverityFromId(self, warningid):
        result = "ERROR: Warning {0} not found in vendor list".format(warningid)

        if warningid in all_warnings.keys():
            result = all_warnings[warningid].severity
        
        return result        