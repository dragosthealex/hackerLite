from Character import *

class Scanner:
    """
    A Scanner object reads through the sourceText
    and returns one character at a time.
    """
    #-------------------------------------------------------------------
    #
    #-------------------------------------------------------------------
    def __init__(self, sourceTextArg):
        global sourceText, lastIndex, char_pos, line_no, col_no
        sourceText = sourceTextArg
        lastIndex    = len(sourceText) - 1
        char_pos  = -1
        line_no    =  0
        col_no     = -1

        self.ENDMARK = "\0"


    #-------------------------------------------------------------------
    #
    #-------------------------------------------------------------------
    def get(self):
        """
        Return the next character in sourceText.
        """
        global lastIndex, char_pos, line_no, col_no

        char_pos += 1    # increment the index in sourceText

        # maintain the line count
        if char_pos > 0:
            if sourceText[char_pos - 1] == "\n":
                #-------------------------------------------------------
                # The previous character in sourceText was a newline
                # character.  So... we're starting a new line.
                # Increment line_no and reset col_no.
                #-------------------------------------------------------
                line_no +=1
                col_no  = -1

        col_no += 1

        if char_pos > lastIndex:
            # We've read past the end of sourceText.
            # Return the ENDMARK character.
            char = Character(self.ENDMARK, line_no, col_no, char_pos,sourceText)
        else:
            c    = sourceText[char_pos]
            char = Character(c, line_no, col_no, char_pos, sourceText)

        return char

    def lookahead(offset=1):
        """
        Return a string (not a Character object) containing the character
        at position:
                sourceIndex + offset
        Note that we do NOT move our current position in the sourceText.
        That is,  we do NOT change the value of sourceIndex.
        """
        index = sourceIndex + offset

        if index > lastIndex:
            # We've read past the end of sourceText.
            # Return the ENDMARK character.
            return ENDMARK
        else:
            return sourceText[index]