import math

class Codificador():
    """Codifica arquivo."""

    def __init__(self):
        # Quantas caracteres/valores vai carregar por vez
        self.buffer_leitura = 500

    def codificar(self, arquivo, tipo, golomb_divisor = 0):
        """Codifica o arquivo com o tipo informado."""
        self.buffer_escrita = ''

        
        # Golomb - divisor deve ser potencia de 2 (2, 4, 8, 16,...)
        if tipo == 0:
            self.golomb_divisor = golomb_divisor
            self.logDivisor = int(math.log(self.golomb_divisor, 2))
            codificador = self._golomb
            codificador_final = self._trata_final_golomb
            extensao = '.golomb'
        # Elias-Gama
        # elif tipo == 1:
        #     codificador = self._elias_gamma
        #     codificador_final = self._trata_final_elias_gamma
        #     extensao = '.eliasgamma'
        # # Fibonacci
        # elif tipo == 2:
        #     self.sequenciaFibonacci = [1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233]
        #     codificador = self._fibonacci
        #     codificador_final = self._trata_final_fibonacci
        #     extensao = '.fibonacci'
        # # Unaria
        # elif tipo == 3:
        #     codificador = self._unaria
        #     codificador_final = self._trata_final_unaria
        #     extensao = '.unaria'
        # # Delta
        # elif tipo == 4:
        #     self.maiorValor = 0
        #     self.isPrimeiroValor = True
        #     self.valorAnterior = 0
        #     self.tabelaCalculo = []
        #     codificador = self._delta
        #     codificador_final = self._trata_final_delta
        #     extensao = '.delta'

        # Retira o caminho ate o arquivo e cria o arquivo saida no diretorio atual
        # print(arquivo)
        destino = arquivo[arquivo.rfind('/')+1:]
        # print("Here"+destino)
        destino = destino[destino.rfind('\\')+1:]
        # print("#"+destino)
        # Cria arquivo de saida. Se arquivo tiver extensao, substitui pela nova
        if destino.rfind('.') >= 0:
            self.arquivo_destino = open(''.join([destino[:destino.rfind('.')], extensao]), 'wb')
        else:
            self.arquivo_destino = open(''.join([destino, extensao]), 'wb')

        # Le arquivo que sera codificado
        # if tipo == 4:
        #     with open(arquivo, 'rb') as file:
        #     # Le a quantidade de caracteres pemitidas no buffer
        #         leitura = file.read(self.buffer_leitura)

        #         # Leitura esta em binario "b' Lorem ipsum..."
        #         while (leitura != b''):
        #             # Separa cada caracter para codificar (L, o, r, e, m ...)
        #             for caracter in leitura: # Caracter = valor inteiro do binario (1001 = 9)
        #                 # Caractere de L vira o inteiro 76
        #                 codificador(caracter, True)

        #             leitura = file.read(self.buffer_leitura)
        #     self._criar_cabecalho(tipo, golomb_divisor, self.maiorValor)
        #     file.close()
        # else:
        self._criar_cabecalho(tipo, golomb_divisor)
        
        # Le arquivo que sera codificado
        with open(arquivo, 'rb') as file:
            # Le a quantidade de caracteres pemitidas no buffer
            leitura = file.read(self.buffer_leitura)

            # Leitura esta em binario "b' Lorem ipsum..."
            while (leitura != b''):
                # Separa cada caracter para codificar (L, o, r, e, m ...)
                for caracter in leitura: # Caracter = valor inteiro do binario (1001 = 9)
                    # Caractere de L vira o inteiro 76
                    self.buffer_escrita += codificador(caracter)
                    self._escrever_arquivo()

                leitura = file.read(self.buffer_leitura)

            # Se sobrou valores no buffer (quando for menos de 8 bits)
            if self.buffer_escrita != '':
                self._escrever_arquivo(True, codificador_final)

        file.close()
        self.arquivo_destino.close()
        # print('Codificado com sucesso!')

    def _criar_cabecalho(self, tipo, golomb_divisor, maiorValorDelta = 0):
        # Primeiro byte, informa qual o tipo da codificacao
        self.buffer_escrita += str(bin(tipo)[2:]).zfill(8)
        # Segundo byte, informa o divisor do Golomb
        self.buffer_escrita += str(bin(golomb_divisor)[2:]).zfill(8)
        # Terceiro byte, informa o maior valor do Delta
        self.buffer_escrita += str(bin(maiorValorDelta)[2:]).zfill(8)

    def _escrever_arquivo(self, final = False, codificador_final = None):
        """Transforma os bits em byte e salva no arquivo"""
        # Monta conjuntos de 8 bits para transformar em byte e salvar
        while len(self.buffer_escrita) >= 8:
            ## Não achei uma forma de transformar o binário (string) direto para byte, por isso essas convercoes ##
            # Transformar binario em inteiro
            inteiro = int(self.buffer_escrita[:8], 2)
            # Transforma inteiro em byte
            byte = bytes([inteiro])

            self.arquivo_destino.write(byte)

            # Tira os 8 bits do buffer que foram salvos no arquivo
            self.buffer_escrita = self.buffer_escrita[8:]

        # Se for ultima parte do arquivo, trata para atingir 8 bits e salva
        if final:
            self.buffer_escrita = codificador_final()
            inteiro = int(self.buffer_escrita, 2)
            byte = bytes([inteiro])
            self.arquivo_destino.write(byte)

    def _int_para_str_binario(self, inteiro):
        # Transforma inteiro em binario no formado string
        return bin(inteiro)[2:].zfill(8) # Formato string com len = 8

    ################ CODIFICADORES ################
    # Recebe valor inteiro do binario e retorna binario codificado
    """
        Regra básicas de todos codificadores:
            - Todos recebem valor inteiro de 0 a 255 que representa um byte
            - Serão chamadas a cada byte existe no arquivo de leitura
            - Todos devem retornar binarios no formato String ('111001'), os
                quais serao adicionados no arquivo codificado

        Trata_final == Quando nao for possivel completar um byte inteiro com a
            ultima parte dos bits codificados, entao devera ser feito algum
            tratamento para preencher o byte ou na hora de decodificar pode
            dar algum problema

        Se for necessario utilizar o binario em vez do valor inteiro, pode ser
            utilizado o metodo "_int_para_str_binario" para receber o binario do
            valor inteiro em formato string (entrada: 10, retorno: '00001010')
    """

    # Golomb --> prefixo(unario) + 1 + sufixo(binario)
    def _golomb(self, valor):
        # Calcula o quociente
        quociente = int(valor / self.golomb_divisor)
        # Calcula o resto
        resto = bin(valor % self.golomb_divisor)[2:].zfill(self.logDivisor)
        # Retorna o valor codificado
        return '1'.zfill(quociente + 1) + str(resto)

    # Escreve o Golomb no buffer
    def _trata_final_golomb(self):
        return self.buffer_escrita.ljust(8, '0')

















    # def _elias_gamma(self, valor):
    #     # Por padrao nao codifica diretamente o zero (NULL na tabela ASCII)
    #     valor += 1
    #     # Descobre o valor da potencia (n)
    #     valorN = int(math.log(valor,2))
    #     # Encontra o resto
    #     resto = abs(valor - (2 ** valorN))
        
    #     # Valida se o valor recebido for 1 ou diferente
    #     if valor != 1:
    #         return "1".zfill(valorN + 1) + bin(resto) [2:].zfill(valorN)
    #     else:
    #         return "1"
         
    # def _trata_final_elias_gamma(self):
    #     return self.buffer_escrita.ljust(8, '0')

    # def _fibonacci(self, valor):
    #     # Exemplo valor = 60 -> 55 (fibonacci) -> pega resto -> 5 (fibonacci)
    #     # Comeca pelo maior e vai ate o menor ou ate atingir o valor objetivo
    #     # Pega o valor escolhido e subtrai do maior valor de fibonacci
    #     # Com o resto ele continua aplicando o fibonacci até chegar em zero
    #     resto = valor + 1
    #     pos = len(self.sequenciaFibonacci) - 1  # 11
    #     achouPrimeiroVal = False
    #     listaFinal = ["0","0","0","0","0","0","0","0","0","0","0","0"]
    #     # Faz o for do maior para o menor elemento
    #     for valSeq in reversed(self.sequenciaFibonacci):
    #         if resto >= valSeq:
    #           resto = resto - valSeq
    #           # Atualiza as pos com 1 caso o elemento do fibonacci tenha sido usado
    #           listaFinal[pos] = "1"
    #           achouPrimeiroVal = True
    #         elif not achouPrimeiroVal:
    #             # Deleta os elementos do fibonacci que sao maiores que o valor
    #             del(listaFinal[pos])
    #         if resto == 0:
    #             # Retorna a listaFinal com o Stop Bit 1 no final
    #             return "".join(listaFinal) + "1"

    #         # Desloca uma posicao para frente no fibonacci.
    #         pos -= 1

    # def _trata_final_fibonacci(self):
    #     return self.buffer_escrita.ljust(8, '0')

    # def _unaria(self, valor):
    #     return '1'.zfill(valor+1)

    # def _trata_final_unaria(self):
    #     return self.buffer_escrita.ljust(8, '0')

    # def _delta(self, valor, contador = False):
    #     # Procurar no arquivo o maior tamanho de valor para representar em binarios. Faz uma leitura a mais do arquivo
    #     if contador:
    #         if valor > self.maiorValor:
    #             self.maiorValor = valor 
    #     else:
    #         # 120 maior valor ->  6 bits, vai gravar 7 bits(negativo ou positivo) exceção no primeiro (6)
    #         # diferenca entre ele e o anterior
    #         # pega em binario index - 1 para montar tabela de calculo
    #         # calcula o valor diferenca
    #         if not self.isPrimeiroValor:
    #             valorDiferenca = valor - self.valorAnterior
    #             if valorDiferenca > 0:
    #                 resposta = "10" + self.tabelaCalculo[valorDiferenca]
    #             elif valorDiferenca < 0:
    #                 resposta =  "11" + self.tabelaCalculo[abs(valorDiferenca)]
    #             else:
    #                 resposta =  "0"
    #         else:
    #             # Pega o tamanho do self.maiorValor tirando todos os zeros da esquerda.
    #             tamanhoInicio = len(self._int_para_str_binario(self.maiorValor).lstrip("0"))
    #             # Monta a tabela de calculo binario do delta
    #             for val in range(self.maiorValor + 1):
    #                 # Index 0 equivale a 1, index 1 equivale a  2...
    #                 # Adiciona na lista o valor binario tirando os valores extras iniciais desnecessarios no byte
    #                 self.tabelaCalculo.append(self._int_para_str_binario(val)[-(tamanhoInicio):])
    #             self.isPrimeiroValor = False
    #             # Resposta recebe o valor em binario sem os valores extras iniciais
    #             resposta = self._int_para_str_binario(valor)[-(tamanhoInicio):]

    #         self.valorAnterior = valor
    #         return resposta

    # def _trata_final_delta(self):
    #     return self.buffer_escrita.ljust(8, '1')