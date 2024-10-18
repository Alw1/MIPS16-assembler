from enum import Enum
from re import compile
#from scanner import InstructionFormats

def toBinary(num, bit_size):
      return format(num, f':0{b}') 

class Instruction():
    def __init__(self, format, match, label = None):
        self.format = format
        self.match = match
        self.label = label  
        
    def __str__(self):
        if self.label is not None:
            return f'{self.label} {self.match}'
        else:
            return f'{self.match}'

    def generateBytecode(self, sym_table):
        instr_binary = "000000000000000"
        match self.format:
            case InstructionFormat.ARITHLOG:
                op = Opcodes.getVal(self.match['op'])
                funct = Funct.getVal(self.match['op'])
                rd = Registers.getVal(self.match['rd'][1:])
                rs = Registers.getVal(self.match['rs'][1:])
                rt = Registers.getVal(self.match['rt'][1:])

                instr_binary = f'{op:03b}{rs:03b}{rt:03b}{rd:03b}{funct:04b}'
            case InstructionFormat.ARITHLOGI:
                op = Opcodes.getVal(self.match['op'])
                rs = Registers.getVal(self.match['rs'][1:])
                rt = Registers.getVal(self.match['rt'][1:])
                imm = int(self.match['imm'])

                instr_binary = f'{op:03b}{rs:03b}{rt:03b}{imm:07b}'
            case InstructionFormat.LOADSTORE:
                op = Opcodes.getVal(self.match['op'])
                rs = Registers.getVal(self.match['rs'][1:])
                rt = Registers.getVal(self.match['rt'][1:])
                imm = int(self.match['imm'])

                instr_binary = f'{op:03b}{rs:03b}{rt:03b}{imm:07b}'
            case InstructionFormat.BRANCH:
                op = Opcodes.getVal(self.match['op'])
                rs = Registers.getVal(self.match['rs'][1:])
                rt = Registers.getVal(self.match['rt'][1:])
                label = self.match['label']

                try:
                    addr = sym_table[label]
                except KeyError:
                    exit(f'ERROR: Label "{label}" is not specified')

                instr_binary = f'{op:03b}{rs:03b}{rt:03b}{addr:07b}'
 
            case InstructionFormat.JUMP:
                op = Opcodes.getVal(self.match['op'])
                addr = self.match['addr']

                try:
                    addr = sym_table[addr]
                except KeyError:
                    exit(f'ERROR: Label "{addr}" is not specified')

                instr_binary = f'{op:03b}{addr:013b}'
                pass
            case InstructionFormat.NOP:
                instr_binary = '1110000000000000'
                pass
            case InstructionFormat.LOADIMM:
                pass
            case _:
                exit("Unexpected instruction format")

        return instr_binary 

class Program():
    def __init__(self, instructions):
        self.instructions = instructions
        self.sym_table = self.getSymTable()
 
    def getSymTable(self):
        sym_table = {}
        addr = 0
        for instruction in self.instructions:
            if instruction.label is not None:
                if instruction.label in sym_table:
                    exit(f"ERROR: Label '{instruction.label}' already defined")
                sym_table[instruction.label] = addr
            addr += 2

        return sym_table

    def generateBytecode(self):
        l = []
        for instr in self.instructions:
            l.append(instr.generateBytecode(self.sym_table))

        return l
                



class Opcodes(Enum):

    # R-Type
    ADD = 0x0
    SUB = 0x0
    ADC = 0x0
    SUBC = 0x0
    SLLV = 0x0
    SLRV = 0x0
    AND = 0x0
    OR = 0X0
    NAND = 0X0
    NOR = 0X0 
    SLT = 0X0

    # I-Type
    ADDI = 0x0
    LI = 0x1
    LW = 0X2
    SW = 0x3
    BEQ = 0X4
    BLT = 0X5

    # J-Type
    J = 0X6

    # Other
    NOP = 0X7

    @classmethod
    def names(cls):
        uppercase = [name for name in cls.__members__]
        lowercase = [name.lower() for name in cls.__members__]
        return uppercase + lowercase

    @classmethod
    def getVal(cls, name):
       name = name.upper()
       return Opcodes[name].value


class Funct(Enum):
    """
    Specifies the function of R-Type Instructions.
    R-Types always have an opcode of 0, funct decides their function
    """

    ADD = 0x0
    SUB = 0x1
    SLLV = 0x2
    SLRV = 0x3
    AND = 0x4
    OR = 0x5
    NAND = 0x6
    NOR = 0x7
    SLT = 0x8
    ADC = 0x9
    SUBC = 0xA

    @classmethod
    def getVal(cls, name):
       name = name.upper()
       return Funct[name].value

class Registers(Enum):
    R0 = 0x0 
    R1 = 0x1
    R2 = 0x2
    R3 = 0x3 
    R4 = 0x4 
    R5 = 0x5 
    R6 = 0x6
    R7 = 0x7 

    @classmethod
    def names(cls):
        uppercase = [name for name in cls.__members__]
        lowercase = [name.lower() for name in cls.__members__]
        return uppercase + lowercase
    
    @classmethod
    def getVal(cls, name):
       name = name.upper()
       return Registers[name].value

class TokenType(Enum):
    RPAREN = r'\)'
    LPAREN = r'\('
#    DIRECTIVE = rf'.({"|".join(directives)})'
    OPCODE =  rf'({"|".join(Opcodes.names())})'
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

    ARITHLOGI = {
        'op' : TokenType.OPCODE.value,
        'x1' : TokenType.SPACE.value,
        'rs' : TokenType.REGISTER.value,
        'x2' : f'{TokenType.SPACE.value}{TokenType.COMMA.value}{TokenType.SPACE.value}',
        'rt' : TokenType.REGISTER.value,
        'x3' : f'{TokenType.SPACE.value}{TokenType.COMMA.value}{TokenType.SPACE.value}',
        'imm' : TokenType.NUMBER.value,
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
        'x1' : TokenType.SPACE.value,
        'rs' : TokenType.REGISTER.value, 
        'x2' : f'{TokenType.SPACE.value}{TokenType.COMMA.value}{TokenType.SPACE.value}',
        'imm' : TokenType.NUMBER.value,
        'x3' : f'{TokenType.LPAREN.value}{TokenType.SPACE.value}',        
        'rt' : TokenType.REGISTER.value,
        'x4' : f'{TokenType.RPAREN.value}{TokenType.SPACE.value}',        
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
        'rs' : TokenType.REGISTER.value,
        'x2' : f'{TokenType.SPACE.value}{TokenType.COMMA.value}{TokenType.SPACE.value}',
        'rt' : TokenType.REGISTER.value,
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

   
