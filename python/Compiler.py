from Lexer import *
from Scanner import *
from symbols import *
from Parser import *

class Compiler:
  def __init__(self, sourceFile):
    self.sourceFile = sourceFile;
    f = open(sourceFile, "r")
    self.sourceText = f.read()
    f.close()

    self.scanner = Scanner(self.sourceText)
    self.lexer = Lexer(self.sourceText)
    self.parser = Parser(self.sourceText)

  def scanner_driver(self):
    character = self.scanner.get()
    while True:
      print(character)
      if character.char == self.scanner.ENDMARK: 
        break
      character = self.scanner.get()   # getnext

  def lexer_driver(self):
    print("Here are the tokens returned by the lexer:")
    while True:
      token = self.lexer.get()
      print(token.show(True))
      if token.type == EOF: 
        break

  def parser_driver(self):
    print("There's the parser:")
    self.parser.parse()