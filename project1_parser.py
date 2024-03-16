# Lexer
class Token:
    def __init__(self, type, value=None):
        self.type = type
        self.value = value

    def __repr__(self):
        return f"Token({self.type}, {self.value})"

class Lexer:
    def __init__(self, code):
        self.code = code
        self.position = 0
        self.current_char = self.code[self.position]

    def advance(self):
        self.position += 1
        if self.position >= len(self.code):
            self.current_char = None  # Indicates end of input
        else:
            self.current_char = self.code[self.position]

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def number(self):
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return int(result)

    def identifier(self):
        result = ''
        while self.current_char is not None and (self.current_char.isalnum() or self.current_char == '_'):
            result += self.current_char
            self.advance()
        return result

    # move the lexer position and identify next possible tokens.
    def get_token(self):
        # Skip any whitespace
        self.skip_whitespace()

        # End of input
        if self.current_char is None:
            return Token('EOF', None)

        # Number token
        if self.current_char.isdigit():
            return Token('NUMBER', self.number())

        # Identifier or keyword
        if self.current_char.isalpha():
            ident = self.identifier()
            # Check if the identifier matches any keyword
            if ident in ('if', 'then', 'else', 'while', 'do'):
                return Token('KEYWORD', ident)
            else:
                return Token('VARIABLE', ident)

        # Operators
        if self.current_char in ('+', '-', '*', '/', '(', ')', '=', '>', '<', '!', ';'):
            # Handle multi-character operators
            if self.current_char == '=' and self.peek() == '=':
                self.advance()
                self.advance()
                return Token('OPERATOR', '==')
            elif self.current_char == '!' and self.peek() == '=':
                self.advance()
                self.advance()
                return Token('OPERATOR', '!=')
            elif self.current_char == '>' and self.peek() == '=':
                self.advance()
                self.advance()
                return Token('OPERATOR', '>=')
            elif self.current_char == '<' and self.peek() == '=':
                self.advance()
                self.advance()
                return Token('OPERATOR', '<=')
            else:
                # Single character operators and parentheses
                char = self.current_char
                self.advance()
                return Token('OPERATOR' if char in ('+', '-', '*', '/', '=', '>', '<') else 'PAREN', char)

        # If we reach here, it means we encountered an unknown character
        raise Exception(f"Unknown character: {self.current_char}")

    def peek(self):
        # Look at the next character without consuming it
        peek_pos = self.position + 1
        if peek_pos >= len(self.code):
            return None
        return self.code[peek_pos]


# Parser
# Input : lexer object
# Output: AST program representation.


# First and foremost, to successfully complete this project you have to understand
# the grammar of the language correctly.

# We advise(not forcing you to stick to it) you to complete the following function 
# declarations.

# Basic idea is to walk over the program by each statement and emit a AST representation
# in list. And the test_utility expects parse function to return a AST representation in list.
# Return empty list for ill-formed programs.

# A minimal(basic) working parser must have working implementation for all functions except:
# if_statment, while_loop, condition.

class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = None

    # function to parse the entire program
    def parse(self):
        
    # move to the next token.
    def advance(self):

    # parse the one or multiple statements
    def program(self):
        
    
    # parse if, while, assignment statement.
    def statement(self):


    # parse assignment statements
    def assignment(self):
     

    # parse arithmetic experssions
    def arithmetic_expression(self):
        
   
    def term(self):
    

    def factor(self):


    # parse if statement, you can handle then and else part here.
    # you also have to check for condition.
    def if_statement(self):

    
    # implement while statment, check for condition
    # possibly make a call to statement?
    def while_loop(self):
    

    def condition(self):
