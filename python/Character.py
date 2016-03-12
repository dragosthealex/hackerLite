# define the end of file
EOF = "\0"

class Character:
  def __init__(self, char, line_no, col_no, char_pos, source):
    # We need to store line number, col number, char position, and whole source
    self.char = char
    self.line_no = line_no
    self.col_no = col_no
    self.char_pos = char_pos
    self.source = source

  # Display as string
  def __str__(self):
    char = self.char
    if char == " ":
      char = "   space"
    elif char == "\n":
      char = "   newline"
    elif char == "\t":
      char = "   tab"
    elif char == EOF:
      char = "   EOF"

    return (
            str(self.line_no).rjust(6)
          + str(self.col_no).rjust(4)
          + "  "
          + char
          )