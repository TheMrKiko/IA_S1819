from nome import *
from utilities.search import (Problem)
from importlib import *
import os
import sys
import io


################ FUNCOES A TESTAR #############
funcoes_a_testar = ('faz_pos', 'linha_pos', 'coluna_pos', 'e_pos', 'pos_iguais',
                    'gera_chave_linhas', 'gera_chave_espiral',
                    'ref_chave', 'muda_chave', 'e_chave', 'string_chave',
                    'digramas', 'figura', 
                    'codifica_l', 'codifica_c', 'codifica_r',
                    'codifica_digrama', 'codifica')


################ OBTEM LISTA DE FICHEIROS DE TESTES #############
nome_directoria_testes = 'Testes Publicos/'
dir_testes = os.listdir(path = nome_directoria_testes)
# guarda so os ficheiros .in
#dir_testes = [f[: -3] for f in dir_testes if f[len(f) - 3 : ] == '.in']

########################## compara_chaves
def compara_chaves(chave1, chave2):
    """ chave1 obtida pela funcao_gera_chave(linhas ou espiral)
    chave2 lista de listas """
    for l in range(5):
        for c  in range(5):
            if ref_chave(chave1, faz_pos(l, c)) != chave2[l][c]:
                return False
    return True
########################## aplica_testes
def aplica_testes():
    for nome_teste in dir_testes:
        #funcao testada pelo teste
        #nome_funcao = extrai_nome_funcao(nome_teste)
        #if nome_funcao in funcoes_a_testar:
        print('*******************', nome_teste, '*******************')
        fich_in = open(nome_directoria_testes + nome_teste + '/input', 'r')
        fich_out = open(nome_directoria_testes + nome_teste + '/output', 'r')
        
        cont_fich_in = fich_in.readlines()
        # res eh o resultado esperado (conteudo do fich.out)
        res = fich_out.readlines()[0][ : -1] #tira \n
        # var_res eh a variavel cujo conteudo deve ser comparado
        # com o resultado esperado (ultima linha do fich.in)
        var_res = cont_fich_in[-1][:-1]
        
        fich_in. close()
        fich_out. close()
        
        
        res_aplica_teste =   True
        old_stdout = sys.stdout # Memorize the default stdout stream
        sys.stdout = buffer = io.StringIO()

        #for linha in cont_fich_in[ : -1]:
            

        try:
            #exec(linha[:-1])
            eval(var_res) ##fazer print
        except ValueError:
            pass
        except:
            res_aplica_teste =   False                





        sys.stdout = old_stdout # Put the old stream back in place

        whatWasPrinted = buffer.getvalue() # Return a str containing the entire contents of the buffer.

        if res_aplica_teste and (e_erro(res) or (str(eval(res)) == whatWasPrinted[:-1])):
            print('PASSOU')
        else:
            print('FALHOU')
            print("Daria", eval(res))
            print("Deu", whatWasPrinted[:-1])
        print('\n')
            
def extrai_nome_funcao(nome_teste):
    i = 6
    nome_funcao = ''
    while nome_teste[i] != '-':
        nome_funcao = nome_funcao + nome_teste[i]
        i += 1
    return nome_funcao

def e_erro(res):
    return res[ : 5] == "'ERRO"


aplica_testes()
