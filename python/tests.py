from Compiler import Compiler

def test_scanner(sourceFile):
  comp = Compiler(sourceFile)
  comp.driver()


test_scanner("test.lilo")
