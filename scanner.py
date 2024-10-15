from enum import Enum
from instructions import Opcodes, Registers
from re import compile, finditer

class TokenType(Enum):
    RPAREN = r'\)'
    LPAREN = r'\('
#   DIRECTIVE = rf'.({"|".join(directives)})'
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
        key, value pairs to be used in capture group of the compiled
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

    @classmethod
    def compile_regex(cls, instr):
        return compile("".join(f'(?P<{x}>{y})' for x,y in instr.value.items()))
    

class Token():
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        return f'{self.type} {self.value}'

def tokenize(line, line_num):
    tokens = []
    
    #print(InstructionFormat.compile_regex(InstructionFormat.ARITHLOG))
    
   # print(compile(InstructionFormat.ARITHLOG.value))
    for match in finditer((InstructionFormat.compile_regex(InstructionFormat.ARITHLOG)), line):
       print(match)

    for match in finditer((InstructionFormat.compile_regex(InstructionFormat.LOADSTORE)), line):
       print(match)
            
    for match in finditer((InstructionFormat.compile_regex(InstructionFormat.JUMP)), line):
       print(match)

    for match in finditer((InstructionFormat.compile_regex(InstructionFormat.BRANCH)), line):
       print(match)

    for match in finditer((InstructionFormat.compile_regex(InstructionFormat.LABEL)), line):
       print(match)

    for match in finditer((InstructionFormat.compile_regex(InstructionFormat.LOADIMM)), line):
       print(match)




    for match in finditer(TokenType.token_regex(), line): 
        for group in TokenType.token_regex().groupindex:
            if match.group(group) and group != "NONTOKEN":  # Filters comments, spaces, and newlines
                tok_val, tok_type = match.group(group), TokenType[group].name

                if tok_type == 'ERROR':
                    exit(f"[Scanner Error] Unexpected input {tok_val} on line {line_num}")

                tokens.append(Token(tok_type, tok_val))            

                #Debug print, enable with cli option later
                #print(f"[Token] {tok_type} {tok_val}")
                break
    return tokens
