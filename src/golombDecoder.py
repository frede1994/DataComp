import math

class Decoder():
    """Decodes file."""

    def __init__(self):
        # Header byte size
        self.tamanho_cabecalho = 3

    def decode(self, arquivo, extensao_saida,result_path):
        """Decodes the reported file"""
        # To store header information
        self.cabecalho = []
        self.buffer_escrita = []

        # Create output file. If file has extension, replace it with the new one
        filename = arquivo[arquivo.rfind('/')+1:]
        outputfile =result_path+"/"+filename.split(".")[0]+extensao_saida

        if arquivo.rfind('.') >= 0:
            # self.arquivo_destino = open('.'.join([arquivo[:arquivo.rfind('.')], extensao_saida]), 'wb')
            self.arquivo_destino = open(outputfile, 'wb')

         # The file to be decoded
        with open(arquivo, 'rb') as file:
            self._ler_cabecalho(file)
            decodificador = self._identificar_tipo_codificador()

            # read byte by byte, interpreting each one
            leitura = file.read(1)
            while (leitura != b''):
                ## I didn't find a way to read the binary straight from the byte, so these conversions ##
                # Transforms byte into integer (1001 = 9)
                inteiro = int.from_bytes(leitura, 'big')
                # Transforms integer into binary into formed string
                binario = bin(inteiro)[2:].zfill(8) # String format with len = 8

                decodificador(binario)
                self._escrever_arquivo()

                leitura = file.read(1)

        file.close()
        self.arquivo_destino.close()

    def _ler_cabecalho(self, file):
        """Read and store headerinformation"""
        for i in range(self.tamanho_cabecalho):
            leitura = file.read(1)
            self.cabecalho.append(int.from_bytes(leitura, 'big'))

    def _identificar_tipo_codificador(self):
        """Read the first byte and identify which encoder was used"""
        # Golomb
        if  self.cabecalho[0] == 0:
            self._contadorPrefixo = 0
            self._contadorSufixo = 0
            self._logDivisor = int(math.log(self.cabecalho[1], 2))
            self._isPrefixo = True
            self._armazenaSufixo = ""
            return self._golomb

    def _escrever_arquivo(self):
        """Turns whole value into byte and saves it in the file"""
        while len(self.buffer_escrita) > 0:
            byte = bytes([self.buffer_escrita.pop(0)])
            self.arquivo_destino.write(byte)

    def _int_para_str_binario(self, inteiro):
        # Transforms integer into binary into formed string
        return bin(inteiro)[2:].zfill(8) # String format with len = 8

    ################ DECODERS #################
    # Receive binary (string) and store integer value (int) of binary
    """
        Basic rules of all decoders:
            - All receive 8 bits in string format
            - Each byte exists in the reading file (encoded) will be called
            - Everyone should save to the "self.buffer_escrita" list (using .append)
                the entire binary value every time any code is decoded
                character. This value will later be converted to byte and
                saved in the destination file
        If it is necessary to use a global variable, it can be created in the
            "_identify_type_coder" method using 'self.'
        If it is necessary to use the binary instead of the entire value, it can be
            the "_int_para_str_binario" method was used to receive the
            integer value in string format (input: 10, return: '00001010')
    """

    def _golomb(self, binario):
        
        # 1 ->  prefix, make counter prefix and get suffix
        for bit in binario:
            # Get prefix.
            if bit == '0' and self._isPrefixo:
                self._contadorPrefixo += 1
            # Stop Bit
            elif bit == '1' and self._isPrefixo:
                self._contadorSufixo = 0
                self._armazenaSufixo = ""
                self._isPrefixo = False
            # Get the suffix
            elif not self._isPrefixo and self._contadorSufixo < self._logDivisor:
                self._contadorSufixo += 1
                self._armazenaSufixo += bit
            # caught them both
            if not self._isPrefixo and self._contadorSufixo >= self._logDivisor:
                self._isPrefixo = True
                valorResposta = (self._contadorPrefixo * self.cabecalho[1]) + int(self._armazenaSufixo, 2)
                self._contadorPrefixo = 0
                self.buffer_escrita.append(valorResposta)

    def _unaria(self, binario):
        """Decodes the binary values ​​encoded as Unary"""
        for bit in binario:
            if bit == '0':
                self._unaria_contador += 1
            else:
                self.buffer_escrita.append(self._unaria_contador)
                self._unaria_contador = 0

    