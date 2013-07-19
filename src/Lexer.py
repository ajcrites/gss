from Scanner import Scanner
from Token import Token

WHITESPACE = "whitespace"
COMMENT = "comment"
EOF = "End-of-file"
NAME = "name"
VARIABLE = "var"
VALUE = "val"
FUNCTION = "function"
ARGUMENT = "arg"
SELECTOR = "selector"
INDENT = "indent"
DEDENT = "dedent"

SPACE = " "
INDENTATION = " \t"
SPACING = " \n\t\r"
DECLARATION = "{"
END_DECLARATION = "}"


class Lexer:

   def __init__(self, scanner):
      self.scanner = scanner
      self.indentStack = [0]
      self.tokens = []
      self.context = 'global'
      self.lastcontext = None

      self.__debug("Initializing Lexer")

   def getToken(self):

      character, c1, c2 = self.next()

      self.__debug("%s token acquired" % c1)

      if character == None:
         return EOF

      """Let's get comments out of the way first
      Indentation doesn't care about them"""
      if c1 + c2 == "//":

         self.__debug("Comment token")

         token = Token(character)
         token.type = SHORTCOMMENT
         token.components += "/"

         #Pass the second slash
         self.next()

         character, c1, c2 = self.next()

         #Double slash comments last till the end of the line
         while c1 != "\n":
            self.__debug("Seeking to end of line")
            token.components += c1
            character, c1, c2 = self.next()

         self.__debug("Returning comment token")

         return token

      #Long comment type
      if c1 + c2 == "/*":

         self.__debug("Long comment token")

         token = Token(character)
         token.type = LONGCOMMENT
         token.components += "*"

         while c1 + c2 != "*/":
            self.__debug("Seeking to end of long comment")
            character, c1, c2 = self.next()
            token.components += c1

         token.components += "/"

         #Pass the ending slash
         self.next()

         self.__debug("Returning long comment token")

         return token

      indentAmount = 0

      #Space and Tab count equally for indentation
      #Don't care to be helpful to people who mix the styles
      if self.context == 'global' and c1 in INDENTATION:
         indentAmount += 1

         token = Token(character)
         token.type = INDENT

         self.__debug("Indentation token")

         while c2 in INDENTATION:

            self.__debug("Gathering all indentation")

            character, c1, c2 = self.next()
            #Keep adding spaces for consistency in printout
            token.components += ' '

         #Ignore indentation ending in a newline
         if c2 == "\n":
            return None

         last = self.indentStack.pop()

         self.__debug("Comparing current indentation amount to last")

         #This is a new, higher level of indentation
         if indentAmount > last:
            self.indentStack.append(last)
            self.indentStack.append(indentAmount)
         #Same indentation level; no token added
         elif indentAmount == last:
            self.indentStack.append(last)
            self.__debug("Indentation level matches")
            return None
         #This is actually a dedent; keep dedenting until the appropriate level is found
         else:
            self.__debug("Starting Dedenting")
            while indentAmount < last:
               self.__debug("Dedenting")
               tok = Token(character)
               tok.type = DEDENT
               tokens.append(tok)
               last = self.indentStack.pop()

               if indentAmount == last:
                  self.indentStack.append(last)
                  return None
               elif len(self.indentStack) == 0:
                  print "Previous indentation amount not found!"

         return Token

      if self.context == 'global' and c1 == DECLARATION:

         self.__debug("Name or variable declaration")

         if c2 == ":":
            self.__debug("Name declaration")
            #skip the { and colon
            self.next()
            character, c1, c2 = self.next()
            token = Token(character)
            token.type = NAME

            character, c1, c2 = self.next()

            while c1 != END_DECLARATION:
               token.components += c1

               self.__debug("Seeking declaration end")

               if c1 in SPACING:
                  print "name declaration contains invalid character"
                  return None

               character, c1, c2 = self.next()


            #Skip }
            self.next()

            #Clear trailing whitespace
            while c2 in INDENTATION:
               self.__debug("Clearing trailing whitespace")
               character, c1, c2 = self.next()

            if c1 != "\n":
               print "name declarations must end with a newline"

               while c1 != "\n":
                  self.__debug("Recovering bad name declaration")
                  character, c1, c2 = self.next()

            return token

         else:
            self.__debug("Variable declaration")
            #Skip the brace
            character, c1, c2 = self.next()
            token = Token(character)
            token.type = VARIABLE

            while c1 != SPACE:
               self.__debug("Gathering variable name")
               character, c1, c2 = self.next()
               token.components += c1

            #Throw the space out
            self.switchContext('variable')

            self.__debug("Returning variable declaration token")

            return token

      #Collect the entire variable contents
      if self.context == 'variable':

         self.__debug("Variable value")

         if c1 == END_DECLARATION:
            print "empty variable declaration"
            self.switchContext('global')
            return None

         token = Token(character)
         token.type = VALUE

         character, c1, c2 = self.next()
         while c1 != END_DECLARATION:
            self.__debug("Scanning for remainder of variable name")

            token.components += c1

            if c1 == '\\':
               if c2 in '\\:}':
                  token.components += c2
                  self.next()

            character, c1, c2 = self.next()

            #The token up to this point is actually a function call
            if c1 == ':':
               token.type = FUNCTION
               switchContext('function')
               #Clear trailing whitespace
               while c2 in INDENTATION:
                  self.__debug("SCANNING2")
                  character, c1, c2 = self.next()
               return token

         #skip }
         self.next()

         #Clear trailing whitespace
         while c2 in INDENTATION:
            self.__debug("SCANNING3")
            character, c1, c2 = self.next()

         self.switchContext('global')
         return token

      if self.context == 'function':
         self.restoreContext()
         #Enclosed function arguments
         if c1 == '(':
            self.switchContext('closed-funcargs')
            #Clear the paren
            self.next()

            #Clear trailing whitespace
            while c2 in INDENTATION:
               self.__debug("SCANNING4")
               character, c1, c2 = self.next()

         else:
            self.switchContext('funcargs')

      if self.context == 'funcargs':

         token = Token(character)
         token.type = ARGUMENT

         #Add initial spacing to the token
         while c1 in SPACING:
            self.__debug("SCANNING5")
            character, c1, c2 = self.next()
            token.components += c1

         #Then, consume everything up to the next whitespace
         while not c1 in SPACING:
            self.__debug("SCANNING6")
            if c1 == '\\':
               if c2 == ' ':
                  token.components += ' '
                  self.next()
            character, c1, c2 = self.next()
            token.components += c1

         #Argument list is over
         if c1 == "\n":
            self.next()
            self.restoreContext()
            return token

         #Do not add funcarg-delimiting whitespace
         self.next()

         return token

      if self.context == 'closed-funcargs':

         token = Token(character)
         token.type = ARGUMENT

         #Add initial spacing to the token
         while c1 in SPACING:
            self.__debug("SCANNING7")
            character, c1, c2 = self.next()
            token.components += c1

         #Then, consume everything up to the next whitespace
         while not c1 in SPACING:
            self.__debug("SCANNING8")
            if c1 == '\\':
               if c2 == ' ' or c2 == ')':
                  token.components += ' '
                  self.next()
            character, c1, c2 = self.next()
            token.components += c1

            if c2 == ')':
               #Funcargs ended; return context after stripping )
               self.next()
               self.restoreContext()
               return token

         return token

      #If we have not indented at all and we aren't using a name declaration, it's a selector
      if len(self.indentStack) == 1:
         self.__debug("Selector")
         token = Token(character)

         token.type = SELECTOR

         character, c1, c2 = self.next()

         while c1 != "\n":
            self.__debug("Seeking selector")
            token.components += c1

            #Declaration starting
            if c2 == DECLARATION:
               return token

            character, c1, c2 = self.next()

         #Remove the terminating newline
         self.next()

         self.__debug("Returning selector")

         return token

      return None

   def next(self):

      character = self.scanner.get()
      if character:
         c1 = character.cargo
         c2 = self.scanner.lookahead(1)

         self.__debug("Scanning next character %s (followed by %s)" % (c1, c2))

         return character, str(c1), str(c2)
      else:
         return None, None, None

   def switchContext(self, context):
      self.__debug("Changing context from %s to %s" % (self.context, context))
      self.lastcontext = self.context
      self.context = context

   def restoreContext(self):
      self.__debug("Restoring conext from %s to %s" % (self.context, self.lastcontext))
      context = self.context
      self.context = self.lastcontext
      self.lastcontext = context

   def get(self):
      token = self.getToken()
      while token != EOF:
         if token != None:
            self.tokens.append(token)

         token = self.getToken()

      for f in self.tokens:
         print f

   def __debug(self, arg):
      print arg

if __name__ == "__main__":
   f = open('../example.gss', 'r')
   f = f.read()

   scanner = Scanner(f)
   lexer = Lexer(scanner)

   lexer.get()
