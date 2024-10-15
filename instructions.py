from enum import Enum

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


class Funct(Enum):
    """
    Specifies the function of R-Type Instructions.
    R-Types always have an opcode of 0.
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


class Registers(Enum):
    r0 = 0x0 
    r1 = 0x1
    r2 = 0x2
    r3 = 0x3 
    r4 = 0x4 
    r5 = 0x5 
    r6 = 0x6
    r7 = 0x7 

    @classmethod
    def names(cls):
        uppercase = [name for name in cls.__members__]
        lowercase = [name.lower() for name in cls.__members__]
        return uppercase + lowercase

    
