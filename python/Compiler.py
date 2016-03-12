from Scanner import *

class Compiler:
  def __init__(self, sourceFile):
    self.sourceFile = sourceFile;
    self.sourceText = open(sourceFile, "r").read()
    self.scanner = Scanner(self.sourceText)

  def driver(self):
    character = self.scanner.get()
    while True:
      print(character)
      if character.char == self.scanner.ENDMARK: 
        break
      character = self.scanner.get()   # getnext