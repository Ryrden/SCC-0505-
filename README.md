Simulador Universal de Autômatos Finitos
===============


O simulador foi desenvolvido para atender a atividade 1 proposta na disciplina de ITC (Introdução à Teoria da Computação).

Seus integrantes são:
```
Eduardo Costa Miranda Azevedo - 12677151
Gustavo de Oliveira Martins - 12625531
Ivan Barbosa Pinheiro - 9050552
Raquel de Jesus Santos Valadão - 12674022
Ryan Souza Sá Teles - 12822062
```

Instalação e Execução
----------

A instalação é bem simples, basta ter o Python instalado em sua máquina, caso não tenha siga o tutorial conforme sua plataforma que pode ser encontrado acessando este link https://www.python.org/, com o Python instalado basta baixar o arquivo "main.py" e executá-lo conforme sua plataforma.

Como usar
-----

Digamos que você tenha o seguinte autômato e você queira verificar algumas cadeias de símbolos terminais:

![alt Autômato](https://i.imgur.com/yeDN2CQ.png)

Para definir este autômato e realizar estas verificações é bem simples, você deve criar um arquivo texto que siga o modelo abaixo:

```py
3
2 a b
1 2
6
0 a 1
0 b 1
1 a 1
1 b 2
2 a 0
2 b 2
10
abbbba
aabbbb
bbabbabbabbb
bbbbbbbbbbb
-
abababababab
bbbbaabbbb
abba
a
aaa
```

Não entendeu? Segue a definição de cada campo para facilitar:

```py
3             <- Quantidade estados
2 a b         <- Quantidade de simbolos terminais seguido deles
1 2           <- Quantidade de estados de aceitações seguido deles
6             <- Quantidade de transições
0 a 1         <- Transição 1 (q0 --a--> q1)
0 b 1         <- Transição 2 (q0 --b--> q1)
1 a 1         <- Transição 3 (q1 --a--> q1)
1 b 2         <- Transição 4 (q1 --b--> q2)
2 a 0         <- Transição 5 (q2 --a--> q0)
2 b 2         <- Transição 6 (q2 --b--> q2)
10            <- Quantidade de cadeias a serem verificadas
abbbba        <- Cadeia 1
aabbbb        <- Cadeia 2
bbabbabbabbb  <- Cadeia 3
bbbbbbbbbbb   <- Cadeia 4
-             <- Cadeia 5 (Representação da cadeia nula)
abababababab  <- Cadeia 6
bbbbaabbbb    <- Cadeia 7
abba          <- Cadeia 8
a             <- Cadeia 9
aaa           <- Cadeia 10
```

No diretório  "Casos de Teste" já existem alguns exemplos(inclusive o exemplo acima seria o "in0.txt".

Após a criação deste documento de texto você deve executar o programa "main.py" (no nosso caso utilizamos um ambiente linux, então o comando é "python3 main.py", mas pode variar dependendo de seu sistema operacional)

Ao abrir uma tela de solicitação de arquivo, selecione o arquivo que deseja verificar.

Caso o arquivo seja válido e esteja no modelo correto, ele interpretará as cadeias e criará um arquivo de saída dentro de uma pasta que será criada chamada "saidas" (como por exemplo a saída do "in0.txt").

```
rejeita
aceita
aceita
aceita
rejeita
rejeita
aceita
rejeita
rejeita
rejeita
```