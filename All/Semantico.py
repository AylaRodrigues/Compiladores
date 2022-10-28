from Sintatico import parser
from Lexer import tokens

Class = []
Type = []
Env = []

for i in range(len(tokens)):
    if tokens[i] not in Env:
        Env.append(tuple([tokens[i],5])) #ao inves do 5 seria o numero da ocorrencia/funcao(?)
        print(Env)
Env.pop()
print(Env)
