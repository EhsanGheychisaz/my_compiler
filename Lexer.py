class Token:
    def __init__(self, type, value, line=1, column=1):
        self.type = type
        self.value = value
        self.line = line
        self.column = column

class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.line = 1
        self.column = 1
        self.current_char = self.text[self.pos] if text else None
        
        self.keywords = {
            'def': 'DEF',
            'if': 'IF',
            'else': 'ELSE',
            'while': 'WHILE',
            'return': 'RETURN'
        }

    def error(self):
        raise Exception(f'Invalid character at line {self.line}, column {self.column}')

    def advance(self):
        if self.current_char == '\n':
            self.line += 1
            self.column = 1
        else:
            self.column += 1
            
        self.pos += 1
        self.current_char = self.text[self.pos] if self.pos < len(self.text) else None

    def skip_whitespace(self):
        while self.current_char and self.current_char.isspace():
            self.advance()

    def get_number(self):
        result = ''
        while self.current_char and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return int(result)

    def get_identifier(self):
        result = ''
        while self.current_char and (self.current_char.isalnum() or self.current_char == '_'):
            result += self.current_char
            self.advance()
        return result

    def get_next_token(self):
        while self.current_char:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char.isdigit():
                return Token('NUMBER', self.get_number(), self.line, self.column)

            if self.current_char.isalpha() or self.current_char == '_':
                identifier = self.get_identifier()
                token_type = self.keywords.get(identifier, 'IDENTIFIER')
                return Token(token_type, identifier, self.line, self.column)

            # Handle operators and other symbols
            if self.current_char == '+':
                self.advance()
                return Token('PLUS', '+', self.line, self.column)
            
            if self.current_char == '-':
                self.advance()
                return Token('MINUS', '-', self.line, self.column)

            if self.current_char == '*':
                self.advance()
                return Token('MULTIPLY', '*', self.line, self.column)

            if self.current_char == '/':
                self.advance()
                return Token('DIVIDE', '/', self.line, self.column)

            if self.current_char == '(':
                self.advance()
                return Token('LPAREN', '(', self.line, self.column)

            if self.current_char == ')':
                self.advance()
                return Token('RPAREN', ')', self.line, self.column)

            if self.current_char == '=':
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    return Token('EQUALS', '==', self.line, self.column)
                return Token('ASSIGN', '=', self.line, self.column)

            self.error()

        return Token('EOF', None, self.line, self.column)