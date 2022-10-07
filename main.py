class arquivo():
    def __init__(self, nomeArquivo): # Construtor da classe
        self.__file_name = nomeArquivo
        self.__list_words = []
        self.__list_desconsidered_words = []
    # Fim do metodo construtor
    # Metodos getter --------------------------------------
    def get_file_name(self):
        return self.__file_name

    def get_list_desconsidered_words(self):
        return self.__list_desconsidered_words

    def get_list_words(self):
        return self.__list_words
    # Fim dos metodos getter ------------------------------

  #Trata as palavras descondideradas
    def make_disconsidered_words(self, nomeArquivoDesconsideradas):
        with open(nomeArquivoDesconsideradas, 'r') as file:
            for line in file:
                line = line.replace('\n', '')
              #Salva na lista de palavras desconsideradas
                self.__list_desconsidered_words.append(line)
      # end of method make_disconsidered_words

    #Preenche a lista de palavras         
    def make_words_file(self, disconsidered):
        separadores = ['!', '?', ',', '.']

        if disconsidered != None:
            self.make_disconsidered_words(disconsidered)

        with open(self.get_file_name(), 'r') as file:
            for line in file:
                words = []

                line = line.replace('\n', '') 
                for separador in separadores:
                    line = line.replace(separador, '')#Troca por espaço em branco
                  
                words = line.split(' ') # separa as palavras por espaço
                for word in words:
                    if self.__list_desconsidered_words == []:
                        self.__list_words.append(word)
                    elif word not in self.__list_desconsidered_words:
                        self.__list_words.append(word)
    # end of method make_words_file
# end of class arquivo

#Cria os objetos Arquivos para cada arquivo do conjunto
def make_files(conjunto, desconsideradas = None):
    
    files = []
    
    with open(conjunto, 'r') as file:
        ptr_file = 0
        for file_name in file:
            files.append(arquivo(file_name.replace('\n', '')))
            files[ptr_file].make_words_file(desconsideradas.replace('\n', ''))
            ptr_file += 1
            
    return files #retorna a lista dos objetos
# end of method make_files

#Criadora do arquivo de índices
def make_index(arquivos):
    #União com palavras únicas de cada arquivo
    words = list(set(arquivos[0].get_list_words()) | set(arquivos[1].get_list_words()) | set(arquivos[2].get_list_words()))
    words.sort() #Ordena

    with open("indice.txt", "w") as file: #Criação do arquivo de índices
        for word in words:
            line = f"{word}: "
           #Em cada iteração verica em qual arquivo contém a palavra
          # e a quantidade de vezes que essa palavra ela se repete
            for i in range(3):
                if word in arquivos[i].get_list_words():
                    line += f"{i + 1},{arquivos[i].get_list_words().count(word)} "
            line = line.rstrip()
            file.write(line+"\n")

# end of method make_index

#Retorna como dicionário as linhas que contém as palavras de consulta
def make_dict_index(lista_consulta):
    dicionary_index = {}

    with open('indice.txt', 'r') as file:       
        for line in file:
            line_aux = line.split(' ', 1)
            line_aux[1] = line_aux[1].replace('\n', '')
            line_aux[0] = line_aux[0].replace(':', '')
            if (len(lista_consulta) == 1):
                if lista_consulta[0] == line_aux[0]:
                    dicionary_index[line_aux[0]] = line_aux[1].replace('\n', '')
            elif (len(lista_consulta) > 1):
                if ((lista_consulta[0] == line_aux[0]) or (lista_consulta[1] == line_aux[0])): 
                    dicionary_index[line_aux[0]] = line_aux[1].replace('\n', '')
    return dicionary_index
# end of method make_dict_index

#Faz a consulta no arquivo consulta.txt
def get_answer(arquivo_consulta):
    consulta = None
    
    with open(arquivo_consulta.replace('\n', ''), 'r') as file:
        for line in file:
            consulta = line.replace('\n', '')

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
            file.write(arquivos[int(i) - 1].get_file_name()+"\n")
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