import ply.lex as lex

class MyLexer(object):
	reserved={
	'class':'class'
	}

	tokens=[
		'ID',
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
		'traco'
	] + list(reserved.values())

	t_mais = r'\+'
	t_menos= r'\-'
	t_multi= r'\*'
	t_dividir= r'\/'
	t_igual= r'\='
	t_menor_igual = r'\<\='
	t_menor= r'\<'
	t_dois_pontos= r'\:'
	t_ponto_virgula= r'\;'
	t_abre_par= r'\('
	t_fecha_par= r'\)'
	t_abre_chaves= r'\{'
	t_fecha_chaves= r'\}'
	t_seta = r'\<\-'
	t_traco = r'\-'
	
	def t_ID(self, t):
		r'[a-zA-Z_][a-zA-Z_0-9]*'
		#checando palavras reservadas
		t.type = self.reserved.get(t.value.lower(),'ID')
		return t
	
	def t_number(self,t):
		r'\d+'
		t.value =int(t.value)
		return t
	
	#numero de linhas
	def t_newline(self,t):
		r'\n+'
		t.lexer.lineNum +=len(t.value)
	
	t_ignore =' \t'
	
	#caracter invalido
	def t_error(self,t):
		print("Caracter invalido"'%s'% t.value[0])
		t.lexer.skip(1)
	
	#criando o lexer
	def build(self, **kwargs):
		self.lexer= lex.lex(module=self, **kwargs)
	
	def test(self,data):
		self.lexer.input(data)
		while True:
			newtok = func(tok)
			tok=self.lexer.token()
			if not tok:
				break
			print(tok)

m= MyLexer()
m.build()
m.test(
"""	
class Main inherits IO {
    main(): Object {
        let hello: String <- "Hello, ",
            name: String <- "",
            ending: String <- "!\n"
        in {
            out_string("Please enter your name:\n");
            name <- in_string();
            out_string(hello.concat(name.concat(ending)));
        }
    };
};
"""
)
	
