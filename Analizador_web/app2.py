from flask import Flask, render_template, request
import ply.lex as lex

app = Flask(__name__)

# List of token names
tokens = [
    'ID', 'PLUS', 'EQUAL','ACENTO','ERROR',
    'OPEN_PAREN', 'CLOSE_PAREN', 'OPEN_BRACE', 'CLOSE_BRACE', 'COMMA', 'SEMICOLON'
]

# Reserved words
reserved = {
    'int': 'INT', 'suma': 'SUMA', 'read': 'READ', 'printf': 'PRINTF',
    'programa': 'PROGRAMA', 'end': 'END'
}
allowed_ids = {'a', 'b', 'c', 'la', 'es'}

tokens = tokens + list(reserved.values())

t_PLUS = r'\+'
t_EQUAL = r'='
t_OPEN_PAREN = r'\('
t_CLOSE_PAREN = r'\)'
t_OPEN_BRACE = r'\{'
t_CLOSE_BRACE = r'\}'
t_COMMA = r','
t_SEMICOLON = r';'
t_ACENTO = r'"'
t_ignore = ' \t\n\r'



def t_id(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.value = t.value.lower()
    if t.value in reserved:
        t.type = reserved[t.value] 
    elif t.value in allowed_ids:
        t.type = 'ID'
    else:
        t.type = 'ERROR'  
    return t

def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.type = 'ERROR'
    t.value = t.value[0] 
    t.lexer.skip(1) 
    return t


@app.route('/', methods=['GET', 'POST'])
def index():
    counters = {tok: 0 for tok in tokens}
    counters.update({val: 0 for val in reserved.values()})
    token_data = []
    lexical_errors = [] 
    if request.method == 'POST':
        code = request.form.get('code', '')
        lexer = lex.lex()
        lexer.input(code)
        while True:
            tok = lexer.token()
            if not tok:
                break
            entry = {'token': tok.value, 'PR': '', 'ID': '', 'SIM': '', 'ERROR': ''}
            if tok.type in reserved.values():
                entry['PR'] = 'X'
            elif tok.type == 'ID':
                entry['ID'] = 'X'
            elif tok.type == 'ERROR':  # Agregar esta condición
                entry['ERROR'] = 'X'
                lexical_errors.append("Error Lexico: '%s'" % tok.value)    
            else:
                entry['SIM'] = 'X'   
                lexical_errors.append(tok.value) 
            counters[tok.type] += 1 
            token_data.append(entry)        
    total_reserved = sum(counters[val] for val in reserved.values())
    total_errors = counters['ERROR'] if 'ERROR' in counters else 0
   
    return render_template("index.html", token_data=token_data, counters=counters, total_reserved=total_reserved, lexical_errors=lexical_errors, total_errors=total_errors,) 

if __name__ == "__main__":
    app.run(debug=True)