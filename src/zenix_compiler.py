from zelexer import Lexer

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
    parser: Lexer = Lexer(src_list, "code.ze")
    tokens = parser.procces_tokens()
    print(tokens)
    print([token.value for token in tokens])