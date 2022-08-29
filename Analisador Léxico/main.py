import struct
nomearq=input('Digite o nome do arquivo:\n')
palavras=[]
numLinha=[]
numLin=0

#abrindo o arquivo
with open(nomearq) as arquivo:
	for linha in arquivo:
		numLin+=1
		#dividindo o arq em linhas
		linha = linha.strip()
		palavras.append(linha)
		numLinha.append(numLin)
	print(palavras)
	print(numLinha)

