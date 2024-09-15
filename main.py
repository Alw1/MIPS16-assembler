from argparse import *
#from scanner import tokenize
from scanner import *

parser = ArgumentParser(description="Shitty MIPS Assembler")

parser.add_argument('source_file') 
parser.add_argument('-c', '--output', default = "output.bin", help = "Output file name") 
args = parser.parse_args()


if __name__ == "__main__":

    tokens = []

    with open(args.source_file, 'r') as f:
        source_file = f.readlines()

#    print(TokenType.token_regex())

        for i,line in enumerate(source_file):
            tokens.append(tokenize(line, i))

        # tokens = map(lambda line: tokenize(line), contents)
        # print(list(tokens))
    
        
