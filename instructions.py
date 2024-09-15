from enum import Enum

directives = [
    "data",
    "text",
    "bss",
    "word",
    "byte",
    "half",
    "space",
    "asciiz",
    "ascii",
    "align",
    "globl",
    "ent",
    "end",
    "extern",
    "equ",
    "org",
    "string",
    "float"
]

class Opcodes(Enum):
    ADD = 0x100000
    ADDU = 0x100001
    ADDI = 0x001000
    ADDIU = 0x001001
    AND = 0x100100
    ANDI = 0x001100
    DIV = 0x011010
    DIVU = 0x011011
    MULT = 0x011000
    MULTU = 0x011001
    NOR = 0x100111
    OR = 0X100101
    ORI = 0x001101
    SLL = 0x000000
    SLLV = 0x000100
    SRA = 0X000011
    SRAV = 0X000111
    SRL = 0X000010
    SRLV = 0X000110
    SUB = 0X100010
    SUBU = 0X100011
    XOR = 0X100110
    XORI = 0X001110
    LHI = 0X011001
    LLO = 0x011000
    SLT = 0x101010
    SLTU = 0x101001
    SLTI = 0x001010
    SLTIU = 0x001001
    BEQ = 0x000100
    BGTX = 0x000111
    BLEZ = 0x000110
    BNE = 0x000101
    J = 0x000010
    JAL = 0x000011
    JALR = 0x001001
    JR = 0x001000
    LB = 0x1000000
    LBU = 0x100100
    LH = 0x100001
    LHU = 0x100101
    LW = 0x100011
    SB = 0x101000
    SH = 0x101001
    SW = 0x101011
    MFHI = 0x100000
    MFLO = 0x10010
    MTHI = 0x10001
    MTLO = 0x10011
    TRAP = 0x11010

    @classmethod
    def names(cls):
        uppercase = [name for name in cls.__members__]
        lowercase = [name.lower() for name in cls.__members__]
        return uppercase + lowercase

class Registers(Enum):
    ZERO = "100000"
    AT = "100001"
    V0 = "001000"
    V1 = "001001"
    A0 = "100100"
    A1 = "001100"
    A2 = "011010"
    A3 = "011011"
    T0 = "011000"
    T1 = "011001" 
    T2 = "011001"
    T3 = "011001"
    T4 = "011001"
    T5 = "011001"
    T6 = "011001"
    T7 = "011001"
    S0 = "011001"
    S1 = "011001"
    S2 = "011001"
    S3 = "011001"
    S4 = "011001"
    S5 = "011001"
    S6 = "011001"
    S7 = "011001"
    T8 = "100111"
    T9 = "100101"
    K0 = "001101"
    K1 = "000000"
    GP = "000100"
    SP = "000011"
    FP = "000111"
    RA = "000010"

    @classmethod
    def names(cls):
        uppercase = [name for name in cls.__members__]
        lowercase = [name.lower() for name in cls.__members__]
        return uppercase + lowercase

    
