import ply.yacc as yacc
from Lexer import MyLexer

def p_program(p):
    'program : class ponto_virgula'
    p[0] = p[1]

 #Perguntar como colocar partes opcionais
def p_class(p):
    'CLASS ID INHERITS ID abre_chaves fecha_chaves'

def p_formal(p):
    'formal : ID dois_pontos ID'
    p[0] = p[1] : p[3]

def p_expr_seta(p):
    'expr : ID seta ID'
    p[0] = p[1] <- p[3]

#Perguntar como proceder com if, then, ..., fi
def p_expr_if(p):
    'expr : IF expr THEN expr ELSE expr FI'
    p[0] = p[1] if p[3] then p[5] 'else' p[7] fi

def p_expr_new(p):
    'expr : NEW expr'
    p[0] =

def p_expr_true(p):
    'expr : TRUE'
    p[0] = True

def p_expr_false(p):
    'expr : FALSE'
    p[0] = False

def p_expr_bin(p):
     '''expr : expr mais expr
        	 | expr menos expr
        	 : expr multi expr
        	 | expr dividir expr
        	 : expr menor expr
        	 | expr menor_igual expr
        	 : expr igual expr        '''
     if p[2] == '+':
         p[0] = p[1] + p[3]
     elif p[2] == '-':
         p[0] = p[1] - p[3]
     elif p[2] == '*':
         p[0] = p[1] * p[3]
     elif p[2] == '/':
         p[0] = p[1] / p[3]
     elif p[2] == '<':
         p[0] = p[1] < p[3]
     elif p[2] == '<=':
         p[0] = p[1] <= p[3]
     elif p[2] == '=':
         p[0] = p[1] = p[3]

 def p_expr_menos(p):
     'expr : expr menos expr'
     p[0] = p[1] - p[3]

 def p_expr_multi(p):
     'expr : expr multi expr'
     p[0] = p[1] * p[3]

 def p_expr_dividir(p):
     'expr : expr dividir expr'
     p[0] = p[1] / p[3]

def p_error(p):
    print("Erro sintático!")

# Build the parser
parser = yacc.yacc()

while True:
   try:
       s = input('calc > ')
   except EOFError:
       break
   if not s: continue
   result = parser.parse(s)
   print(result)
