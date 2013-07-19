class Character:

   def __init__(self, c, lineIndex, colIndex, sourceIndex, sourceText):
      self.cargo = c
      self.si = sourceIndex
      self.li = lineIndex
      self.ci = colIndex
      self.source = sourceText

   def __str__(self):
      cargo = self.cargo
      if cargo == " ":
         cargo = "   space"
      elif cargo == "\n":
         cargo = "   newline"
      elif cargo == "\t":
         cargo = "   tab"
      elif cargo == "\0":
         cargo = "   eof"

      return str(self.li).rjust(6) + str(self.ci).rjust(4) + "  " + cargo
