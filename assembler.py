from enum import Enum 
from instructions import Opcodes, Registers, Instruction
from re import compile, finditer, findall

class TokenType(Enum):
    RPAREN = r'\)'
    LPAREN = r'\('
#    DIRECTIVE = rf'.({"|".join(directives)})'
    OPCODE =  rf'({"|".join(Opcodes.names())})\s+'
    REGISTER = rf'\$({"|".join(Registers.names())})'
    NUMBER = r'(-)?(0x)?[0-9]+'
    LABEL = r'\w+:'
    LABEL_CALL = r'\w+'
    SPACE = r'\s*'
    NONTOKEN = r'(\n)|(\s+)|(#.*|;.*|@.*)'
    STRING = r'".*"'
    COMMA = r','
    ERROR = r'.*'
    
    @classmethod
    def token_regex(cls):
        return compile('|'.join([f'(?P<{token.name}>{token.value})' for token in cls]))


class InstructionFormat(Enum):
    """
        Define each instruction format as enum mapped to a dict.
        key value pairs will become the name and value of the capture groups of the 
        regex
    """

    LABEL = {
        'label' : TokenType.LABEL.value
    }

    ARITHLOG = {
        'op' : TokenType.OPCODE.value,
        'x1' : TokenType.SPACE.value,
        'rd' : TokenType.REGISTER.value,
        'x2' : f'{TokenType.SPACE.value}{TokenType.COMMA.value}{TokenType.SPACE.value}',
        'rs' : TokenType.REGISTER.value,
        'x3' : f'{TokenType.SPACE.value}{TokenType.COMMA.value}{TokenType.SPACE.value}',
        'rt' : TokenType.REGISTER.value,
        'x4' : TokenType.NONTOKEN.value
    }

    JUMP = {
        'op' : TokenType.OPCODE.value,
        'x1' : TokenType.SPACE.value,
        'addr' : TokenType.LABEL_CALL.value,
        'x2' : TokenType.NONTOKEN.value,
    }

    LOADSTORE = {
        'op' : TokenType.OPCODE.value,
        'rs' : TokenType.REGISTER.value, 
        'x2' : f'{TokenType.SPACE.value}{TokenType.COMMA.value}{TokenType.SPACE.value}',
        'imm' : TokenType.NUMBER.value,
        'x3' : TokenType.LPAREN.value,        
        'rt' : TokenType.REGISTER.value,
        'x4' : f'{TokenType.RPAREN.value}'
    }

    LOADIMM = {
        'op' : TokenType.OPCODE.value,
        'rs' : TokenType.REGISTER.value, 
        'x2' : f'{TokenType.SPACE.value}{TokenType.COMMA.value}{TokenType.SPACE.value}',
        'imm' : TokenType.NUMBER.value,
        'x3' : TokenType.NONTOKEN.value,
    }

    BRANCH ={
        'op' : TokenType.OPCODE.value,
        'x1' : TokenType.SPACE.value,
        'rd' : TokenType.REGISTER.value,
        'x2' : f'{TokenType.SPACE.value}{TokenType.COMMA.value}{TokenType.SPACE.value}',
        'rs' : TokenType.REGISTER.value,
        'x3' : f'{TokenType.SPACE.value}{TokenType.COMMA.value}{TokenType.SPACE.value}',
        'label' : TokenType.LABEL_CALL.value,
        'x4' : TokenType.NONTOKEN.value
    }

    NOP = {
        'op' : r'(NOP)',
        'x1' : TokenType.NONTOKEN.value
    }

    @classmethod
    def compile_regex(cls, instr):
        return compile("".join(f'(?P<{x}>{y})' for x,y in instr.value.items()))

    @classmethod
    def whole_regex(cls):
        return { str(name) : InstructionFormat.compile_regex(name) for name in cls.__members__}
        #return compile('|'.join([f'(?P<{format.name}>{InstructionFormat.compile_regex(format)})' for format in cls]))


def instructionize(line, line_num):

    """
        PC + 2 for 16-bit CPU
        Labels compile to binary for labeled instruction
    """

    formats = [
        InstructionFormat.LABEL,
        InstructionFormat.ARITHLOG,
        InstructionFormat.BRANCH,
        InstructionFormat.NOP,
        InstructionFormat.LOADIMM,
        InstructionFormat.LOADSTORE
    ]


    for match in finditer(TokenType.token_regex(), line): 
       for group in TokenType.token_regex().groupindex:
           if match.group(group) and group != "NONTOKEN":  # Filters comments, spaces, and newlines
               tok_val, tok_type = match.group(group), TokenType[group].name

               if tok_type == 'ERROR':
                   exit(f"[Scanner Error] Unexpected input {tok_val} on line {line_num}")

               #Debug print, enable with cli option later
               #print(f"[Token] {tok_type} {tok_val}")
               break

    for format in formats:
        for match in finditer(InstructionFormat.compile_regex(format),line):
            print(format, match)
            #return Instruction(format, match)


