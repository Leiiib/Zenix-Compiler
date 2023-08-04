import ctypes

def error(error: str):
    print(f"\033[31;1m{error}\033[0m")

class TokenTypes():
    TOKEN_NAME = 1
    TOKEN_OPAREN = 2
    TOKEN_CPAREN = 3
    TOKEN_OCURLY = 4
    TOKEN_CCURLY = 5
    TOKEN_NUMBER = 6
    TOKEN_STRING = 7
    TOKEN_RETURN = 8
    TOKEN_IMPORT = 9

    def from_index(index: int):
        dict = TokenTypes.__dict__
        for field in dict:
            if(field.isupper()):
                if(dict[field] == index):
                    return field

literal_tokens = {
    "(": TokenTypes.TOKEN_OPAREN,
    ")": TokenTypes.TOKEN_CPAREN,
    "{": TokenTypes.TOKEN_OCURLY,
    "}": TokenTypes.TOKEN_CCURLY,
}

class StmtTypes():
    STMT_FUNCALL = 1
    STMT_RETURN = 2

    def from_index(index: int):
        dict = TokenTypes.__dict__
        for field in dict:
            if(field.isupper()):
                if(dict[field] == index):
                    return field

class Loc: 
    def __init__(self, file_path: str, row: int, col: int):
        self.file_path = file_path
        self.row = row
        self.col = col

    def display(self) -> str:
        return (f"File: {self.file_path} r:{self.row + 1} c:{self.col + 1}")

class Token:
    def __init__(self, loc: Loc, type, value):
        self.type = type
        self.value = value
        self.loc = loc

class Lexer:
    
    def __init__(self, src: str, f_path: str):
        self.src: str = src
        self.cur: int = 0
        self.bol: int = 0
        self.row: int = 0
        self.file_path = f_path

    def get_sub_str(self, start: int, end: int) -> str:
        value = self.src[start:end]
        return ''.join(value)

    def current_char(self):
        return self.src[self.cur]

    def is_empty(self) -> bool:
        return self.cur+1 > len(self.src)
    
    def is_not_empty(self) -> bool:
        return not self.is_empty()
    
    def chop_char(self):
        if(self.is_not_empty()):
            c = self.current_char()
            self.cur += 1
            if(c == "\n"):
                self.bol = self.cur
                self.row += 1

    def loc(self) -> Loc:
        return Loc(self.file_path, self.row, self.cur - self.bol)
    
    def trim_left(self):
        while (self.is_not_empty()) and (self.current_char().isspace() or self.current_char() == '\n'):
            self.chop_char()

    def drop_line(self):
        while (self.is_not_empty() and self.current_char() != "\n"):
            self.chop_char()
        

    def next_token(self) -> Token:
        self.trim_left()    

        while (self.is_not_empty() and self.current_char() == "#"):
            self.drop_line()
            self.trim_left()

        if(self.is_empty()): 
            print("End of file")
            return False

        loc = self.loc()        
        first = self.current_char()

        if(self.current_char().isalpha()):
            index = self.cur
            while (self.is_not_empty() and self.current_char().isalpha()):
                self.chop_char()
            value = self.get_sub_str(index, self.cur)
            return Token(loc, TokenTypes.TOKEN_NAME, value)

        if(first in literal_tokens):
            self.chop_char()
            return Token(loc, literal_tokens[first], first)
        
        if(first == '"'):
            self.chop_char()
            start = self.cur    
            while (self.is_not_empty() and self.current_char() != '"'):
                self.chop_char()
            
            if(self.is_not_empty()):
                value = self.get_sub_str(start, self.cur)
                self.chop_char()
                return Token(loc, TokenTypes.TOKEN_STRING, value)

            error(f'Unclosed string {loc.display()}')
        
        if(first.isnumeric()):
            start = self.cur
            while (self.is_not_empty() and self.current_char().isnumeric()):
                self.chop_char()
            print(self.is_empty())
            value = self.get_sub_str(start, self.cur)
            return Token(loc, TokenTypes.TOKEN_NUMBER, value)
        
        error(f'Unrecognized token {loc.display()}')
        return False
    
class Satement:
    

class Function:
    def __init__(self):
        pass          

def expect_token(lexer, token_type: int):
    token = lexer.next_token()
    if(not token):
        error(f"Expected token")
        return False
    if(token.type != TokenTypes.TOKEN_NAME):

def parse_func(lexer: Lexer):
    expect_token(lexer, TokenTypes.TOKEN_NAME)


def read_file_to_list(file_path):
    try:
        with open(file_path, 'rb') as file:
            src_bytes = file.read()
            src = src_bytes.decode('utf-8')

        return list(src)
    except FileNotFoundError as e:
        error(f"Couldn't load file '{file_path}': {e}")
        exit()

if __name__ == "__main__":
    file_path = 'code.ze'
    src_list = read_file_to_list(file_path)
    lexer: Lexer = Lexer(src_list, "code.ze")
    token = lexer.next_token()
    while token:
        if(token): 
            print(f"{token.loc.display()} | {token.value} | {TokenTypes.from_index(token.type)}")
        token = lexer.next_token()
