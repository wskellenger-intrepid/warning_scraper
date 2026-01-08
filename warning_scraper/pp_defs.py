import pyparsing as pp

LBRACE,RBRACE,LBRACK,RBRACK,LT,GT,LPAREN,RPAREN,DQ,SEMI,COLON,COMMA = map(pp.Suppress,'{}[]<>()";:,')
NUMBERS = pp.Word(pp.nums)
DATETIME = pp.pyparsing_common.iso8601_datetime.copy()
ALPHADOT = pp.Word(pp.alphanums + "._-")
BRACKETED = pp.QuotedString(quoteChar="[", endQuoteChar="]")
PARENTHESISWRAPPED = pp.QuotedString(quoteChar="(", endQuoteChar=")")
DRIVEANDFILEPATH = pp.Combine(
    pp.oneOf(list(pp.alphas)) + (pp.Literal(':/') ^ pp.Literal(':\\'))+ 
    pp.Word(pp.alphanums + ' _()-./\\'))
RELATIVEFILEPATH = pp.Combine(
    pp.oneOf(".. . / \\") +
    pp.Word(pp.alphanums + ' _()-./\\'))
POSITIONINFO = (LPAREN + NUMBERS + pp.ZeroOrMore(COMMA + NUMBERS) + RPAREN + COLON)  #examples: (123):  (123,3):  (123,344):
GCCPOSITIONINFO = (COLON + NUMBERS + COLON + NUMBERS + COLON)  #examples:  :123:34:  :1:1:
CPPLINTPOSITIONINFO = (COLON + NUMBERS + COLON)  #examples:  :445:, :249:
CLANGWARNINGGROUP = pp.QuotedString(quoteChar="[-W", endQuoteChar="]")
