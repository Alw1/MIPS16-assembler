from enum import Enum
from instructions import directives, Opcodes, Registers
from re import compile, finditer

class TokenType(Enum):
    LPAREN = r'\)'
    RPAREN = r'\('
    DIRECTIVE = rf'.({"|".join(directives)})'
    OPCODE =  rf'({"|".join(Opcodes.names())})\s+'
    REGISTER = rf'\$({"|".join(Registers.names())})'
    LABEL = r'\w+:'
    LABEL_CALL = r'\w+'
    NUMBER = r'(0x)?[0-9]+'
    NONTOKEN = r'(\n)|(\s+)|(#.*|;.*|@.*)'
    STRING = r'".*"'
    COMMA = r','
    ERROR = r'.*'
    
    @classmethod
    def token_regex(cls):
        return compile('|'.join([f'(?P<{token.name}>{token.value})' for token in cls]))

# Move to parser later
class Memory():
    address = 0x0 #Starting address of memory
    size = 0x8    #Size of memory chunk

    mem_arr = [] #(mem_name, addr)

    @classmethod
    def allocate(cls):
        cls.address += cls.size
        return cls.address 

class Token():
    def __init__(self, type, value):
        self.type = type
        self.value = value
        self.address = Memory.allocate()

def tokenize(line, line_num):
    tokens = []
    for match in finditer(TokenType.token_regex(), line): 
        for group in TokenType.token_regex().groupindex:
            if match.group(group) and group != "NONTOKEN":  # Filters comments and stuff
                tok_val = match.group(group)
                tok_type = TokenType[group].name

                if tok_type == 'ERROR':
                    exit(f"[Scanner Error] Unexpected input {tok_val} on line {line_num}")

                tokens.append(Token(tok_type, tok_val))            

                #Debug print, enable with cli option later
                print(f"[Token] {tok_type} {tok_val}")
                break

