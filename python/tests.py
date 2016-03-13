from Compiler import Compiler

def test_scanner(sourceFile):
  comp = Compiler(sourceFile)
  comp.scanner_driver()

def test_lexer(sourceFile):
  comp = Compiler(sourceFile)
  comp.lexer_driver()

def test_parser(sourceFile):
  comp = Compiler(sourceFile)
  comp.parser_driver()

test_scanner("test.lilo")
test_lexer("test.lilo")
test_parser("test.lilo")