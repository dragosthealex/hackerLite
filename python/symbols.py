#----------------------------------------------------------
# a list of keywords
#----------------------------------------------------------
keywords = """
if
else
while
end
dog
call
say
return
exit
box
"""
keywords = keywords.split()

#----------------------------------------------------------
# a list of symbols that are one character long
#----------------------------------------------------------
singleCharSymbols = """
=
( )
< >
/ * + - %
! & , 
.  ;
"""
singleCharSymbols = singleCharSymbols.split()

#----------------------------------------------------------
# a list of symbols that are two characters long
#----------------------------------------------------------
twoCharSymbols = """
-> <-
<= >=
!= ++
** --
+= -=
|| &&
"""
twoCharSymbols = twoCharSymbols.split()

import string
#----------------------------------------------------------
# valid characters for start and middle/end of variables
#----------------------------------------------------------
VAR_START_CHARS = string.letters
VAR_CHARS = string.letters + string.digits + "_"
#----------------------------------------------------------
# valid characters for numbers (literals)
#----------------------------------------------------------
LITERAL_START_CHARS = string.digits
LITERAL_CHARS = string.digits + ","
#----------------------------------------------------------
# valid characters for strings (literals)
#----------------------------------------------------------
STRING_DELIMITERS = "'" +"'"
WHITESPACE_CHARS = " \t\n"
#----------------------------------------------------------
# types
#----------------------------------------------------------
STRING = "String"
VAR = "Variable"
LITERAL = "Number"
WHITESPACE = "Whitespace"
COMMENT = "Comment"
EOF = "Eof"