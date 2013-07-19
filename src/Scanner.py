from Character import Character

class Scanner:

   def __init__(self, source):
      self.source = source
      self.end = len(source) - 1
      self.si = -1
      self.li = 0
      self.ci = -1

   def get(self):
      self.si += 1

      if self.si > 0:
         if self.source[self.si -1] == "\n":
            self.li += 1
            self.ci = -1

      self.ci += 1

      if self.si > self.end:
         char = None
      else:
         char = Character(self.source[self.si], self.li, self.ci, self.si, self.source)

      return char

   def __str__(self):
      s = ""
      char = self.get()
      while char:
         s += char
         char = self.get()

      return s

   def lookahead(self, times):
      if self.si + times > self.end:
         return None
      else:
         return self.source[self.si + times]

if __name__ == "__main__":

   scan = Scanner("""
uno

dos

tres quatro cinco
\t seis""")

   print scan.scan()
