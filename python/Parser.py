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
  def __init__(self, sourceText, outputFile, verbose=False):
    self.token = ""
    self.ast = ""
    self.indent = 0
    self.lexer = lexer(sourceText, verbose)
    self.out = outputFile
    self.verbose = verbose
    
    # Set of executing instructions
    self.executing = set()

  def error(self, token=None):
    token = self.token
    print("PROBLEM with following token: " + token.type + " at line " + str(token.lineIndex + 1) + ", col " + str(token.colIndex + 1))
    quit()

  def parse(self):
    self.token = self.getToken()
    self.program()
    if self.verbose:
      print("Successful Parse")

  def getToken(self):
    if self.token: 
      # print the current token, before we get the next one
      if self.verbose:
        print(("  " * self.indent) + "   (" + self.token.show(align=False) + ")")
    # get next token
    return self.lexer.get()

  def found(self, token_type, node=None):
    if self.token.type == token_type:
      self.consume(token_type, node)
      return True
    return False

  def consume(self, token_type, node=None):
    if self.token.type == token_type:
      if node:
        node.add(self.token)
      # Do the translating
      if token_type == DOG:
        # Write functions
        self.out.write('def ')
      elif token_type == AND:
        self.out.write('and ')
      elif token_type == OR:
        self.out.write('or ')
      elif token_type == CALL:
        pass
      elif token_type == BOX:
        pass
      elif token_type == ASSIGNMENT_LEFT:
        self.out.write('= ')
      elif token_type == EQ:
        self.out.write('== ')
      elif token_type == SAY:
        self.out.write('print ')
      elif token_type == PERIOD:
        self.out.write('\n')
      elif token_type == END:
        self.out.write('\n\n')
        self.indent -= 1
      elif token_type == EXIT:
        quit()
      elif token_type == COMMA: 
        if "assignment" in self.executing:
          self.out.write('\n')
        else:
          self.out.write(', ')
      else:
        # write directly the token
        self.out.write(str(self.token.cargo) + ' ')

      self.token = self.getToken()

    else:
      print("consume problem: wrong token")
      self.error(self.token)

  def program(self):
    """
    program: statement (statement)* EOF
    """
    self.executing.add("program")

    node = Node()
    self.statement(node)
    while not self.found(EOF, node):
      self.block(node)
    self.executing.remove("program")

  def block(self, node=None):
    """
    block: DOG function | statement | IF if_cond | WHILE while_cond
    """
    # print any indent
    self.out.write(self.indent*'  ')

    if self.found(DOG, node):
      self.function(node)
    elif self.found(IF, node):
      self.if_cond(node)
    elif self.found(WHILE, node):
      self.while_cond(node)
    else:
      self.statement(node)

  def function(self, node=None):
    """
    function: IDENTIFIER "("IDENTIFIER (COMMA IDENTIFIER)* ")" (block)* END
    """
    self.executing.add("function")

    if self.found(IDENTIFIER):
      # Define a function
      pass
    else:
      print("dog problem: Missing dog name")
      self.error(self.token)
    if self.found(LEFT_PARAN, node):
      if self.found(IDENTIFIER, node):
        while self.found(COMMA, node):
          if self.found(IDENTIFIER, node):
            pass
          else:
            print("dog problem: Missing identifier after ','")
            self.error(self.token)
        if self.found(RIGHT_PARAN, node):
          # Increase indent and add colon
          self.indent += 1
          self.out.write(':\n')
        else:
          print("dog problem: Missing ')'")
          self.error(self.token)
      else:
        if self.found(RIGHT_PARAN, node):
          # Increase indent and add colon
          self.indent += 1
          self.out.write(':\n')
        else:
          print("dog problem: Missing ')'")
          self.error(self.token)
    else:
      print("dog problem: Missing '('")
      self.error(self.token)

    # end function when find "end"
    # if we find eof first, error
    while not self.found(END, node):
      if self.found(EOF, node):
        print("dog problem: Unexpected end of file: Missing end statement")
        self.error(self.token)
      self.block()

    self.executing.remove("function")


  def function_call(self, node=None):
    self.executing.add("function_call")

    if not self.found(IDENTIFIER, node):
      print("dog call problem: Missing dog name")
      self.error(self.token)

    if not self.found(LEFT_PARAN, node):
      print("dog call problem: Missing '('")
      self.error(self.token)

    self.expression(node)
    while self.found(COMMA, node):
      self.expression(node)

    if not self.found(RIGHT_PARAN, node):
      print("dog call problem: Missing ')'")
      self.error(self.token)

    self.executing.remove("function_call")


  def if_cond(self, node=None):
    """
    ifcond: condition block (ELSE block)? END
    """
    self.executing.add("if_cond")

    self.condition()

    # print the colon and increase indent
    self.out.write(':\n')
    self.indent += 1

    while (not self.found(END, node)) and (not self.found(ELSE, node)):
      if self.found(EOF):
        print("If condition error: Unexpected end of file. Probably missing 'end'")
        self.error(self.token)
      self.block(node)
      if self.found(ELSE, node):
        while not self.found(END):
          if self.found(EOF):
            print("If condition error: Unexpected end of file. Probably missing 'end'")
            self.error(self.token)
          self.block(node)
        break

    self.executing.remove("if_cond")


  def while_cond(self, node=None):
    """
    ifcond: condition block END
    """
    self.executing.add("while_cond")

    self.condition(node)

    # print the colon and increase indent
    self.out.write(':\n')
    self.indent += 1

    while not self.found(END):
      if self.found(EOF):
        print("While condition error: Unexpected end of file. Probably missing 'end'")
        self.error(self.token)
      self.block(node)

    self.executing.remove("while_cond")


  def factor(self, node=None):
    """
    factor: STRING | IDENTIFIER | NUMBER | "(" expression ")"
    """
    if self.found(STRING, node):
      pass
    elif self.found(IDENTIFIER, node):
      pass
    elif self.found(NUMBER, node):
      pass
    elif self.found(LEFT_PARAN, node):
      # Error if string
      if self.about(STRING, node):
        print("factor problem: cannot perform arithmetics on strings")
        self.error(self.token)
      self.expression(node)
      if self.found(RIGHT_PARAN, node):
        pass
      else:
        print("factor problem: missing ')'")
        self.error(self.token)
    else:
      print("factor problem: wrong token")
      self.error(self.token)

  def term(self, node=None):
    """
    term: factor ((MULTIPLY | DIVIDE) factor)*
    """
    self.factor(node)

    while self.found(MULTIPLY, node) or self.found(DIVIDE, node):
      if self.found(STRING, node):
        print("term problem: cannot perform arithmetics on strings")
        self.error(self.token)
      self.factor(node)


  def expression(self, node=None):
    """
    expression: (term ((PLUS | MINUS) term)*)
    """
    self.term(node)
    while self.found(PLUS, node) or self.found(MINUS, node):
      if self.found(STRING, node):
        print("expression problem: cannot perform arithmetics on strings")
        self.error(self.token)
      self.term(node)

  def condition(self, node=None):
    """
    condition: "(" condition ")" | (simpleCondition | "!" condition) (("&&" | "||") condition | "!" condition))*
    """
    if self.found(LEFT_PARAN, node):
      self.condition(node)
      if not self.found(RIGHT_PARAN, node):
        print("condition error: Missing ')'")
        self.error(self.token)
    elif self.found(NOT, node):
      self.condition(node)
    else:
      self.simpleCondition(node)
      while self.found(AND, node) or self.found(OR, node):
        self.condition(node)

  def simpleCondition(self, node=None):
    """
    condition: expression ("<" | ">" | "<=" | ">=" | "=" | "!=") expression
    """
    self.expression(node)
    if (self.found(GE, node) or self.found(LE, node) or self.found(LT, node) or self.found(GT, node)
      or self.found(EQ, node) or self.found(NE, node)):
      self.expression(node)
    else:
      print("condition error: wrong token")
      self.error(self.token)

  def statement(self, node=None):
    """
    statement: (EXIT | CALL function_call | SAY expression | assignmentStatement) PERIOD
    """

    if self.found(EXIT, node):
      pass
    elif self.found(CALL, node):
      self.function_call(node)
    elif self.found(SAY, node):
      self.expression(node)
    else:
      self.assignmentStatement(node)

    if not self.found(PERIOD, node):
      print("statement problem: Missing '.'")
      self.error(self.token)

  def assignmentStatement(self, node=None):
    """
    assignmentStatement: BOX assignment (COMMA assignment)*
    """
    self.executing.add("assignment")

    if self.found(BOX, node):
      pass
    else:
      print("'box' keyword missing")
      self.error(self.token)
    self.assignment(node)
    while self.found(COMMA, node):
      self.assignment(node)

    self.executing.remove("assignment")


  def assignment(self, node=None):
    """
    assignment: IDENTIFIER <- expression
    """
    if self.found(IDENTIFIER, node):
      if self.found(ASSIGNMENT_LEFT, node):
        self.expression(node)
      else:
        print("assignment sign '<-' missing")
        self.error(self.token)
    else:
      print("identifier missing")
      self.error(self.token)
