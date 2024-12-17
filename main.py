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

    prog = Program(instructions)

    print("-- Source --")
    print("".join(source_file))
    print("-- Machine Code --")


    with open(args.output, 'w') as f:
        for line in prog.generateBytecode():
            f.write(line + '\n')

    # So I can copy contents directly into instruction memory
    for i, line in enumerate(prog.generateBytecode()):        
        print(f'Memory({i}) <='  + f' {line}')
    

