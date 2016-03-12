import Scanner
from Token import *
from symbols import *

class Lexer:
  def __init__(self, sourceText):
    """
    """
    # Init the scanner
    self.scanner = Scanner(sourceText)
    # Read first char
    self.scanner.get()

  def get():
    # Construct and return the next token in sourceText

    #ignore any whitespace or comments
    while c1 in WHITESPACE_CHARS or c2 == "/*"