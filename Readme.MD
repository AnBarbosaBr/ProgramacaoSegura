# SQL Injection
Esse projeto foi realizados para a aula de Programação Segura. O objetivo era determinar a senha do usuário "jake" no site: http://sqlzoo.net/hack/, mais especificamente na área de logon vulnerável: http://sqlzoo.net/hack/passwd.pl.


## SQLZoo/Hack
É uma seção do site SQLZoo que serve para orientar os desenvolvedores sobre como ocorre um ataque do tipo Injeção de SQL e algumas formas de prevenção.

## Sistema Utilizado:
### hack.sh
Prototipo de um sistema de acesso automatizado para fazer diversas "perguntas" através do formulário. Foi melhorado e transformado no sqlInjection.py.

### sqlInjection.py
Script capaz de automatizar queries sobre o sistema. 

Possui a função makeQuestionAboutPassword(str). Essa função cria os parâmetros que serão utilizados por um request de forma a "perguntar" ao DB se a senha de Jake se parece com o argumento, segundo a sintaxe do SQL.

Na função obtemLetrasDaSenha é verificado quais letras estão incluídas na senha de Jake, através de sucessivos questionamentos.

Sabendo as letras, executamos queryes para identificar os pares de letras que estão encadeadas.

De posse dos pares de letras, utilizamos busca em profundidade para obter a senha correta.


## To Do
- Refatorar o código, talvez dividindo-o em arquivos diferentes.
- Criar funções para explorar outras vulnerabilidades do site(como descobrir o nome de outros usuários, por exemplo, e descobrir caracteristicas do esquema do banco de dados)


## Outras Considerações
util.py foi obtido do repositório de AI, que contém exercícios da berkeley para ensino de inteligência artificial: http://ai.berkeley.edu.