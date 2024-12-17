from enum import Enum 
from instructions import Opcodes, Registers, Instruction, InstructionFormat, TokenType
from re import finditer

def instructionize(line, line_num):

    formats = [
        InstructionFormat.LABEL,
        InstructionFormat.ARITHLOG,
        InstructionFormat.ARITHLOGI,
        InstructionFormat.BRANCH,
        InstructionFormat.NOP,
        InstructionFormat.LOADIMM,
        InstructionFormat.LOADSTORE,
        InstructionFormat.JUMP
    ]

    # Scan for unexpected inputs
    for match in finditer(TokenType.token_regex(), line): 
       for group in TokenType.token_regex().groupindex:

           if match.group(group) and group == "COMMENT":  # Filters comments, spaces, and newlines
                return None
           
           if match.group(group) and group != "NONTOKEN":  # Filters comments, spaces, and newlines
               tok_val, tok_type = match.group(group), TokenType[group].name

               if tok_type == 'ERROR':
                   exit(f"[Scanner Error] Unexpected input {tok_val} on line {line_num+1}")

               #Debug print, enable with cli option later
               #print(f"[Token] {tok_type} {tok_val}")
               break


    # If input is valid, grab instruction
    label = None
    for format in formats:
        for match in finditer(InstructionFormat.compile_regex(format),line):
            if format == InstructionFormat.LABEL:
                label = match.group('label')[:-1]
                continue
           
#                print(match)
            return Instruction(format, match.groupdict(), label)



