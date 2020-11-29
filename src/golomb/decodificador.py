import math

class Decodificador():
    """Decodifica arquivo."""

    def __init__(self):
        # Tamanho de bytes do cabecalho
        self.tamanho_cabecalho = 3

    def decodificar(self, arquivo, extensao_saida='txt2'):
        """Decodifica o arquivo informado"""
        # Para armazenar as informacoes do cabecalho
        self.cabecalho = []
        self.buffer_escrita = []

        # Cria arquivo de saida. Se arquivo tiver extensao, substitui pela nova
        if arquivo.rfind('.') >= 0:
            self.arquivo_destino = open('.'.join([arquivo[:arquivo.rfind('.')], extensao_saida]), 'wb')
        else:
            self.arquivo_destino = open('.'.join([arquivo, extensao_saida]), 'wb')

        # Le arquivo que sera decodificado
        with open(arquivo, 'rb') as file:
            self._ler_cabecalho(file)
            decodificador = self._identificar_tipo_codificador()

            # Le byte por byte, interpretando cado um deles
            leitura = file.read(1)
            while (leitura != b''):
                ## Não achei uma forma de ler o binário direto do byte, por isso essas convercoes ##
                # Transforma byte em inteiro (1001 = 9)
                inteiro = int.from_bytes(leitura, 'big')
                # Transforma inteiro em binario no formado string
                binario = bin(inteiro)[2:].zfill(8) # Formato string com len = 8

                decodificador(binario)
                self._escrever_arquivo()

                leitura = file.read(1)

        file.close()
        self.arquivo_destino.close()
        # print('Decodificado com sucesso!')

    def _ler_cabecalho(self, file):
        """Le e armazena as informacoes do cabecalho"""
        for i in range(self.tamanho_cabecalho):
            leitura = file.read(1)
            self.cabecalho.append(int.from_bytes(leitura, 'big'))

    def _identificar_tipo_codificador(self):
        """Le o primeiro byte e identifica qual codificador foi utilizado"""
        # Golomb
        if self.cabecalho[0] == 0:
            self._contadorPrefixo = 0
            self._contadorSufixo = 0
            self._logDivisor = int(math.log(self.cabecalho[1], 2))
            self._isPrefixo = True
            self._armazenaSufixo = ""
            return self._golomb

        # # Elias-Gamma
        # elif self.cabecalho[0] == 1:
        #     self._contadorPrefixo = 0
        #     self._contadorSufixo = 0
        #     self._isPrefixo = True
        #     self._armazenaSufixo = ""
        #     return self._elias_gamma

        # # Fibonacci
        # elif self.cabecalho[0] == 2:
        #     self._sequenciaFibonacci = [1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233]
        #     self._sequenciaAtual = []
        #     return self._fibonacci

        # # Unaria
        # elif self.cabecalho[0] == 3:
        #     self._unaria_contador = 0
        #     return self._unaria

        # # Delta
        # elif self.cabecalho[0] == 4:
        #     self._isPrimeiroValor = True
        #     self._sequenciaAtual = ""
        #     self._valorAnterior = 0
        #     self._tamanhoInicio = 0 
        #     return self._delta

    def _escrever_arquivo(self):
        """Transforma valor inteiro em byte e salva no arquivo"""
        while len(self.buffer_escrita) > 0:
            byte = bytes([self.buffer_escrita.pop(0)])
            self.arquivo_destino.write(byte)

    def _int_para_str_binario(self, inteiro):
        # Transforma inteiro em binario no formado string
        return bin(inteiro)[2:].zfill(8) # Formato string com len = 8

    ################ DECODIFICADORES ################
    # Recebe binario (string) e armazena valor inteiro (int) do binario
    """
        Regra básicas de todos decodificadores:
            - Todos recebem 8 bits em formato string
            - Serão chamadas a cada byte existe no arquivo de leitura (codificado)
            - Todos devem salvar na lista "self.buffer_escrita" (usando .append)
                o valor inteiro do binario toda vez que for decodificado algum
                caracter. Esse valor posteriormente será convertido para byte e
                salvo no arquivo de destino

        Se for necessario utilizado alguma variavel global, pode ser criado no
            metodo "_identificar_tipo_codificador" utilizando 'self.'

        Se for necessario utilizar o binario em vez do valor inteiro, pode ser
            utilizado o metodo "_int_para_str_binario" para receber o binario do
            valor inteiro em formato string (entrada: 10, retorno: '00001010')
    """

    def _golomb(self, binario):
        
        # 1 -> le prefixo, faz contador prefixo e pega sufixo
        for bit in binario:
            # Pega prefixo.
            if bit == '0' and self._isPrefixo:
                self._contadorPrefixo += 1
            # Stop Bit
            elif bit == '1' and self._isPrefixo:
                self._contadorSufixo = 0
                self._armazenaSufixo = ""
                self._isPrefixo = False
            # Pega o sufixo
            elif not self._isPrefixo and self._contadorSufixo < self._logDivisor:
                self._contadorSufixo += 1
                self._armazenaSufixo += bit
            # Jah pegou os dois
            if not self._isPrefixo and self._contadorSufixo >= self._logDivisor:
                self._isPrefixo = True
                valorResposta = (self._contadorPrefixo * self.cabecalho[1]) + int(self._armazenaSufixo, 2)
                self._contadorPrefixo = 0
                self.buffer_escrita.append(valorResposta)

    # def _elias_gamma(self, binario):
    #     for bit in binario:
    #         # Pega prefixo
    #         if bit == '0' and self._isPrefixo:
    #             self._contadorPrefixo += 1
    #         # Stop Bit
    #         elif bit == '1' and self._isPrefixo:
    #             self._contadorSufixo = 0
    #             self._armazenaSufixo = ""
    #             self._isPrefixo = False
    #         # Pega o sufixo
    #         elif not self._isPrefixo and self._contadorSufixo < self._contadorPrefixo:
    #             self._contadorSufixo += 1
    #             self._armazenaSufixo += bit
    #         # Jah pegou os dois
    #         if not self._isPrefixo and self._contadorSufixo >= self._contadorPrefixo:
    #             self._isPrefixo = True
    #             if self._armazenaSufixo != "":
    #                 valorResposta = (2 ** self._contadorPrefixo + int(self._armazenaSufixo,2)) - 1
    #             else:
    #                 valorResposta = 0

    #             self._contadorPrefixo = 0
    #             self.buffer_escrita.append(valorResposta)

    # def _fibonacci(self, binario):
        
    #     # Verifica se tem dois 1s juntos e faz a separacao dos binarios
    #     for bit in binario:
    #         self._sequenciaAtual.append(bit)
    #         if len(self._sequenciaAtual) >= 2 and self._sequenciaAtual[-1] == "1" and self._sequenciaAtual[-2] == "1":
    #             val = 0
    #             del(self._sequenciaAtual[-1])
    #             for pos in range(len(self._sequenciaAtual)):
    #                 # Calcula os valores aplicando a sequencia de fibonacci
    #                 if self._sequenciaAtual[pos] == "1":
    #                     val += self._sequenciaFibonacci[pos]
    #             self.buffer_escrita.append(val - 1)
    #             self._sequenciaAtual.clear()

    def _unaria(self, binario):
        """Decodifica os valores binarios codificado como Unaria"""
        for bit in binario:
            if bit == '0':
                self._unaria_contador += 1
            else:
                self.buffer_escrita.append(self._unaria_contador)
                self._unaria_contador = 0

    # def _delta(self, binario):
    #     for bit in binario:
    #         self._sequenciaAtual += bit 
    #         # Pega os valores de toda a sequencia e calcula o valor deles
    #         if not self._isPrimeiroValor:
    #             # Pega os valores que nao sao iguais
    #             if len(self._sequenciaAtual) >= self._tamanhoInicio + 2:
    #                 # Pega o valor que eh positivo
    #                 if self._sequenciaAtual[1] == "0":
    #                     valor = int(self._sequenciaAtual[2:],2) + self._valorAnterior
    #                 # Pega o valor que eh negativo
    #                 else:
    #                     valor = abs(int(self._sequenciaAtual[2:],2) - self._valorAnterior)
    #                 self._valorAnterior = valor
    #                 self.buffer_escrita.append(self._valorAnterior)
    #                 self._sequenciaAtual = ""
    #             # Pega o valor que jah apareceu pois sao iguais
    #             elif len(self._sequenciaAtual) == 1 and self._sequenciaAtual[0] == "0":
    #                 self.buffer_escrita.append(self._valorAnterior)
    #                 self._sequenciaAtual = ""
    #         else:
    #             # Pega o primeiro valor e atualiza o self.valorAnterior para ser usado na sequencia
    #             if len(self._sequenciaAtual) == 1:
    #                 self._tamanhoInicio = len(self._int_para_str_binario(self.cabecalho[2]).lstrip("0"))
    #             if len(self._sequenciaAtual) >= self._tamanhoInicio:
    #                 self._isPrimeiroValor = False
    #                 self._valorAnterior = int(self._sequenciaAtual,2)
    #                 self.buffer_escrita.append(self._valorAnterior)
    #                 self._sequenciaAtual = ""