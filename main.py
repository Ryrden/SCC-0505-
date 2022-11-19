'''
============================================
O simulador foi desenvolvido para atender a 
atividade 1 proposta na disciplina de ITC 
(Introdução à Teoria da Computação) do curso
de Sistemas de Informação no ICMC - USP.

Seus integrantes são:

Eduardo Costa Miranda Azevedo     - 12677151
Gustavo de Oliveira Martins       - 12625531
Ivan Barbosa Pinheiro             -  9050552
Raquel de Jesus Santos Valadão    - 12674022
Ryan Souza Sá Teles               - 12822062
============================================
'''

from tkinter import Tk
from tkinter.filedialog import askopenfilename
from datetime import datetime
import os

class Automato():
  
  def __init__(self, estados, simbolosTerminais, estadosDeAceitacao):
    '''
      Método construtor da classe Automato.
      Recebe uma lista de estados, uma lista de símbolos terminais e uma lista de estados de aceitação.
      Por fim retorna uma instância do objeto automato.
    '''
    self.estados = estados
    self.simbolosTerminais = simbolosTerminais
    self.estadosDeAceitacao = estadosDeAceitacao
    

  
  def isDeterministico(self):
    '''
      Método que verifica com base nas transições dos estados se o automato é determinístico.
      Recebe o objeto automato e verifica se há duplicidade de transições com o mesmo simbolo terminal.
      Por fim retorna True se for determinístico ou False se for não determinístico.
    '''
    for estado in self.estados:
      todosEstados = ""
      for possivel in estado:
        todosEstados += possivel[0]
      for simbolo in self.simbolosTerminais:
        if(todosEstados.count(simbolo) > 1):
          return False
    return True

  
    
  def converteNaoDeterministicoEmDeterministico(self):
    '''
      Método que converte um automato não determinístico em um determinístico.
      Recebe o objeto automato e cria novos estados para remover a duplicidade de transições com os mesmos símbolos terminais.
      Por fim altera os estados do objeto automato passado para a nova lista de estados criada.
    '''
    if self.isDeterministico():
        return

    buffer = []
    quantidadeDeEstadosNoInicio = len(self.estados)
    for estado in self.estados:
      todasTransicoes = ""
      for possivel in estado:
        todasTransicoes += possivel[0]
      for simbolo in self.simbolosTerminais:
        if(todasTransicoes.count(simbolo) > 1):
          possiveisCaminho = ""
          for transicao in estado:
            if simbolo in transicao:
              if int(transicao[1]) >= quantidadeDeEstadosNoInicio:
                for buscaBuffer in buffer:
                  if str(transicao[1]) == str(buscaBuffer[0]):
                    for elementoBuscaBuffer in buscaBuffer[1]:
                      if elementoBuscaBuffer not in possiveisCaminho:
                        possiveisCaminho += elementoBuscaBuffer
              elif transicao[1] not in possiveisCaminho:
                possiveisCaminho += transicao[1]
          if len(possiveisCaminho) == 1:
            continue
          possiveisCaminho = "".join(sorted(possiveisCaminho))
          posicaoNovoEstado = isInBuffer(buffer, possiveisCaminho)
          if(posicaoNovoEstado == -1):
            posicaoNovoEstado = len(self.estados)
            buffer.append([posicaoNovoEstado,possiveisCaminho])
            transicoesNovoEstado = []
            for possivelCaminho in possiveisCaminho:
              for indexDeEstado in self.estados[int(possivelCaminho)]:
                transicoesNovoEstado.append(indexDeEstado)
            self.estados.append(transicoesNovoEstado)
            if posicaoNovoEstado not in self.estadosDeAceitacao:
              for estadoDeAceitacao in self.estadosDeAceitacao:
                if str(estadoDeAceitacao) in possiveisCaminho:
                  self.estadosDeAceitacao.append(posicaoNovoEstado)

          indexT = 0
          while indexT < len(estado):
            if estado[indexT][0] == simbolo:
              del(estado[indexT])
            else:
              indexT += 1
              
          estado.append([simbolo,str(posicaoNovoEstado)])

    self.limparTransacoesEEstadosDeAceitacaoRepetidos()
    print()
    print("-"*50)
    print("----- AUTOMATO CONVERTIDO EM DETERMINISTICO! -----")
    self.imprimirAutomato()


  
  def limparTransacoesEEstadosDeAceitacaoRepetidos(self):
    '''
      Método que remove transições de estados que estejam repetidas.
      EXEMPLO: ([["a","2"],["a","2"],["b","1"]] == [["a","2"],["b","1"]])
      E que também remove estados de aceitação repetidos.
      EXEMPLO: ([2,4,5,5,6,6] = [2,4,5,6]).
      Isso deve ser feito pois pode haver duplicidade de dados na inserção do arquivo .txt ou podem
      ser gerados no processo de transformação do automato de não determinístico para determinístico.
      Recebe o objeto automato e cria novos estados para remover as transições e estados de aceitação repetidos.
      Por fim altera os estados criados e os estados de aceitação do objeto automato passado.
    '''
    novosEstados = []
    for estado in self.estados:
      listaNova = []
      for transicao in estado:
        adicionar = True
        for elemento in listaNova:
          if (transicaoEhIgualAElemento(transicao, elemento)):
            adicionar = False
        if adicionar:
          listaNova.append(transicao)
      
      novosEstados.append(listaNova[:])
    self.estados = novosEstados[:]
    novosEstadosFinais = []
    for estadoFinal in self.estadosDeAceitacao:
      if estadoFinal not in novosEstadosFinais:
        novosEstadosFinais.append(estadoFinal)
    self.estadosDeAceitacao = novosEstadosFinais[:]


  
  def imprimirAutomato(self):
    '''
      Método que imprime os atributos do automato
      Recebe o objeto automato.
      Por fim imprime os atributo do automato.
    '''
    print("-"*50)
    print("Estados :: ")
    for index, estado in enumerate(self.estados):
      print("q",index, estado)
    print("\nEstados de aceitação :: ")
    print(self.estadosDeAceitacao)
    print("\nSímbolos terminais :: ")
    print(self.simbolosTerminais)  
    print("-"*50)


  
  def processarAsCadeias(self, cadeias):
    '''
      Método que cria uma lista de aceitação com base em uma cadeia de símbolos terminais.
      Recebe o objeto automato e uma lista de cadeias de símbolos terminais.
      Por fim retorna uma lista contendo quais cadeias foram aceitas ou não pelo automato.
    '''
    self.limparTransacoesEEstadosDeAceitacaoRepetidos()
    self.converteNaoDeterministicoEmDeterministico()
    saidas = []
    for cadeia in cadeias:
      estadoAtual = 0
      if(cadeia[0] == "-") and (0 in self.estadosDeAceitacao):
        saidas.append('aceita')
        continue
      for transicao in cadeia:
        mudou = False
        for par_transicao_possivel in self.estados[estadoAtual]:
            if transicao in par_transicao_possivel:
                estadoAtual = int(par_transicao_possivel[1])
                mudou = True
        if not mudou:
          estadoAtual = -1
          break
      if(estadoAtual in self.estadosDeAceitacao):
          saidas.append('aceita')
      else:
          saidas.append('rejeita')
    return saidas



def isInBuffer(buffer, elemento):
  '''
    Função que verifica se um elemento está presente em uma lista passada.
    Recebe o buffer e o elemento que deseja procurar.
    Por fim retorna True se o elemento está na lista e False caso não esteja.
  '''
  if len(buffer) == 0:
    return -1
  for elementoDeBuffer in buffer:
    if elementoDeBuffer[1] == elemento:
      return elementoDeBuffer[0]
  return -1



def transicaoEhIgualAElemento(transicao, elemento):
  '''
   Verifica se o par de transicao no estado é igual ao par de transição criado na nova instância do estado criado. 
  '''
  return ((str(transicao[0]) == str(elemento[0])) and str(transicao[1]) == str(elemento[1]))



def lerCadeias(nomeArquivoEntrada):
  '''
    Função que lê de um arquivo e as adiciona em uma lista de cadeias de símbolos terminais.
    Recebe o nome de um arquivo e o abre.
    Por fim salva os dados das cadeias em uma lista e a retorna.
  '''
  arquivoEntrada = open(nomeArquivoEntrada, "r")
  for i in range(3):
    arquivoEntrada.readline()

  for i in range(int(arquivoEntrada.readline())):
      arquivoEntrada.readline()
    
  quantidadeDeCadeias = int(arquivoEntrada.readline())
  cadeias = []
  for i in range(quantidadeDeCadeias):
    if(i == quantidadeDeCadeias-1):
      cadeias.append((list(arquivoEntrada.readline())))
    else:
        cadeias.append((list(arquivoEntrada.readline()[:-1])))

  arquivoEntrada.close()
  return cadeias



def criarAutomatoPeloArquivo(nomeArquivoEntrada): 
  '''
    Função que lê as linhas de um arquivo e as transforma em dados fundamentais do automato.
    Recebe o nome de um arquivo e o abre.
    Por fim separa os dados em vetores e os salva em uma estancia da classe automato.
  '''
  arquivoEntrada = open(nomeArquivoEntrada, "r")
  nroEstados = int(arquivoEntrada.readline())
  estados = [list() for i in range(nroEstados)]
  simbolosTerminais = (arquivoEntrada.readline()).split()
  simbolosTerminais.pop(0)
  estadosDeAceitacao = [int(i) for i in arquivoEntrada.readline().split()]
  estadosDeAceitacao.pop(0)
  
  nroDeTransicoes = int(arquivoEntrada.readline())
  for i in range(nroDeTransicoes):
      origem, simboloTerminal, destino = arquivoEntrada.readline().split()
      estados[int(origem)].append([simboloTerminal, destino])
  arquivoEntrada.close()

  return Automato(estados, simbolosTerminais, estadosDeAceitacao)



def criarArquivoDeSaida(saidas):
  '''
    Função que recebe uma lista de resultados e as adiciona em uma lista em um arquivo de saída.
    Recebe uma lista de resultados.
    Por fim salva os dados em um arquivo de saída na pasta "saidas" como nome a data da execução.
  '''
  nomeArquivoSaida = datetime.now().strftime("saida_%Y-%m-%d_%H-%M-%S.txt")
  if not os.path.exists('saidas'):
    os.makedirs('saidas')
  
  with open("saidas/" + nomeArquivoSaida, "w") as f:
      for i in range(len(saidas)-1):
        f.write('{}\n'.format(saidas[i]))
      f.write('{}'.format(saidas[-1]))

  

def imprimirSaidasECadeias(cadeias, saidas):
  '''
    Função que recebe uma lista de cadeias e outra de resultados e as imprimem no terminal.
    Recebe uma lista de cadeias e outra de resultados.
    Por fim as imprimem no terminal.
  '''
  print()
  print("-"*40)
  print("---------- SAIDAS DAS CADEIAS ----------")
  print("-"*40)
  for index, cadeia in enumerate(cadeias):
    if saidas[index] == "aceita":
      alinhador = " "
    else:
      alinhador = ""
    print(index, " ->  ", saidas[index].capitalize(), alinhador, "-> ", "".join(cadeia))
  print("-"*40)

  
def main():
  try:
    Tk().withdraw()
    nomeArquivoEntrada = askopenfilename() 
    automato = criarAutomatoPeloArquivo(nomeArquivoEntrada)
    cadeias = lerCadeias(nomeArquivoEntrada)
    automato.imprimirAutomato()
    saidas = automato.processarAsCadeias(cadeias)
    criarArquivoDeSaida(saidas)
    imprimirSaidasECadeias(cadeias, saidas)
  except:
    print("Arquivo de entrada inválido!")

if __name__ == "__main__":
    main()