import Scanner
from Token import *
from symbols import *

class Lexer:
  def __init__(self, sourceText, verbose=False):
    """
    """
    # Init the scanner
    self.scanner = Scanner(sourceText, verbose)
    self.ENDMARK = self.scanner.ENDMARK
    # Read first char
    self.getChar()

    self.verbose = verbose

  def dq(self, s): 
    return '"%s"' %s

  def getChar(self):
    """
    get the next character
    """
    self.character = self.scanner.get()
    self.c1 = self.character.char
    #---------------------------------------------------------------
    # Every time we get a character from the scanner, we also  
    # lookahead to the next character and save the results in c2.
    # This makes it easy to lookahead 2 characters.
    #---------------------------------------------------------------
    self.c2 = self.c1 + self.scanner.lookahead(1)

  def get(self):
    # Construct and return the next token in sourceText

    #---------------------------------------------------------
    #                PROCESS WHITE SPACE / COMMENTS
    #---------------------------------------------------------
    #ignore any whitespace or comments
    # print self.character
    while self.c1 in WHITESPACE_CHARS or self.c2 == "/*":
      # process whitespace
      while self.c1 in WHITESPACE_CHARS:
        token = Token(self.character)
        token.type = WHITESPACE
        self.getChar() 

        while self.c1 in WHITESPACE_CHARS:
          token.cargo += self.c1
          self.getChar() 
                  
      # process comments
      while self.c2 == "/*":
        # we found comment start
        token = Token(self.character)
        token.type = COMMENT
        token.cargo = self.c2

        self.getChar() # read past the first  character of a 2-character token
        self.getChar() # read past the second character of a 2-character token

        while not (self.c2 == "*/"):
          if self.c1 == self.ENDMARK:
            token.abort("Found end of file before end of comment")
          token.cargo += self.c1
          self.getChar() 

        token.cargo += self.c2  # append the */ to the token cargo

        self.getChar() # read past the first  character of a 2-character token
        self.getChar() # read past the second character of a 2-character token
        
        # return token  # only if we want the lexer to return comments
    #---------------------------------------------------------
    #               END PROCESS WHITE SPACE / COMMENTS
    #---------------------------------------------------------

    # Create a new token. It will remember position and line info from character
    token = Token(self.character)
    # End of file
    if self.c1 == self.ENDMARK:
      token.type = EOF
      return token

    # A variable starts
    if self.c1 in VAR_START_CHARS:
      token.type = VAR
      # get the whole variable
      self.getChar()

      while self.c1 in VAR_CHARS:
        token.cargo += self.c1
        self.getChar()

      # We found a keyword
      if token.cargo in keywords:
        token.type = token.cargo

      return token

    # A literal starts
    if self.c1 in LITERAL_START_CHARS:
      token.type = LITERAL
      self.getChar()

      while self.c1 in LITERAL_CHARS:
        if self.c1 == ',' and self.c2 not in LITERAL_CHARS:
          break
        token.cargo += self.c1
        self.getChar()

      return token

    # A string starts
    if self.c1 in STRING_DELIMITERS:
      # remember the quoteChar (single or double quote)
      # so we can look for the same character to terminate the quote.
      quoteChar   = self.c1

      self.getChar() 

      while self.c1 != quoteChar:
        if self.c1 == self.ENDMARK:
          token.abort("Found end of file before end of string literal")

        token.cargo += self.c1  # append quoted character to text
        self.getChar()      

      token.cargo += self.c1      # append close quote to text
      self.getChar()          
      token.type = STRING
      return token

    # Two char symbols
    if self.c2 in twoCharSymbols:
        token.cargo = self.c2
        token.type  = token.cargo  # for symbols, the token type is same as the cargo
        self.getChar() # read past the first  character of a 2-character token
        self.getChar() # read past the second character of a 2-character token
        return token

    if self.c1 in singleCharSymbols:
        token.type  = token.cargo  # for symbols, the token type is same as the cargo
        self.getChar() # read past the symbol
        return token

    # Else we found a token we don't recognise, so abort
    token.abort("Symbol not recognised: " + self.dq(self.c1))