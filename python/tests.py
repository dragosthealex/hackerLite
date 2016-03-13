from LiloCompiler import LiloCompiler as Compiler
import os

def test_scanner(sourceFile, outFile):
  comp = Compiler(sourceFile, outFile, True)
  comp.scanner_driver()

def test_lexer(sourceFile, outFile):
  comp = Compiler(sourceFile, outFile, True)
  comp.lexer_driver()

def test_parser(sourceFile, outFile):
  comp = Compiler(sourceFile, outFile, True)
  comp.parser_driver()

if os.path.exists("out.py"):
  os.remove("out.py")
test_scanner("test.lilo", "out1.py")
test_lexer("test.lilo", "out1.py")
test_parser("test.lilo", "out1.py")

test_scanner("test_prime.lilo", "out2.py")
test_lexer("test_prime.lilo", "out2.py")
test_parser("test_prime.lilo", "out2.py")