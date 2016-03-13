from Lexer import *
from Scanner import *
from symbols import *
from Parser import *
import os

class LiloCompiler:
  def __init__(self, sourceFileName, outputFileName, verbose=False):
    self.sourceFileName = sourceFileName;
    f = open(sourceFileName, "r")
    self.sourceText = f.read()
    f.close()
    
    if os.path.exists(outputFileName):
      os.remove(outputFileName)

    self.outputFile = open(outputFileName, "a")
    self.scanner = Scanner(self.sourceText, verbose)
    self.lexer = Lexer(self.sourceText, verbose)
    self.parser = Parser(self.sourceText, self.outputFile, verbose)
    self.verbose = verbose

  def scanner_driver(self):
    character = self.scanner.get()
    while True:
      if self.verbose:
        print(character)
      if character.char == self.scanner.ENDMARK: 
        break
      character = self.scanner.get()   # getnext

  def lexer_driver(self):
    if self.verbose:
      print("Here are the tokens returned by the lexer:")
    while True:
      token = self.lexer.get()
      if self.verbose:
        print(token.show(True))
      if token.type == EOF: 
        break

  def parser_driver(self):
    if self.verbose:
      print("There's the parser:")
    self.parser.parse()

  def compile(self):
    self.parser.parse()