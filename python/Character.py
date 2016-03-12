# define the end of file
EOF = "\0"

class Character:
  def __init__(self, char, lineIndex, colIndex, sourceIndex, source):
    # We need to store line number, col number, char position, and whole source
    self.char = char
    self.lineIndex = lineIndex
    self.colIndex = colIndex
    self.sourceIndex = sourceIndex
    self.sourceText = source

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
            str(self.lineIndex).rjust(6)
          + str(self.colIndex).rjust(4)
          + "  "
          + char
          )