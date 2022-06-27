from token import Token, TokenType


class Scanner:
    def __init__(self, source: str):
        self.source = source
        self.tokens: list[Token] = []
        self.start = 0
        self.current = 0
        self.line = 0
        self.keywords = {
            "and": TokenType.AND,
            "class": TokenType.CLASS,
            "else": TokenType.ELSE,
            "false": TokenType.FALSE,
            "for": TokenType.FOR,
            "fun": TokenType.FUN,
            "if": TokenType.IF,
            "nil": TokenType.NIL,
            "or": TokenType.OR,
            "print": TokenType.PRINT,
            "return": TokenType.RETURN,
            "super": TokenType.SUPER,
            "this": TokenType.THIS,
            "true": TokenType.TRUE,
            "var": TokenType.VAR,
            "while": TokenType.WHILE,
        }

    def scan_tokens(self) -> list[Token]:

        while not self.at_end():
            self.start = self.current
            self.scan_token()

        self.tokens.append(Token(TokenType.EOF, "", None, self.line))
        return self.tokens

    def scan_token(self):
        char = self.advance()
        if char == "(":
            self.add_token(TokenType.LEFT_PAREN)
        elif char == ")":
            self.add_token(TokenType.RIGHT_PAREN)
        elif char == "{":
            self.add_token(TokenType.LEFT_BRACE)
        elif char == "}":
            self.add_token(TokenType.RIGHT_BRACE)
        elif char == ",":
            self.add_token(TokenType.COMMA)
        elif char == ".":
            self.add_token(TokenType.DOT)
        elif char == "-":
            self.add_token(TokenType.MINUS)
        elif char == "+":
            self.add_token(TokenType.PLUS)
        elif char == "*":
            self.add_token(TokenType.STAR)
        elif char == "!":
            self.add_token(TokenType.BANG_EQUAL if self.match("=") else TokenType.BANG)
        elif char == "=":
            self.add_token(
                TokenType.EQUAL_EQUAL if self.match("=") else TokenType.EQUAL
            )
        elif char == "<":
            self.add_token(TokenType.LESS_EQUAL if self.match("=") else TokenType.LESS)
        elif char == ">":
            self.add_token(
                TokenType.GREATER_EQUAL if self.match("=") else TokenType.GREATER
            )
        elif char == "/":
            if self.match("/"):
                while self.peek() != "\n" and not self.at_end():
                    self.advance()
            else:
                self.add_token(TokenType.SLASH)
        elif char == " ":
            pass
        elif char == "\r":
            pass
        elif char == "\t":
            pass
        elif char == "\n":
            self.line += 1
        elif char == '"':
            self.parse_string()
        elif char == "o":
            if (self.match("r")):
                self.add_token(TokenType.OR)
        else:
            if char.isdigit():
                self.parse_number()
            elif char.isalpha():
                self.parse_identifier()
            else:
                # print error
                pass

    def advance(self) -> str:
        current_char = self.source[self.current]
        self.current += 1
        return current_char

    def match(self, expected: str) -> bool:
        if self.at_end():
            return False

        if self.source[self.current] != expected:
            return False

        self.current += 1
        return True

    def peek(self) -> str:
        if self.at_end():
            return "\0"
        else:
            return self.source[self.current]

    def peek_next(self) -> str:
        if self.current + 1 >= len(self.source):
            return "\0"
        else:
            return self.source[self.current + 1]

    

    def add_token(self, token_type: TokenType):
        self.add_token_literal(token_type, None)

    def add_token_literal(self, token_type: TokenType, literal: object):
        text = self.source[self.start : self.current]
        self.tokens.append(Token(token_type, text, literal, self.line))

    def at_end(self) -> bool:
        return self.current >= len(self.source)

    def parse_string(self):
        while self.peek() != '"' and not self.at_end():
            if self.peek() == "\n":
                self.line += 1
            self.advance()

        if self.at_end():
            # error
            return

        self.advance()
        value = self.source[self.start + 1:self.current - 1]
        self.add_token_literal(TokenType.STRING, value)

    def parse_number(self):
        while self.peek().isdigit():
            self.advance()
        
        if self.peek() == "." and self.peek_next().isdigit():
            self.advance()

            while self.peek().isdigit():
                self.advance()

        self.add_token_literal(TokenType.NUMBER, float(self.source[self.start:self.current]))

    def parse_identifier(self):
        while self.peek().isalnum():
            self.advance()
        
        text = self.source[self.start:self.current]
        token_type = self.keywords.get(text)
        if token_type is None:
            token_type = TokenType.IDENTIFIER
        
        self.add_token(token_type)
