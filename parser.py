
#   MIPS Grammar
#   program ::= line*
#   line ::= [label] instruction | directive | label
#   instruction ::= opcode operands+
#   directive ::= directiveType [operand]



class Parser():

    def __init__(self, token_stream):
        self.token_stream = token_stream

 
    def error():
        pass
    #Include Error printing func here
    # also maybe pass string in as well for better error prints


def parseLine(tok_stream):

    match tok_stream[0]:
        case LABEL:
            pass
        case DIRECTIVE:
            parseDirective(tok_stream[1:])
        case LABEL:
            pass

def parseInstruction(tok_stream):
    pass

def parseDirective(tok_stream):
    pass


