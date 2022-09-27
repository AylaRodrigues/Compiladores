import ply.lex as lex
import sys
import os

def MyLexer (nomearq):
    reserved = {
    'class':'CLASS',
    'else': 'ELSE',
    'if': 'IF',
    'fi':'FI',
    'false':'FALSE',
    'in':'IN',
    'inherits':'INHERITS',
    'isvoid':'ISVOID',
    'let':'LET',
    'loop':'LOOP',
    'pool':'POOL',
    'then':'THEN',
    'while':'WHILE',
    'case':'CASE',
    'esac':'ESAC',
    'new':'NEW',
    'of':'OF',
    'not':'NOT',
    'true':'TRUE'
    }

    tokens = [
            'ID',
            'num',
            'mais',
            'menos',
            'multi',
            'dividir',
            'igual',
            'menor_igual',
            'menor',
            'dois_pontos',
            'ponto_virgula',
            'abre_par',
            'fecha_par',
            'abre_chaves',
            'fecha_chaves',
            'seta',
            'ponto',
            'string',
            'virgula',
            'arroba',
            'til',
            'comentario_linha',
            'comentario_bloco',
         ] + list(reserved.values())

    t_mais = r'\+'
    t_menos = r'\-'
    t_multi = r'\*'
    t_dividir = r'\/'
    t_igual = r'\='
    t_menor_igual = r'\<\='
    t_menor = r'\<'
    t_dois_pontos = r'\:'
    t_ponto_virgula = r'\;'
    t_virgula =r'\,'
    t_ponto = r'\.'
    t_abre_par = r'\('
    t_fecha_par = r'\)'
    t_abre_chaves = r'\{'
    t_fecha_chaves = r'\}'
    t_seta = r'\<\-'
    t_arroba = r'\@'
    t_til = r'\~'

    def t_string(t):
        r'".*"'
        return t

    def t_ID(t):
        r'[a-zA-Z_]+([a-zA-Z0-9_]*)'
        t.type = reserved.get(t.value, 'ID')  # Procurando palavras reservadas
        return t

    def t_num(t):
        r'\d+'
        t.value = int(t.value)
        return t

    def t_comentario_linha(t):
        r'[--]+([a-zA-Z0-9_]*)'
        if t.lexer : '\n'
        pass

    def t_comentario_bloco(t):
        r'(\(\*(.|\n)*?\*\))'
        pass

    # numero de linhas
    def t_newline(t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    t_ignore = ' \t'

    # caracter invalido
    def t_error(t):
        print("Caracter invalido'%s'" % t.value[0])
        t.lexer.skip(1)


    lexer = lex.lex()

    with open(nomearq) as file:
        data = file.read()

    lexer.input(data)

    while True:
        tok = lexer.token()
        if not tok:
            break      # No more input
        print(tok)
    return lex.lex()


path = sys.path[0]
print(path)

files = (file for file in os.listdir(path) if os.path.isfile(os.path.join(path, file)))
for file in files:
    if file.endswith('.cl'): #pra só pegar arquivos .cl
        print('\n\t'+ file)
        MyLexer(file)