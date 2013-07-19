from Scanner import Scanner

class LexerError(Exception): pass

class Token:

   def __init__(self, starter):
      self.components = starter.cargo
      self.char = starter
      self.type = None

   def show(self, showLineNumbers = False, **kwargs):

      align = kwargs.get("align", True)

      if align:
         tokenTypeLen = 12
         space = " "
      else:
         tokenTypeLen = 0
         space = ""

      if showLineNumbers:
         s = str(self.char.li).rjust(6) + str(self.char.ci).rjust(4) + "  "
      else:
         s = ""

      if self.type == self.components:
         s = s + "Symbol".ljust(tokenTypeLen, ".") + ":" + space + self.type
      elif self.type == "Whitespace":
         s = s + "Whitespace".ljust(tokenTypeLen, ".") + ":" + space + repr(self.char)
      else:
         s = s + self.type.ljust(tokenTypeLen, ".") + ":" + space + self.char

      return s

   def __str__(self):
      return "COMPONENTS: %s   TYPE: %s" % (self.components, self.type)
