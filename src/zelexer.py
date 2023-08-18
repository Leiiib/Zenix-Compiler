import typing

def is_empty(txt: str) -> str:
    return txt.isspace() or txt == '\n' or txt == '\r'

class Loc: 
    def __init__(self, file_path: str, row: int, col: int):
        self.file_path = file_path
        self.row = row
        self.col = col

    def display(self) -> str:
        return (f"<F:{self.file_path} R:{self.row + 1} C:{self.col + 1}>")
    
def error(error: str, loc: Loc):
    print(f'\033[31;1m CAUGHT ERROR AT {loc.display()} : {error}', end='\033[0m\n')
    exit(69)

def waring(waring: str, loc: Loc):
    print(f'\033[33;1m WARING AT {loc.display()} : {waring}', end='\033[0m\n')

class Token:
    def __init__(self, loc: Loc, value):
        self.value = value
        self.loc = loc

class Tokens:
    class TokenName(Token):
        def __init__(self, loc: Loc, value):
            super().__init__(loc, value)

    class TokenOpenParen(Token):
        def __init__(self, loc: Loc):
            super().__init__(loc, '(')

    class TokenCloseParen(Token):
        def __init__(self, loc: Loc):
            super().__init__(loc, ')')

    class TokenString(Token):
        def __init__(self, loc: Loc, value):
            super().__init__(loc, value)

    class TokenInteger(Token):
        def __init__(self, loc: Loc, value: str):
            if(not value.isnumeric()): error("Content should be an integer.")
            super().__init__(loc, value)

class Lexer():
    def __init__(self, src: str, f_path: str):
        self.src = src
        self.cur: int = 0
        self.bol: int = 0
        self.row: int = 0
        self.f_path = f_path
        self.leng = len(src)

    def char(self):
        return self.src[self.cur]
    
    def is_emty(self):
        return ((self.cur + 1) > self.leng)

    def is_not_empty(self):
        return not self.is_emty()

    def chop_char(self):
        if(self.is_not_empty()):
            c = self.char()
            self.cur += 1
            if(c == ("\n" or '\r')):
                self.bol = self.cur
                self.row += 1

    def trim_left(self):
        while (self.is_not_empty()) and (self.char().isspace() or self.char() == ('\n' or '\r')):
            self.chop_char()
            
    def drop_line(self):
        while (self.is_not_empty() and self.char() != ("\n" or '\r')):
            self.chop_char()

    def loc(self) -> Loc:
        return Loc(self.f_path, self.row, self.cur - self.bol)
    
    def get_sub_str(self, start: int, end: int) -> str:
        value = self.src[start:end]
        return ''.join(value)
    
    def procces_tokens(self) -> typing.List[Token]:
        tks = list()
        while self.is_not_empty():
            self.trim_left()
            while (self.is_not_empty() and self.char() == "#"):
                self.drop_line()
                self.trim_left()
            loc = self.loc()
            if(self.char() == '('):
                tks.append(Tokens.TokenOpenParen(loc))
                self.chop_char()
            elif(self.char() == ')'):
                tks.append(Tokens.TokenCloseParen(loc))
                self.chop_char()
            elif(self.char().isalpha()):
                start = self.cur
                while self.char().isalpha() and self.is_not_empty():
                    self.chop_char()
                    loc = self.loc()
                content = self.get_sub_str(start, self.cur)
                tks.append(Tokens.TokenName(loc, content))
            elif(self.char().isnumeric()):
                start = self.cur
                while self.char().isnumeric():
                    self.chop_char()
                    loc = self.loc()
                content = self.get_sub_str(start, self.cur)
                tks.append(Tokens.TokenInteger(loc, content))
            else:
                error("Undefined token", loc)
        return tks
"""   
repeats = {
    'exit': ['exdit', Tokens.TokenOpenParen, Tokens.TokenCloseParen]
}


def check_regex(regex: list):
    for repeat in repeats:
        repeat_list = repeats.get(repeat)
        if len(repeat_list) != len(regex):
            print(f"Pattern '{repeat}' does not match the reference regex.")
            continue
        for i in range(len(repeat_list)):
            if(isinstance(regex[i], str)):
                print(regex[i])
                if(isinstance(repeat_list[i], str)):
                    if(regex[i] != repeat_list[i]): return False
                    else: 
                        continue
            elif(isinstance(regex[i], Token)):
                if(isinstance(repeat_list[i], Token)):
                    if(not isinstance(regex[i], repeat_list[i])): return False
                    else: continue
            else: return False
    return True
"""