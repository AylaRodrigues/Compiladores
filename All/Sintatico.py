import ply.yacc as yacc
from Lexer import MyLexer
import sys
import os


path = sys.path[0]
files = (file for file in os.listdir(path) if os.path.isfile(os.path.join(path, file)))
for file in files:
    if file.endswith('.cl'):  # pra só pegar arquivos .cl
        print('\n\t' + file)
        print(MyLexer(file).tokens)

SE =1

def p_empty(p):
    'empty : '
    pass

def p_program(p):
    '''program : class_list
                | empty '''
    pass

def p_class (p) :
    '''class : CLASS ID INHERITS ID abre_chaves ft_list fecha_chaves
               | CLASS ID abre_chaves ft_list fecha_chaves '''
    pass

def p_class_list(p):
    '''class_list : class_list class ponto_virgula
                | class ponto_virgula '''
    pass

def p_feature(p):
    '''feature : ID abre_par formal_list fecha_par dois_pontos ID abre_chaves expr fecha_chaves
            | ID abre_par fecha_par dois_pontos ID abre_chaves expr fecha_chaves
            | ID dois_pontos ID seta expr
            | ID dois_pontos ID
            | empty '''
    pass

def p_ft_list(p):
    '''feature_list : ft_list feature ponto_virgula
                    | empty '''

def p_formal(p):
    'formal : ID dois_pontos ID'
    #p[0] = p[1] : p[3]
    pass

def p_formal_list(p):
    '''formal_list : formal_list virgula formal
                    | empty
                    | formal '''
    pass

def p_1_expr(p):
    '''expr : ID seta expr
            | NEW ID
            | ISVOID expr
            | expr mais expr
            | expr menos expr
            | expr multi expr
            | expr divide expr
            | til expr
            | expr menos expr
            | expr menor_igual expr
            | expr igual expr
            | NOT expr
            | abre_par expr fecha_par
            | ID
            | num
            | string
            | TRUE
            | FALSE '''
    pass

def p_expr_list(p):
    '''expr_list : expr_list virgula expr
                | expr
                | empty '''
    pass

def p_id_expr(p):
    'expr : ID abre_par expr_list fecha_par'
    pass

def p_expr_arroba(p):
    '''expr : expr arroba ID ponto ID abre_par expr_list fecha_par
            | expr ponto ID abre_par expr_list fecha_par '''
    pass

def p_if_expr(p):
    'expr : IF expr THEN expr ELSE expr FI'
    pass

def p_while_expr(p):
    'expr : WHILE expr LOOP expr POOL'
    pass

def p_2_expr(p):
    'expr : abre_chaves expr_list_mais fecha_chaves'
    pass

def p_expr_list_mais(p):
    '''expr_list_mais : expr_list_mais expr ponto_virgula
            | expr ponto_virgula '''
    pass

def p_let_expr(p):
    '''expr : LET ID dois_pontos ID seta expr id_type_list IN expr
            | LET ID dois_pontos ID id_type_list IN expr '''
    pass

def p_id_type_list(p):
    '''id_type_list : id_type_list id_type
                    | id_type '''
    pass

def p_id_type(p):
    '''id_type : virgula ID dois_pontos ID seta expr
                    | virgula ID dois_pontos ID
                    | empty '''
    pass

def p_2_id_type(p):
    '2_id_type : ID dois_pontos ID igual_maior expr ponto_virgula'
    pass

def p_2_id_type_list(p):
    '''2_id_type_list : 2_id_type_list 2_id_type
                    | 2_id_type '''
    pass

def p_case_expr(p):
    'expr : CASE expr OF 2_id_type_list ESAC'
    pass


def p_erro(p):
    if SE:
        if p is not None:
            print ("Erro sintatico na linha: " + str(lexer.lineno)+"  Erro contextual: " + str(p.value))
        else:
            print ("Erro lexico na linha: " + str(lexer.lineno))
    else:
        raise Exception('Syntax', 'error')


parser = yacc.yacc()

while True:
   try:
       s = input('calc > ')
   except EOFError:
       break
   if not s: continue
   result = parser.parse(s)
   print(result)
