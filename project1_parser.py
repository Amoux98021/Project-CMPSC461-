#Lexer Class Functions
#__init__- Setup, Initializes the lexer with a string of code and sets up the current position and characters for tokenization
#advance- Moves to the next character in our input code. It moves till End-Of-Input(EOI) by setting the current character to None
#skip_whitespace- Advances over any whitespace characters, ignoring them during tokenization
#number- Extracts a numerical value (as a string) from the current position, this advances until a non-digit character is encountered
#identifier- It captures an identifier or keyword from the input. Similar to number it continues until a non-alphanumeric character or underscore is found
#get_token- Main method for our token generation. Depending on the current character, it will identify the appropriate token type (number, keyword and operator) and returns a new Token instance
#peek- Returns the character at the next position without advancing the lexer. Helps for lookahead operations, like identifying multi-character operators(==, <=, >=, etc)

# Lexer
class Token: # Token
    def __init__(self, type, value=None): 
        self.type = type
        self.value = value

    def __repr__(self):
        return f"Token({self.type}, {self.value})"

class Lexer:
    def __init__(self, code): # Initialize
        self.code = code
        self.position = 0
        self.current_char = self.code[self.position]

    def advance(self): # Move to the next character
        self.position += 1
        if self.position >= len(self.code):
            self.current_char = None  # Indicates the end of our input
        else:
            self.current_char = self.code[self.position]

    def skip_whitespace(self): # Advance over any whitespace
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def number(self): # Number values until non-digit character encountered
        result = ''
        while self.current_char is not None and self.current_char.isdigit(): # isdigit
            result += self.current_char
            self.advance()
        return int(result)

    def identifier(self): # Identifiers like if-else and while-do
        result = ''
        while self.current_char is not None and (self.current_char.isalnum() or self.current_char == '_'):
            result += self.current_char
            self.advance()
        return result

    # We move the lexer position and identify all next possible tokens
    def get_token(self): # It will identify the type of Token based on numbers, operator and keywords
        self.skip_whitespace()  # Skip whitespace

        if self.current_char is None:  # EOI = End of Input
            return Token('EOI', None)

        if self.current_char.isdigit():
            return Token('NUMBER', self.number())  # For all Numbers

        if self.current_char.isalpha():
            ident = self.identifier() # Identifiers

            # We check if the identifier has a specific keyword
            if ident == 'if':
                return Token('IF', 'if')
            elif ident == 'then':
                return Token('THEN', 'then')
            elif ident == 'else':
                return Token('ELSE', 'else')
            elif ident == 'while':
                return Token('WHILE', 'while')
            elif ident == 'do':  # Handle 'do' keyword (Added the fix while_loop error)
                return Token('DO', 'do')
            else:
                return Token('VARIABLE', ident) # Else case (No valid keywords)

        # Operators
        if self.current_char in ('+', '-', '*', '/', '(', ')', '=', '>', '<', '!', ';'): # Handles all cases
            # Cases to handle multi-character operators
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

        # If we reach here it means we encountered an unknown character
        raise Exception(f"Error- Unknown character: {self.current_char}")

    def peek(self): # To help handle Multi-Character operators
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
        self.current_token = self.lexer.get_token()
    # Move to the next token.
    def advance(self):
        self.current_token = self.lexer.get_token()
    # Function to parse the entire program
    def parse(self):
        return self.program()
    # Parse the one or multiple statements
    def program(self):
        statements = []
        while self.current_token.type != 'EOI':
            statements.append(self.statement())
        return statements

    def statement(self): # Determines the type of statement based on the token
        if self.current_token.type == 'IF': # Goes to if_statement method
            return self.if_statement()
        elif self.current_token.type == 'WHILE': # while_loop
            return self.while_loop()
        elif self.current_token.type == 'VARIABLE': # assignment
            return self.assignment()

    def assignment(self):
        var_token = self.current_token
        self.advance()
        if self.current_token.type != 'OPERATOR' or self.current_token.value != '=':
            raise Exception("Error- Invalid assignment syntax") # Debug
        self.advance()
        expr = self.arithmetic_expression()
        return ('=', var_token.value, expr)
    # To parse arithmetic experssions (All binary operations included)
    def arithmetic_expression(self):
        node = self.term()
        while self.current_token.type == 'OPERATOR' and self.current_token.value in ('+', '-'):
            token = self.current_token
            self.advance()
            node = (token.value, node, self.term())
        return node

    def term(self): # '*' and '/'
        node = self.factor()
        while self.current_token.type == 'OPERATOR' and self.current_token.value in ('*', '/'):
            token = self.current_token
            self.advance()
            node = (token.value, node, self.factor())
        return node

    def factor(self):
        token = self.current_token
        if token.type == 'NUMBER':
            self.advance()
            return token.value
        elif token.type == 'VARIABLE':
            self.advance()
            return token.value
        elif token.type == 'PAREN' and token.value == '(':
            self.advance()
            node = self.arithmetic_expression()
            if self.current_token.type == 'PAREN' and self.current_token.value == ')':
                self.advance()
                return node
            else:
                raise Exception("Error- Missing closing parenthesis") # D
        else:
            raise Exception(f"Error- Unexpected token: {token}") # D

    def if_statement(self):
        self.advance()  # Move past 'IF' as if_statement is only called if the token 'IF' is detected
        condition_node = self.condition()

        if self.current_token.type != 'THEN': # Checking for 'THEN'
            raise Exception("Error- Expected 'then' after 'if' condition") # If there is no then token after if (Since its autograded, error wont be caused)
        self.advance()  # Move past 'THEN'

        then_branch = self.statement()

        else_branch = None # If else is not present the code will print the output without the else_branch
        if self.current_token.type == 'ELSE':
            self.advance()  # Move past 'ELSE'
            else_branch = self.statement()

        if else_branch is None: # else_branch cases
            return ('if', condition_node, then_branch)
        else:
            return ('if', condition_node, then_branch, else_branch)

    def expect(self, expected_type, expected_value=None): # Helps debug 
        if self.current_token.type != expected_type or (expected_value is not None and self.current_token.value != expected_value):
            raise Exception(f"Error- Expected {expected_type} but got {self.current_token.type}")
        self.advance()
    
    def while_loop(self): # Working while loop
        self.advance()  # Assuming 'while' token already matched, advance past 'while'
        
        condition_node = self.condition()
        #print(f"Condition parsed: {condition_node}")
        #print(f"Current Token before expecting 'DO': {self.current_token}") 
        #print(f"Current Token Type: {self.current_token.type}, Value: '{self.current_token.value}'")
        if self.current_token.type != 'DO':
            #print("Raising exception due to not 'DO'") #debug
            raise Exception("Error- Expected 'do'")
        self.advance()  # Advance past 'do'
        
        #print(f"Current Token after 'do': {self.current_token}")
        
        do_branch = self.statement() 
        body = [do_branch] # [] added to fix error
        #print(f"Body parsed: {do_branch}")
        return ('while', condition_node, body)

        # All print statements to help debug. Issue- Expected 'do'
    
    def condition(self): # All conditional expressions in our 'if' and 'while' statements
        left = self.arithmetic_expression()
        
        if self.current_token.type == 'OPERATOR' and self.current_token.value in ('==', '!=', '<', '>', '<=', '>='):
            operator = self.current_token.value
            self.advance()
            right = self.arithmetic_expression()
            return (operator, left, right)
        else:
            raise Exception("Error- Invalid condition")

# Parser Class Functions
#__init__- Initializes the parser with a Lexer instance. Starts by immediately fetching the first token to start parsing
#advance- Updates the current token by fetching the next token from the lexer
#parse- Begins the parsing process, to construct an Abstract Syntax Tree (AST)
#program- This handles the parsing of the entire program. It will loop through statements until the end of input (EOI) token is encountered
#statement- Determines the type of statement based on the current token (if, while, or assignment) and directs control to the corresponding parsing method (Every type of token has a different function)
#assignment- Parses assignment statements (variable followed by an = operator and an expression)
#arithmetic_expression- Parses arithmetic expressions (binary operations (+, -, *, /))
#term- This is a part of our arithmetic expression parsing, specifically dealing with multiplication and division operations for correct operator precedence
#factor- Parses the smallest units of arithmetic expressions, including numbers, variables, and parenthesis expressions
#if_statement- Handles the parsing of if statements, including condition evaluation and branching for then and optional else parts (IMP)
#while_loop- Parses while loop constructs, including the condition and the loop body (do_branch), ensuring correct handling of the do keyword
#condition- Parses conditional expressions used in if and while statements
#expect- Helps handle unexpected errors (test for tokens)
