from ply.yacc import yacc
from Lexer import tokens, lexer
import sys


SE = 1

def p_program(p):
    '''program : class_list
                | empty'''
    p[0] = [p[1]]
    pass

def p_class_list(p):
    '''class_list : class_list class ponto_virgula
                    | class ponto_virgula'''
    if len(p) > 3:
        p[0] = p[1]
        p[0].append(p[2])
    else:
        p[0] = [p[1]]
    pass

def p_class (p) :
    '''class : CLASS ID INHERITS ID abre_chaves ft_list fecha_chaves
               | CLASS ID abre_chaves ft_list fecha_chaves'''
    if len(p) == 8:
        p[0] = ('classInh', p[2], p[4], p[6])
    else:
        p[0] = ('class', p[2], p[4])
    pass

def p_ft_list(p):
    '''ft_list : ft_list feature ponto_virgula
                |  empty'''
    if len(p) == 4:
        p[0] = [p[1]]
        p[0].append(p[2])
    elif len(p) == 2:
        p[0] = None

def p_feature(p):
    '''feature : ID abre_par formal_list fecha_par dois_pontos ID abre_chaves expr fecha_chaves
                | ID abre_par fecha_par dois_pontos ID abre_chaves expr fecha_chaves
                | ID dois_pontos ID seta expr
                | ID dois_pontos ID
                | empty'''
    if len(p) == 10:
        p[0] = ('featureReturnParametro',p[1],p[3],p[6],p[8])
    elif len(p) == 9:
        p[0] = ('featureReturn',p[1],p[5],p[7])
    elif len(p) == 6:
        p[0] = ('featureAnonimus',p[1],p[3],p[5])
    elif len(p) == 4:
        p[0] = ('featureDeclaration',p[1],p[3])
    elif len(p) == 2:
        p[0] = None
    pass

def p_formal_list(p):
    '''formal_list : formal_list virgula formal
                    | formal
                    | empty
                    '''
    if len(p) > 3:
        p[0] = p[1]
        p[0].append(p[3])
    elif len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = None
    pass

def p_formal(p):
    'formal : ID dois_pontos ID'
    p[0] = ('formal', p[1], p[3])
    pass

def p_ex_novo(p):
    'expr : NEW ID'
    p[0] = ('expNovo', p[1], p[2])
    pass

def p_ex_void(p):
    'expr : ISVOID expr'
    p[0] = ('expVoid', p[1], p[2])
    pass

def p_ex_not_comp(p):
    '''expr : NOT expr
            | til expr
            '''
    p[0] = ('expNot', p[1], p[2])
    pass

def p_ex_1(p):
    '''expr : string
            | TRUE
            | FALSE
            '''
    p[0] = ('expVal', p[1])
    pass

def p_ex_num(p):
    'expr : num'
    p[0] = ('expVal', tryParseInt(p[1]))
    pass

def p_ex_id(p):
    'expr : ID'
    p[0] = ('expID', p[1])
    pass


def p_ex_op(p):
    '''expr : expr mais expr
                | expr menos expr
                | expr multi expr
                | expr dividir expr
                '''
    p[0] = ('op', p[2], p[1], p[3])
    pass

def p_ex_comp(p):
    '''expr : expr menor expr
              | expr menor_igual expr
              | expr igual expr
              '''
    p[0] = ('comp', p[2], p[1], p[3])
    pass


def p_ex_2(p):
    'expr :  ID seta expr'
    p[0] = ('expSeta', p[1], p[2], p[3])
    pass

def p_ex_3(p):
    'expr :  abre_par expr fecha_par'
    p[0] = ('expEntreParenteses', p[2])
    pass

def p_id_expr(p):
    'expr : ID abre_par expr_list fecha_par'
    p[0] = ('expChamaMetodo', p[1], p[3])
    pass

def p_expr_arroba(p):
    '''expr : expr arroba ID ponto expr
            | expr ponto expr '''
    if len(p) == 9:
        p[0] = ('expArroba', p[1], p[3], p[5])
    else:
        p[0] = ('expArroba', p[1], p[3])
    pass

def p_expr_list(p):
    '''expr_list : expr_list virgula expr
                | expr
                |  empty'''
    if len(p) > 3:
        p[0] = p[1]
        p[0].append(p[3])
    elif len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = None
    pass

def p_ex_if(p):
    'expr : IF expr THEN expr ELSE expr FI'
    p[0] = ('expIf', p[2], p[4], p[6])
    pass

def p_ex_while(p):
    'expr : WHILE expr LOOP expr POOL'
    p[0] = ('expWhile', p[2], p[4])
    pass

def p_ex_4(p):
    'expr : abre_chaves expr_list_mais fecha_chaves'
    p[0] = ('expEntreChaves', p[2])
    pass


def p_expr_list_mais(p):
    '''expr_list_mais : expr_list_mais expr ponto_virgula
            | expr ponto_virgula '''
    if len(p) > 3:
        p[0] = p[1]
        p[0].append(p[2])
    else:
        p[0] = [p[1]]
    pass

def p_let_expr(p):
    '''expr : LET ID dois_pontos ID seta expr id_type_list IN expr
            | LET ID dois_pontos ID id_type_list IN expr '''
    if len(p) > 9:
        p[0] = ('exprLetSeta', p[2], p[4], p[6], p[7], p[9])
    else:
        p[0] = ('exprLet', p[2], p[4], p[5], p[7])
    pass

def p_id_type_list(p):
    '''id_type_list : id_type_list id_type
                    | id_type '''
    if len(p) == 3:
        p[0] = p[1]
        p[0].append(p[2])
    else:
        p[0] = [p[1]]
    pass

def p_id_type(p):
    '''id_type : virgula ID dois_pontos ID seta expr
                    | virgula ID dois_pontos ID
                    |  empty'''
    if len(p) == 7:
        p[0] = ('exprType', p[2], p[4], p[6])
    elif len(p) == 5:
        p[0] = ('exprType', p[2], p[4])
    else:
        p[0] = None
    pass

def p_case_expr(p):
    'expr : CASE expr OF 2_id_type_list ESAC'
    p[0] = ('exprCase', p[2], p[4])
    pass

def p_2_id_type_list(p):
    '''2_id_type_list : 2_id_type_list 2_id_type
                    | 2_id_type '''
    if len(p) == 3:
        p[0] = p[1]
        p[0].append(p[2])
    else:
        p[0] = [p[1]]
    pass

def p_2_id_type(p):
    '2_id_type : ID dois_pontos ID menor_igual expr ponto_virgula'
    p[0] = ('idType', p[1], p[3], p[5])
    pass

def p_empty(p):
    'empty : '
    pass

def p_error(p):
    if SE:
        if p is not None:
            print("Erro sintatico na linha: " + str(lexer.lineno)+"  Error: " + str(p.value))
        else:
            print("Erro lexico na linha: " + str(lexer.lineno))
    else:
        raise Exception('Syntax', 'error')

def tryParseInt(s):
    try:
        return int(s)
    except:
        return s

parser = yacc()

if (len(sys.argv) > 1):
    arq = sys.argv[1]
else:
    arq = 'helloworld.cl'

f = open(arq,'r')
data = f.read()
arvore = parser.parse(data, lexer=lexer)
