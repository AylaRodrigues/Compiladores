from Sintatico import parser
from Lexer import tokens

Classes=[

]

Tipos=[

]

for i in range(len(tokens)):
    if(tokens[i] in Classes):
        print('Yes, it is')
    else:
        Classes.append(tokens[i])
        print(Classes)

