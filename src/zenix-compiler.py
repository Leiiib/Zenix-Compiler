from time import *

iota = 1
class TokenTypes():
    
    TOKEN_NAME = iota; iota += 1
    TOKEN_OPAREN = iota; iota += 1
    TOKEN_CPAREN = iota; iota += 1
    TOKEN_OCURLY = iota; iota += 1
    TOKEN_CCURLY = iota; iota += 1
    TOKEN_NUMBER = iota; iota += 1
    TOKEN_BOOLEAN = iota; iota += 1
    TOKEN_STRING = iota; iota += 1
    TOKEN_COMMA = iota; iota += 1
    TOKEN_RETURN = iota; iota += 1
    TOKEN_IMPORT = iota; iota += 1

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

literal_returns = {
    "noreturn": None,
    "str": TokenTypes.TOKEN_STRING,
    "int": TokenTypes.TOKEN_NUMBER,
    "bool": TokenTypes.TOKEN_BOOLEAN
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
        return (f"<F:{self.file_path} R:{self.row + 1} C:{self.col + 1}>")

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

    def error(self, error: str):
        print(f"\033[31;1m[ERROR REPORT AT {self.loc().display()} ] {error}\033[0m")

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
        
    def is_string_delimiter(self, char):
        if(char == '"' or char == "'"): return True
        return False

    def next_token(self) -> Token:
        self.trim_left()    

        while (self.is_not_empty() and self.current_char() == "#"):
            self.drop_line()
            self.trim_left()

        if(self.is_empty()): 
            return False

        loc = self.loc()        
        first = self.current_char()     

        if(first == ","):
            self.chop_char()
            return Token(loc, TokenTypes.TOKEN_COMMA, ",")

        if(self.current_char().isalpha()):
            index = self.cur
            while (self.is_not_empty() and self.current_char().isalpha()):
                self.chop_char()
            value = self.get_sub_str(index, self.cur)
            return Token(loc, TokenTypes.TOKEN_NAME, value)

        if(first in literal_tokens):
            self.chop_char()
            return Token(loc, literal_tokens[first], first)
        
        if(self.is_string_delimiter(first)):
            self.chop_char()
            start = self.cur    
            while (self.is_not_empty() and self.current_char() != first):
                self.chop_char()
            
            if(self.is_not_empty()):
                value = self.get_sub_str(start, self.cur)
                self.chop_char()
                return Token(loc, TokenTypes.TOKEN_STRING, value)
            self.error('Unclosed string')
            return False
        if(first.isnumeric()):
            start = self.cur
            while (self.is_not_empty() and self.current_char().isnumeric()):
                self.chop_char()
            value = self.get_sub_str(start, self.cur)
            return Token(loc, TokenTypes.TOKEN_NUMBER, value)
        
        self.error('Unrecognized token')
        return False
    
class Statement:
    def __init__(self):
        pass

class ReturnStatement(Statement):
    def __init__(self, expresion: str):
        self.expression = expresion
        super().__init__()

class FunctionCallStatement(Statement):
    def __init__(self, name: str, args):
        self.name = name
        self.args = args
        super().__init__()

class Function:
    def __init__(self, name: str, body: list, return_type: str = "noreturn"):
        self.name = name
        self.body = body
        self.return_type = return_type

def expect_token(lexer: Lexer, *token_types: int):
    token = lexer.next_token()
    if(not token):
        lexer.error(f"Expected token of type/s {' or '.join([TokenTypes.from_index(type) for type in token_types])} but got end of file.")
        return False
    for type in token_types:
        if(token.type == type):
            return token    
    lexer.error(f"Expected token of type/s {' or '.join([TokenTypes.from_index(type) for type in token_types])} but got {TokenTypes.from_index(token.type)} '{token.value}'")
    return False

def parse_type(type: str):
    token = expect_token(lexer, TokenTypes.TOKEN_NAME)
    if(not token): return False
    keyword = token.value
    if(keyword != type):
        lexer.error(f"Unexpected keyword '{keyword}'")
        return False
    return token

def parse_args(lexer: Lexer):
    if(not expect_token(lexer, TokenTypes.TOKEN_OPAREN)): return False

    arglist = []
    while True:
        arg = expect_token(lexer, TokenTypes.TOKEN_NAME, TokenTypes.TOKEN_STRING, TokenTypes.TOKEN_NUMBER, TokenTypes.TOKEN_CPAREN)
        if(not arg): return False
        if(arg.type == TokenTypes.TOKEN_CPAREN): break
        if(arg.type == TokenTypes.TOKEN_NAME):
            if(not expect_token(lexer, TokenTypes.TOKEN_OPAREN)): return False
            if(not expect_token(lexer, TokenTypes.TOKEN_CPAREN)): return False
        arglist.append(arg.value)
        comma_or_cparen = expect_token(lexer, TokenTypes.TOKEN_COMMA, TokenTypes.TOKEN_CPAREN)
        if(not comma_or_cparen): return False
        if(comma_or_cparen.type == TokenTypes.TOKEN_CPAREN): break
        
    return arglist

def parse_fun_block(lexer: Lexer, return_type):
    if(not expect_token(lexer, TokenTypes.TOKEN_OCURLY)): return False

    block = []

    while True:
        name = lexer.next_token()
        if(not name): return False
        if(name.type == TokenTypes.TOKEN_CCURLY): break
        if(name.value == "return"):
            if(return_type == "noreturn"):
                lexer.error("Function with no return type is returning something")
                return False
            expresion = expect_token(lexer, literal_returns[return_type])
            if(not expresion): return False
            block.append(ReturnStatement(expresion.value))
        else:
            args = parse_args(lexer) 
            if(not args):
                lexer.error(f"Coudln't parse arguments for function: {name.value}")
                return False
            block.append(FunctionCallStatement(name.value, args))

    return block

def parse_fun(lexer: Lexer):
    isfun = parse_type("fun")
    if(not isfun): return False
    return_type_or_name = expect_token(lexer, TokenTypes.TOKEN_NAME)
    if(not return_type_or_name): return False
    name_or_oparen = lexer.next_token()
    if(not name_or_oparen): return False
    if(name_or_oparen.type == TokenTypes.TOKEN_NAME):
        if(not return_type_or_name.value in literal_returns):
            lexer.error(f"Function returns type is an invalid type '{return_type_or_name.value}'")
            return False
        return_type = return_type_or_name.value
        fun_name = name_or_oparen.value
        if(fun_name == "main"):
            lexer.error("Main function cannot return any type")
            return False
        if(not expect_token(lexer, TokenTypes.TOKEN_OPAREN)): return False
        if(not expect_token(lexer, TokenTypes.TOKEN_CPAREN)): return False
    elif(name_or_oparen.type == TokenTypes.TOKEN_OPAREN):
        return_type = "noreturn"
        fun_name = return_type_or_name.value
        if(not expect_token(lexer, TokenTypes.TOKEN_CPAREN)): return False
    body = parse_fun_block(lexer, return_type)
    if(not body): return False
    return Function(fun_name, body, return_type)


def read_file_to_list(file_path):
    try:
        with open(file_path, 'rb') as file:
            src_bytes = file.read()
            src = src_bytes.decode('utf-8')

        return list(src)
    except FileNotFoundError as e:
        print(f"\033[31;1mCouldn't load file '{file_path}': {e}")
        exit()

if __name__ == "__main__":
    file_path = 'src/code.ze'
    src_list = read_file_to_list(file_path)
    lexer: Lexer = Lexer(src_list, "code.ze")
    fun = parse_fun(lexer)
    print("Done compiling")
    sleep(1)
    print("\033c")
    

