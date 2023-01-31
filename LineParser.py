import Warning
import pyparsing as pp

class LineParser(object):
    """This is an interface class for LineParsers"""

    def setGrammar(self, grammar):
        """set the grammar used to parse the line"""
        pass

    def setLine(self, line):
        """provide the raw warning line"""
        pass

    def parseLine(self):
        """will parse the warning line"""
        pass

    def getWarningObject(self) -> Warning:
        """get Warning object from the information parsed"""
        pass