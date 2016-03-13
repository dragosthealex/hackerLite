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
NE = "!="
AND = "&&"
OR = "||"
NOT = "!"
PERIOD = "."
IDENTIFIER = "Variable"
NUMBER = "Number"
STRING = "String"

from Lexer import Lexer as lexer
from symbols import *
from Node import Node

class Parser:
  def __init__(self, sourceText):
    self.token = ""
    self.indent = 0
    self.lexer = lexer(sourceText)

  def error(self, token=None):
    token = self.token
    print("PROBLEM with following token: " + token.type + " at line " + str(token.lineIndex + 1) + ", col " + str(token.colIndex + 1))
    quit()

  def parse(self):
    self.token = self.getToken()
    self.program()
    print("Successful Parse")

  def getToken(self):
    if self.token: 
      # print the current token, before we get the next one
      #print (" "*40 ) + token.show() 
      print(("  " * self.indent) + "   (" + self.token.show(align=False) + ")")
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
      print("consume problem")
      self.error(self.token)

  def program(self):
    """
    program: statement (statement)* EOF
    """
    self.statement()
    while not self.found(EOF):
      self.block()

  def block(self):
    """
    block: DOG function | statement | IF if_cond | WHILE while_cond
    """
    if self.found(DOG):
      self.function()
    elif self.found(IF):
      self.if_cond()
    elif self.found(WHILE):
      self.while_cond()
    else:
      self.statement()

  def function(self):
    """
    function: IDENTIFIER "("IDENTIFIER (COMMA IDENTIFIER)* ")" (block)* END
    """
    if self.found(IDENTIFIER):
      pass
    else:
      print("dog problem: Missing dog name")
      self.error(self.token)
    if self.found(LEFT_PARAN):
      if self.found(IDENTIFIER):
        while self.found(COMMA):
          if self.found(IDENTIFIER):
            pass
          else:
            print("dog problem: Missing identifier after ','")
            self.error(self.token)
        if self.found(RIGHT_PARAN):
          pass
        else:
          print("dog problem: Missing ')'")
          self.error(self.token)
      else:
        if self.found(RIGHT_PARAN):
          pass
        else:
          print("dog problem: Missing ')'")
          self.error(self.token)
    else:
      print("dog problem: Missing '('")
      self.error(self.token)

    # end function when find "end"
    # if we find eof first, error
    while not self.found(END):
      if self.found(EOF):
        rint("dog problem: Unexpected end of file: Missing end statement")
        self.error(self.token)
      self.block()

  def function_call(self):
    if not self.found(IDENTIFIER):
      print("dog call problem: Missing dog name")
      self.error(self.token)

    if not self.found(LEFT_PARAN):
      print("dog call problem: Missing '('")
      self.error(self.token)

    self.expression()
    while self.found(COMMA):
      self.expression()

    if not self.found(RIGHT_PARAN):
      print("dog call problem: Missing ')'")
      self.error(self.token)

  def if_cond(self):
    """
    ifcond: condition block (ELSE block)? END
    """
    self.condition()
    while (not self.found(END)) and (not self.found(ELSE)):
      if self.found(EOF):
        print("If condition error: Unexpected end of file. Probably missing 'end'")
        self.error(self.token)
      self.block()
      if self.found(ELSE):
        while not self.found(END):
          self.block()
        break


  def while_cond(self):
    """
    ifcond: expression block END
    """
    self.expression()
    self.block()
    if self.found(END):
      pass
    else:
      print("while problem")
      self.error(self.token)

  def factor(self):
    """
    factor: STRING | IDENTIFIER | NUMBER | "(" expression ")"
    """
    if self.found(STRING):
      pass
    elif self.found(IDENTIFIER):
      pass
    elif self.found(NUMBER):
      pass
    elif self.found(LEFT_PARAN):
      # Error if string
      if self.about(STRING):
        print("factor problem")
        self.error(self.token)
      self.expression()
      if self.found(RIGHT_PARAN):
        pass
      else:
        print("factor problem")
        self.error(self.token)
    else:
      print("factor problem")
      self.error(self.token)

  def term(self):
    """
    term: factor ((MULTIPLY | DIVIDE) factor)*
    """
    self.factor()

    while self.found(MULTIPLY) or self.found(DIVIDE):
      if self.found(STRING):
        print("term problem")
        self.error(self.token)
      self.factor()


  def expression(self):
    """
    expression: (term ((PLUS | MINUS) term)*)
    """
    self.term()
    while self.found(PLUS) or self.found(MINUS):
      if self.found(STRING):
        print("expression problem")
        self.error(self.token)
      self.term()

  def condition(self):
    """
    condition: "(" condition ")" | (simpleCondition | "!" condition) (("&&" | "||") condition | "!" condition))*
    """
    if self.found(LEFT_PARAN):
      self.condition()
      if not self.found(RIGHT_PARAN):
        print("condition error: Missing ')'")
        self.error(self.token)
    elif self.found(NOT):
      self.condition()
    else:
      self.simpleCondition()
      while self.found(AND) or self.found(OR):
        self.condition()

  def simpleCondition(self):
    """
    condition: expression ("<" | ">" | "<=" | ">=" | "=" | "!=") expression
    """
    self.expression()
    if (self.found(GE) or self.found(LE) or self.found(LT) or self.found(GT)
      or self.found(EQ) or self.found(NE)):
      self.expression()
    else:
      print("condition error")
      self.error(self.token)

  def statement(self):
    """
    statement: (EXIT | CALL function_call | SAY expression | assignmentStatement) PERIOD
    """

    if self.found(EXIT):
      pass
    elif self.found(CALL):
      self.function_call()
    elif self.found(SAY):
      self.expression()
    else:
      self.assignmentStatement()

    if not self.found(PERIOD):
      print("statement problem: Missing '.'")
      self.error(self.token)

  def assignmentStatement(self):
    """
    assignmentStatement: BOX assignment (COMMA assignment)*
    """
    if self.found(BOX):
      pass
    else:
      print("BOX keyword missing")
      self.error(self.token)
    self.assignment()
    while self.found(COMMA):
      self.assignment()

  def assignment(self):
    """
    assignment: IDENTIFIER <- expression
    """
    if self.found(IDENTIFIER):
      if self.found(ASSIGNMENT_LEFT):
        self.expression()
      else:
        print("assignment sign '<-' missing")
        self.error(self.token)
    else:
      print("IDENTIFIER missing")
      self.error(self.token)
