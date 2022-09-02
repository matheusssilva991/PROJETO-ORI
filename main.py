class arquivo():
    def __init__(self, nomeArquivo): # Construtor da classe
        self.__nomeArquivo = nomeArquivo
        self.__listaPalavras = []
        self.__listaPalavrasDesconsideradas = []
    # Fim do metodo construtor
    # Metodos getter --------------------------------------
    def getNomeArquivo(self):
        return self.__nomeArquivo

    def getListaPalavrasDesconsideradas(self):
        return self.__listaPalavrasDesconsideradas

    def getListaPalavras(self):
        return self.__listaPalavras
    # Fim dos metodos getter ------------------------------

  #Trata as palavras descondideradas
    def make_disconsidered_words(self, nomeArquivoDesconsideradas):
        with open(nomeArquivoDesconsideradas, 'r') as file:
            for linha in file:
                linha = linha.replace('\n', '')
              #Salva na lista de palavras desconsideradas
                self.__listaPalavrasDesconsideradas.append(linha)
      # end of method make_disconsidered_words

    #Preenche a lista de palavras         
    def make_words_file(self, disconsidered):
        separadores = ['!', '?', ',', '.']

        if disconsidered != None:
            self.make_disconsidered_words(disconsidered)

        with open(self.getNomeArquivo(), 'r') as file:
            for linha in file:
                palavras = []

                linha = linha.replace('\n', '') 
                for separador in separadores:
                    linha = linha.replace(separador, '')#Troca por espaço em branco
                  
                palavras = linha.split(' ') # separa as palavras por espaço
                for palavra in palavras:
                    if self.__listaPalavrasDesconsideradas == []:
                        self.__listaPalavras.append(palavra)
                    elif palavra not in self.__listaPalavrasDesconsideradas:
                        self.__listaPalavras.append(palavra)
    # end of method make_words_file
# end of class arquivo

#Cria os objetos Arquivos para cada arquivo do conjunto
def make_files(conjunto, desconsideradas = None):
    
    arquivos = []
    
    with open(conjunto, 'r') as file:
        ponteiroArquivo = 0
        for nomeArquivo in file:
            arquivos.append(arquivo(nomeArquivo.replace('\n', '')))
            arquivos[ponteiroArquivo].make_words_file(desconsideradas.replace('\n', ''))
            ponteiroArquivo += 1
            
    return arquivos #retorna a lista dos objetos
# end of method make_files

#Criadora do arquivo de índices
def make_index(arquivos):
    #União com palavras únicas de cada arquivo
    palavras = list(set(arquivos[0].getListaPalavras()) | set(arquivos[1].getListaPalavras()) | set(arquivos[2].getListaPalavras()))
    palavras.sort() #Ordena

    with open("indice.txt", "w") as file: #Criação do arquivo de índices
        for palavra in palavras:
            linha = f"{palavra}: "
           #Em cada iteração verica em qual arquivo contém a palavra
          # e a quantidade de vezes que essa palavra ela se repete
            for i in range(3):
                if palavra in arquivos[i].getListaPalavras():
                    linha += f"{i + 1},{arquivos[i].getListaPalavras().count(palavra)} "
            linha = linha.rstrip()
            file.write(linha+"\n")

# end of method make_index

#Retorna como dicionário as linhas que contém as palavras de consulta
def make_dict_index(lista_consulta):
    dicionario_index = {}

    with open('indice.txt', 'r') as file:       
        for linha in file:
            linha_aux = linha.split(' ', 1)
            linha_aux[1] = linha_aux[1].replace('\n', '')
            linha_aux[0] = linha_aux[0].replace(':', '')
            if (len(lista_consulta) == 1):
                if lista_consulta[0] == linha_aux[0]:
                    dicionario_index[linha_aux[0]] = linha_aux[1].replace('\n', '')
            elif (len(lista_consulta) > 1):
                if ((lista_consulta[0] == linha_aux[0]) or (lista_consulta[1] == linha_aux[0])): 
                    dicionario_index[linha_aux[0]] = linha_aux[1].replace('\n', '')
    return dicionario_index
# end of method make_dict_index

#Faz a consulta no arquivo consulta.txt
def get_answer(arquivo_consulta):
    consulta = None
    
    with open(arquivo_consulta.replace('\n', ''), 'r') as file:
        for linha in file:
            consulta = linha.replace('\n', '')

    if ',' in consulta: #retorna and 
        operador = ','
        lista_consulta = consulta.split(operador)
        dict = make_dict_index(lista_consulta)
        return dict[lista_consulta[0]] and dict[lista_consulta[1]]  
    elif ';' in consulta: #retorna união dos valores
        operador = ';'
        lista_consulta = consulta.split(operador)
        dict = make_dict_index(lista_consulta)
        return dict[lista_consulta[0]] + " " + dict[lista_consulta[1]]  
    else: # retorna apenas o valor do dicionário que contém a palavra consulta
        operador = ' '
        lista_consulta = consulta.split(operador)
        dict = make_dict_index(lista_consulta)
        return dict[lista_consulta[0]]
# end of method get_answer

#Cria o arquivo de resposta
def make_answer(arquivos, index_arquivos):
    indexes = index_arquivos.split(' ')
    for i in range(len(indexes)):
        aux = indexes[i].split(',')
        indexes[i] = aux[0]
#Escreve no arquivo resposta os índices dos arquivos que contém as palavras da consulta
    with open("resposta.txt", 'w') as file:
        file.write(str(len(indexes))+"\n")
        for i in indexes:
            file.write(arquivos[int(i) - 1].getNomeArquivo()+"\n")
# end of method make_answer  

def main():
    #entradas = input().split(" ")
    entradas = ["conjunto.txt", 'desconsideradas.txt', 'consulta.txt']
    arquivos = make_files(entradas[0], entradas[1])
    arquivo_consulta = entradas[2]
    make_index(arquivos)
    index_arquivos = get_answer(arquivo_consulta)
    make_answer(arquivos, index_arquivos)
# end of method main
main()