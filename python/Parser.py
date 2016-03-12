ASSIGNMENT_LEFT = "<-"
DOG = "dog"
CALL = "call"
END = "end"
BOX = "box"
SAY = "say"
RETURN = "return"
EXIT = "exit"
IF = "if"
ELSE = "else"
COMMA = ","
WHILE = "while"
PLUS = "+"
MINUS = "-"
DIVIDE = "/"
MOD = "%"
MULTIPLY = "*"
LEFT_PARAN = "("
RIGHT_PARAN = ")"
LT = "<"
GT = ">"
LE = "<="
GE = ">="
EQ = "="
NEQ = "!="
AND = "&&"
OR = "||"
NOT = "!"
PERIOD = "."
IDENTIFIER = "VAR"
NUMBER = "LITERAL"
STRING = "STRING"

import Lexer as lexer
from symbols import *
from Node import Node

class Parser:
  def __init__(self, sourceText):
    self.token = ""
    self.indent = 0
    self.lexer = lexer(sourceText)

  def error(self):
    print("PROBLEM")
    quit()

  def getToken(self):
    if self.token: 
      # print the current token, before we get the next one
      #print (" "*40 ) + token.show() 
      print(("  " * self.indent) + "   (" + token.show(align=False) + ")")
    # get next token
    return self.lexer.get()

  def found(self, token_type):
    if self.token.type == token_type:
      self.consume(token_type)
      return True
    return False

  def consume(self, token_type):
    if self.token.type == token_type:
      self.token = self.getToken()
    else:
      self.error()

  def expression(self):
    """
    (IDENTIFIER | NUMBER | expression) (+ | - | * | /) (IDENTIFIER | NUMBER | expression)
    IDENTIFIER
    NUMBER
    """
    # Expression can be either identif, nuber or express, then operator then again
    if self.found(IDENTIFIER):
      pass
    elif self.found(NUMBER):
      pass
    else:
      self.expression()


    if self.found(PLUS):
      pass
    elif self.found(MINUS):
      pass
    elif self.found(MULTIPLY):
      pass
    elif: self.found(DIVIDE):
      pass
    else:
      # Throw error if no operators found
      self.error()





  def condition(self):
    """
    (IDENTIFIER | expression) (< > <= >= =) (IDENTIFIER | expression)
    """

  def statement(self):
    """
    IDENTIFIER ASSIGNMENT_LEFT (IDENTIFIER | LITERAL | STRING)
    """"