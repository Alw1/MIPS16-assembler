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
    ADD = 0x000000
    ADDI = 0x000001
    ADDIU = 0x000010
    LI = 0x0
    LW = 0x0

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

    