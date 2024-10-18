from argparse import *
from scanner import *
from instructions import *

parser = ArgumentParser(description="Shitty MIPS Assembler")

parser.add_argument('source_file') 
parser.add_argument('-o', '--output', default = "output.bin", help = "Output file name") 
args = parser.parse_args()


if __name__ == "__main__":

    with open(args.source_file, 'r') as f:
        source_file = f.readlines()


    instructions = []    
    for i,line in enumerate(source_file):
        l = instructionize(line,i)
        if l is not None:
            instructions.append(l)

#    for instr in instructions:
#        if instr is not None:
#            print(instr)

    prog = Program(instructions)
    print("\n".join(prog.generateBytecode()))


