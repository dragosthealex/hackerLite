from Scanner import *

# TODO
class LexerError(Exception): pass

class Token:
  """
  A Token object is the kind of thing that the Lexer returns.
  It holds:
  - the text of the token (self.cargo)
  - the type of token that it is
  - the line number and column index where the token starts
  """
  def __init__(self, startChar):
    # remember the start char
    self.cargo = startChar.char
    # it has to know about position
    self.sourceText = startChar.sourceText
    self.lineIndex = startChar.lineIndex
    self.colIndex = startChar.colIndex
    # We will know what type of token it is after we finished processing
    self.type = None

  # return the token as string
  def show(self, showLineNumbers = False, **kwargs):
    # align or not
    align = kwargs.get("align", True)
    if align:
      tokenTypeLen = 12
      space = " "
    else:
      tokenTypeLen = 0
      space = ""
    # show the line numbers or not
    if showLineNumbers:
      s = str(self.lineIndex).rjust(6) + str(self.colIndex).rjust(4) + " "
    else:
      s = ""
    # if this token is the one that we have
    if self.type == self.cargo:
      s = s + "Symbol".ljust(tokenTypeLen, ".") + ":" + space + self.type
    elif self.type == "Whitespace":
      s = s + "Whitespace".ljust(tokenTypeLen, ".") + ":" + space + repr(self.cargo)
    else:
      s = s + self.type.ljust(tokenTypeLen, ".") + ":" + space + self.cargo

    return s

    
  def abort(self,msg):
    lines = self.sourceText.split("\n")
    sourceLine = lines[self.lineIndex]
    raise LexerError("\nIn line "      + str(self.lineIndex + 1)
           + " near column " + str(self.colIndex + 1) + ":\n\n"
           + sourceLine.replace("\t"," ") + "\n"
           + " "* self.colIndex
           + "^\n\n"
           + msg)