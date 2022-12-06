from Sintatico import arvore
import copy

#lista de tipos organizadas de forma (<nome>, <de quem herda>, <metodos>, <IDs(?)>)
TypeList = [('Object', None, [('abort', [], 'Object'), ('type_name', [], 'String'), ('copy', [], 'SELF_TYPE')], []),
        ('SELF_TYPE', None, [], []),
        ('IO', 'Object', [('out_string', [('x', 'String')], 'SELF_TYPE'), ('out_int', [('x', 'Int')], 'SELF_TYPE'), ('in_string', [], 'String'), ('in_int', [], 'Int')], []),
        ('Int', 'IO', [], []),
        ('String', 'IO', [('length', [], 'Int'), ('concat', [('s', 'String')], 'String'), ('substr', [('i', 'Int'), ('l', 'Int')], 'String')], []),
        ('Bool', 'IO', [], [])]
MethodsList = []
IDsList = []

scope = 'program'

for Type in TypeList:
    for method in Type[2]:
        MethodsList.append(method)

for Type in TypeList:
    for ID in Type[3]:
        IDsList.append(ID)


def percorrerArv( t ):
    if type(t) == list or type(t) == tuple:
        for filho in t:
            percorrerArv(filho)
        print(t[0])


def chamarFun( t, IDsList, MethodsList, TypeList ):
    if t == None:
        return

    newTypeList = []
    newIDsList = []
    newMethodsList = []
    newTypeList = TypeList

    if isNewScopeClass(t[0]):
        global scope
        scope = t[1]
        newMethodsList = copy.deepcopy(MethodsList)
        newIDsList = IDsList
    elif isNewScopeMethod(t[0]) or isNewScopeLet(t[0]):
        newIDsList = copy.deepcopy(IDsList)
        newMethodsList = MethodsList

    else:
        newTypeList = TypeList
        newIDsList = IDsList
        newMethodsList = MethodsList

    if t[0] == 'idType':
        manipulaIdType(t, IDsList, newTypeList)
    elif t[0] == 'expID':
        manipulaExprId(t, newIDsList)
    elif t[0] == 'expType':
        manipulaExprLetSeta(t, newIDsList, newTypeList)
        chamarFun(t[5], newIDsList, newMethodsList, newTypeList)
    elif t[0] == 'expLet':
        manipulaExprLet(t, newIDsList, newTypeList)
        chamarFun(t[4], newIDsList, newMethodsList, newTypeList)
    elif t[0] == 'expEntreChaves':
        chamarFun(t[1], newIDsList, newMethodsList, newTypeList)
    elif t[0] == 'expWhile':
        manipulaExprWhile(t, newIDsList)
        chamarFun(t[3], newIDsList, newMethodsList, newTypeList)
    elif t[0] == 'expIf':
        manipulaExprIf(t, newIDsList)
        chamarFun(t[2], newIDsList, newMethodsList, newTypeList)
        chamarFun(t[3], newIDsList, newMethodsList, newTypeList)
    elif t[0] == 'expChamaMetodo':
        manipulaExprCallMetodo(t, newMethodsList, newIDsList)
    elif t[0] == 'expArroba':
        nome = None
        methodName = None
        if t[1][0] == 'expChamaMetodo':
            nome = getMetodo(t[1][1], newMethodsList)[2]
            methodName = t[1][1]
        else:
            aux = getId(t[1][1], newIDsList)
            methodName = t[2][1]
            if aux != None:
                nome = aux[1]
        if nome != None:
            tipo = getType(nome, newTypeList)
            if nome == 'SELF_TYPE':
                configSelfType(newIDsList, newMethodsList, newTypeList)
            if not isInListMetodo(t[2][1], tipo[2]):
                print("Erro de chamada: metodo %s não pertence ao tipo %s" % methodName, nome)
        chamarFun(t[1], newIDsList, newMethodsList, newTypeList)
    elif t[0] == 'expSemArroba':
        nome = None
        methodName = None
        if t[1][0] == 'exprCallMetodo':
            nome = getMetodo(t[1][1], newMethodsList)[2]
            methodName = t[1][1]
        else:
            aux = getId(t[1][1], newIDsList)
            methodName = t[2][1]
            if aux != None:
                nome = aux[1]
        if nome != None:
            tipo = getType(nome, newTypeList)
            if nome == 'SELF_TYPE':
                configSelfType(newIDsList, newMethodsList, newTypeList)
            if not isInListMetodo(methodName, tipo[2]):
                print("Erro de chamada: metodo %s não pertence ao tipo %s" % methodName, nome)
        chamarFun(t[1], newIDsList, newMethodsList, newTypeList)
    elif t[0] == 'exprEntreParenteses':
        chamarFun(t[1], newIDsList, newMethodsList, newTypeList)
    elif t[0] == 'expSeta':
        manipulaExprSeta(t, newIDsList)
    elif t[0] == 'op':
        manipulaOp(t, newIDsList)
    elif t[0] == 'comp':
        manipulaComp(t, newIDsList)
    elif t[0] == 'expNovo':
        manipulaExprNew(t, newIDsList)
    elif t[0] == 'expVoid':
        manipulaExprVoid(t, newIDsList)
    elif t[0] == 'expNot':
        manipulaExprNot(t, newIDsList)
    elif t[0] == 'formal':
        manipulaFormal(t, newIDsList, newTypeList)
    elif t[0] == 'featureReturnParametro':
        manipulaFeatureRetornoParametro(t, newIDsList, newMethodsList, newTypeList)
        for formal in t[4]:
            chamarFun(formal, newIDsList, newMethodsList, newTypeList)
    elif t[0] == 'featureReturn':
        manipulaFeatureRetorno(t, newMethodsList, newTypeList)
        chamarFun(t[3], newIDsList, newMethodsList, newTypeList)
    elif t[0] == 'featureAnonimus':
        manipulafeatureAnonima(t, newIDsList, newTypeList)
        for formal in t[2]:
            chamarFun(formal, newIDsList, newMethodsList, newTypeList)
    elif t[0] == 'featureDeclaration':
        manipulaFeatureDeclaration(t, newIDsList, newTypeList)
    elif t[0] == 'class':
        for formal in t[2]:
            chamarFun(formal, newIDsList, newMethodsList, newTypeList)
    elif t[0] == 'classInh':
        manipulaClasseInh(t, newTypeList)
        for formal in t[3]:
            if type(formal) == list:
                for i in formal:
                    chamarFun(i, newIDsList, newMethodsList, newTypeList)
            else:
                chamarFun(formal, newIDsList, newMethodsList, newTypeList)
    else:
        if type(t) == list:
            for i in t:
                chamarFun(i, newIDsList, newMethodsList, newTypeList)


def manipulaIdType( t, IDsList, TypeList ):
    if len(t) == 4:
        aux = ('featureAnonima', t[1], t[2], t[3])
        manipulafeatureAnonima(aux, IDsList, TypeList)
    elif len(t) == 3:
        aux = ('featureDeclaration', t[1], t[2])
        manipulaFeatureDeclaration(aux, IDsList, TypeList)
    pass


def manipulaExprId( t, IDsList ):
    if not isInListId(t[1], IDsList):
        print("Erro de declaração: %s não foi declarado" % t[1])


def manipulaExprLetSeta( t, IDsList, TypeList ):
    aux = ('featureAnonima', t[1], t[2])
    manipulafeatureAnonima(aux, IDsList, TypeList)
    for fanonima in t[3]:
        if fanonima != None:
            manipulaIdType(fanonima, IDsList, TypeList)


def manipulaExprLet( t, IDsList, TypeList ):
    aux = ('featureDeclaration', t[1], t[2])
    manipulaFeatureDeclaration(aux, IDsList, TypeList)
    for fanonima in t[3]:
        if fanonima != None:
            manipulaIdType(fanonima, IDsList, TypeList)


def manipulaExprWhile( t, IDsList ):
    if t[1][0] == 'comp':
        manipulaComp(t[1], IDsList)
        return
    if t[1][0] == 'expNot':
        manipulaExprNot(t[1], IDsList)
        return
    print('Erro de declaração: expressão {t[1]} não é booleano')


def manipulaExprIf( t, IDsList ):
    if t[1][0] == 'comp':
        manipulaComp(t[1], IDsList)
        return
    if t[1][0] == 'expNot':
        manipulaExprNot(t[1], IDsList)
        return
    print("Erro de declaração: expressão %s não é booleano" % t[1])


def manipulaExprCallMetodo( t, MethodsList, IDsList ):
    if not isInListMetodo(t[1], MethodsList):
        print("Erro de chamada: metodo %s não declarado" % t[1])
    verificaParametroCall(t[2], getMetodo(t[1], MethodsList), IDsList)


def manipulaExprEntreParenteses( t ):
    pass


def manipulaExprSeta( t, IDsList ):
    if getId(t[1], IDsList) == None:
        print("Erro de atribuição: %s não foi declarada" % t[1])
    elif t[3][0] == 'op':
        manipulaOp(t[3], IDsList)
    elif t[3][0] == 'expID':
        id = getId(t[3][1], IDsList)
        if id == None:
            print("Erro de atribuição: %s não foi declarada" % t[3][1])
    return t[1]


def manipulaOp( t, IDsList ):
    id1 = getId(t[2], IDsList)
    id2 = getId(t[3], IDsList)

    if id1 == None:
        tryParseInt(t[2][1], IDsList)
    elif id1[1] != "Int":
        print("Erro de operação: %s deve ser do tipo Int" % id1[0])
    if id2 == None:
        tryParseInt(t[3][1], IDsList)
    elif id2[1] != "Int":
        print("Erro de operação: %s deve ser do tipo Int" % id2[0])


def manipulaComp( t, IDsList ):
    if t[2][0] == 'expNot':
        id1 = getId(t[2][2][1], IDsList)
    elif t[2][0] == 'op':
        manipulaOp(t[2], IDsList)
        id1 = (0, 'Int')
    else:
        id1 = getId(t[2][1], IDsList)
    if t[3][0] == 'expNot':
        id2 = getId(t[3][2][1], IDsList)
    elif t[3][0] == 'op':
        manipulaOp(t[3], IDsList)
        id2 = (0, 'Int')
    else:
        id2 = getId(t[3][1], IDsList)

    if id1 == None:
        if type(tryConvertInt(t[2][1])) != int:
            print("Erro de declaração: %s não foi declarado" % t[2][1])
        id1 = (str(tryConvertInt(t[2][1])), 'Int')
    if id2 == None:
        if type(tryConvertInt(t[3][1])) != int:
            print("Erro de declaração: %s não foi declarado" % t[3][1])
        id2 = (str(tryConvertInt(t[3][1])), 'Int')
    if id1[1] != id2[1]:
        print("Erro de comparação: %s %s devem ser do mesmo tipo" % id1[0], id2[0])


def manipulaExprNew( t, TypeList ):
    if not isInListType(t[2], TypeList):
        print("Erro de declaração: tipo %s não foi declarado" % t[2])


def manipulaExprVoid( t, IDsList ):
    if not isInListId(t[2], IDsList):
        print("Erro de declaração: %s não foi declarado" % t[2])


def manipulaExprNot( t, IDsList ):
    if t[2][0] == 'comp':
        manipulaComp(t[2], IDsList)
        return
    print("Erro de declaração: expressão %s não é booleano" % t[2])


def manipulaFormal( t, IDsList, TypeList ):
    if isInListId(t[1], IDsList):
        print("Erro de declaração: %s já declarado" % t[1])
    if not isInListType(t[2], TypeList):
        print("Erro de declaração: tipo %s não foi declarado" % t[2])
    IDsList.append((t[1], t[2]))


def manipulaFeatureRetornoParametro( t, IDsList, MethodsList, TypeList ):
    if isInListMetodo(t[1], MethodsList):
        print("Erro de declaração: method %s já declarado" % t[1])
    if not isInListType(t[3], TypeList):
        print("Erro de declaração: tipo %s não foi declarado" % t[3])
    verificaParametro(t[2], TypeList)
    method = (t[1], [], t[3])
    tipo = getType(scope, TypeList)
    if tipo != None:
        tipo[2].append(method)
    for id in t[2]:
        newId = (id[1], id[2])
        IDsList.append(newId)
        method[1].append(newId)
    MethodsList.append(method)


def manipulaFeatureRetorno( t, MethodList, TypeList ):
    if isInListMetodo(t[1], MethodList):
        print("Erro de declaração: method %s já declarado" % t[1])
    if not isInListType(t[2], TypeList):
        print("Erro de declaração: tipo %s não foi declarado" % t[2])
    method = (t[1], [], t[2])
    tipo = getType(scope, TypeList)
    if tipo != None:
        tipo[2].append(method)
    MethodList.append(method)


def manipulafeatureAnonima( t, IDsList, TypeList ):
    if isInListId(t[1], IDsList):
        print("Erro de declaração: variavel %s já declarada" % t[1])
    if not isInListType(t[2], TypeList):
        print("Erro de declaração: tipo %s não foi declarado" % t[2])
    if t[2] == 'String':
        if type(t[3][1]) != str:
            print("Erro de declaração: valor incompativel com a variavel %s" % t[1])
    if t[2] == 'Int':
        if type(t[3][1]) != int:
            print("Erro de declaração: valor incompativel com a variavel %s" % t[1])

    IDsList.append((t[1], t[2]))


def manipulaFeatureDeclaration( t, IDsList, TypeList ):
    if isInListId(t[1], IDsList):
        print("Erro de declaração: variavel %s já declarada" % t[1])
    if not isInListType(t[2], TypeList):
        print("Erro de declaração: tipo %s não foi declarado" % t[2])
    IDsList.append((t[1], t[2]))


def manipulaClasseInh( t, TypeList ):
    inherits = getType(t[2], TypeList)
    classe = getType(t[1], TypeList)
    if inherits == None:
        print("Tipo '%s' não declarado" % t[2])
    else:
        for method in inherits[2]:
            classe[2].append(method)
        for id in inherits[3]:
            classe[3].append(id)


def isInListType( item, lista ):
    for i in lista:
        if item == i[0]:
            return True
    return False


def isInListId( item, lista ):
    for i in lista:
        if item == i[0]:
            return True
    return False


def getId( nome, lista ):
    for item in lista:
        if item[0] == nome:
            return item
    return None


def tryParseInt( valor, IDsList ):
    try:
        valor = int(valor)
    except:
        if isInListId(valor, IDsList):
            tipo = getId(valor, IDsList)[1]
            if tipo == 'Int':
                return
        print(f'Erro de conversão: {valor} não é do tipo inteiro')


def tryConvertInt( s ):
    try:
        return int(s)
    except:
        return s


def isInListMetodo( metodo, lista ):
    for i in lista:
        if metodo == i[0]:
            return True
    return False


def verificaParametro( parametros, TypeList ):
    idsParametros = []
    for parametro in parametros:
        if not isInListType(parametro[2], TypeList):
            print("Erro de declaração: tipo %s não foi declarado" % parametro[2])
        if parametro[1] in idsParametros:
            print("Erro de declaração: id %s já utilizado por outro parametro" % parametro[1])
        idsParametros.append(parametro[1])


def verificaParametroCall( parametros, metodo, IDsList ):
    if parametros[0] == None:
        del (parametros[0])
    if len(parametros) != len(metodo[1]):
        print("Erro de chamada: metodo %s deve conter %d parametros" % metodo[0], len(metodo[1]))
    for i in range(0, len(parametros)):
        if not isInListId(parametros[i][1], IDsList):
            if metodo[1][i][1] == 'Int':
                tryParseInt(parametros[i][1], IDsList)
            elif metodo[1][i][1] != 'String':
                print(f'Erro de chamada: parametro {parametros[i][1]} de tipo incorreto')
            if parametros[i][0] != 'exprValores':
                print(f'Erro de chamada: id {parametros[i][1]} não foi declarado')
        else:
            parametro = getId(parametros[i][1], IDsList)
            if parametro[1] != metodo[1][i][1]:
                print("Erro de chamada: parametro %s de tipo incorreto" % parametros[i][1])


def getMetodo( nome, MethodList ):
    for method in MethodList:
        if nome == method[0]:
            return method
    return None


def getType( nome, TypeList ):
    for tipo in TypeList:
        if nome == tipo[0]:
            return tipo
    return None


def isNewScopeClass(s):
    return s == 'classInh' or s == 'class'


def isNewScopeMethod( s ):
    return s == 'featureRetornoParametro' or s == 'featureRetorno'


def isNewScopeLet( s ):
    return s == 'exprLetSeta' or s == 'exprLet'


def configSelfType( IDsList, MethodsList, TypeList ):
    selftype = getType('SELF_TYPE', TypeList)
    selftype[2].clear()
    selftype[3].clear()
    for metodo in MethodsList:
        selftype[2].append(metodo)
    for id in IDsList:
        selftype[3].append(id)


for filho in arvore[0]:
    if type(filho) == tuple:
        if isInListType(filho[1], TypeList):
            print("Erro de declaração: tipo %s já foi declarado" % filho[1])
        if filho[0] == 'class':
            TypeList.append((filho[1], None, [], []))
        elif filho[0] == 'classInh':
            TypeList.append((filho[1], filho[2], [], []))

for filho in arvore[0]:
    chamarFun(filho, IDsList, MethodsList, TypeList)


