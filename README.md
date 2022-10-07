# PROJETO ORI - Construção de Índice Invertido
Projeto desenvolvido na disciplina Organização e recuperação de informação

## Descrição
Esse trabalho consiste na criação de um programa de gerenciamento de índices para um conjunto de arquivos no contexto de um sistema de Recuperação da Informação.

## Entrada do programa
O programa recebe como entrada o nome de três arquivos.txt. O primeiro arquivo consiste em um arquivo de texto que contém o conjunto de arquivos que serão indexados.
O segundo arquivo especifica todas as palavras que serão desconsideradas dos arquivos do conjunto. O terceiro arquivo especifica as palavras que serão consultadas, sendo
separadas por "," para consultar os arquivos que tenham ambas as palavras e por ";" para consultar os arquivos que tenham uma ou ambas as palavras.

## Saida do programa
O programa tem como saída dois arquivos.txt, arquivo de indice, contendo todas as palavras únicas contidas nos arquivos e quais arquivos elas pertencem, e o arquivo resposta, que contém quantos arquivos possuem as palavras consultadas e em quais arquivos elas estão.