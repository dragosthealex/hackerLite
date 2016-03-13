from LiloCompiler import LiloCompiler as Compiler
import sys

args = sys.argv
source_filename = args[1]
output_filename = args[2]

compiler = Compiler(source_filename, output_filename)
compiler.compile()