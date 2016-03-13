from LiloCompiler import LiloCompiler as Compiler
import sys

args = sys.argv
source_filename = args[1]
output_filename = args[2]

verbose = False
if len(args) > 3:
  verbose = args[3]

compiler = Compiler(source_filename, output_filename, verbose)
compiler.compile()