from Sintatico import arvore
import copy

#lista de tipos organizadas de forma (<nome>, <de quem herda>, <metodos>, <IDs(?)>)
typeList = [('Object', None, [('abort', [], 'Object'), ('type_name', [], 'String'), ('copy', [], 'SELF_TYPE')], []),
        ('SELF_TYPE', None, [], []),
        ('IO', 'Object', [('out_string', [('x', 'String')], 'SELF_TYPE'), ('out_int', [('x', 'Int')], 'SELF_TYPE'), ('in_string', [], 'String'), ('in_int', [], 'Int')], []),
        ('Int', 'IO', [], []),
        ('String', 'IO', [('length', [], 'Int'), ('concat', [('s', 'String')], 'String'), ('substr', [('i', 'Int'), ('l', 'Int')], 'String')], []),
        ('Bool', 'IO', [], [])]
methodsList = []
idsList = []

scope = 'program'

for Type in typeList:
    for method in Type[2]:
        methodsList.append(method)
    for ID in Type[3]:
       idsList.append(ID)

#Corre a arvore semântica, caso ache filho, percorre como se fosse outra árvore
def percorrerArv(t):
    if type(t) == list or type(t) == tuple:
        for son in t:
            percorrerArv(son)
        print(t[0])

def chamarFun(t, idsList, methodsList, typeList):
    if t == None:
        return

    newTypesList = []
    newIDsList = []
    newMethodsList =[]
    newTypeList = typeList

    if isNewScopeClass(t[0]):
        global scope
        scope = t[1]
        newMethodsList = copy.deepcopy(methodsList)
        newIDsList = idsList
    elif isNewScopeMethod(t[0]) or isNewScopeLet(t[0]):
        newIDsList = copy.deepcopy(idsList)
        newMethodsList = methodsList

    else:
        newTypeList = typeList
        newIDsList = idsList
        newMethodsList = methodsList

