import math

class Encoder():
    """Encode file."""
    def __init__(self):
        # How many characters / values will load at a time
        self.buffer_read = 500

    def code(self, arquivo, tipo, result_path,golomb_divisor = 0):
        """Encode the file with the given type."""
        self.buffer_escrita = ''
        # Golomb - divisor must be power of 2 (2, 4, 8, 16, ...)
        if tipo == 0:
            self.golomb_divisor = golomb_divisor
            self.logDivisor = int(math.log(self.golomb_divisor, 2))
            codificador = self._golomb
            codificador_final = self._trata_final_golomb
            extensao = '.golomb'
    
        
        destino = arquivo[arquivo.rfind('\\')+1:] #CHANGED THIS FROM / TO \\ TO WORK
        filename = destino
        outputfile =result_path+"/"+filename.split(".")[0]+extensao
        destino = destino[destino.rfind('\\')+1:]
        # Create output file. If file has extension, replace it with the new one
        if destino.rfind('.') >= 0:
            self.arquivo_destino = open(outputfile, 'wb')

    
        self._criar_cabecalho(tipo, golomb_divisor)

       # The file to be encoded
        with open(arquivo, 'rb') as file:
            # Read the number of characters allowed in the buffer
            leitura = file.read(self.buffer_read)

            # Reading is in binary "b 'Lorem ipsum ..."
            while (leitura != b''):
              # Separates each character to encode (L, o, r, e, m ...)
                for caracter in leitura: # Character = integer value of binary (1001 = 9)
                    # Character of L becomes the integer 76
                    self.buffer_escrita += codificador(caracter)
                    self._escrever_arquivo()

                leitura = file.read(self.buffer_read)

        # If there are values ​​left in the buffer (when less than 8 bits)
            if self.buffer_escrita != '':
                self._escrever_arquivo(True, codificador_final)

        file.close()
        self.arquivo_destino.close()

    def _criar_cabecalho(self, tipo, golomb_divisor, maiorValorDelta = 0):
        # First byte, informs the encoding type
        self.buffer_escrita += str(bin(tipo)[2:]).zfill(8)
        # Second byte, informs the Golomb divisor
        self.buffer_escrita += str(bin(golomb_divisor)[2:]).zfill(8)
        # Third byte, informs the highest Delta value
        self.buffer_escrita += str(bin(maiorValorDelta)[2:]).zfill(8)

    def _escrever_arquivo(self, final = False, codificador_final = None):
        """Turns the bits into bytes and saves them in the file"""
        # Assemble 8-bit sets to byte and save
        while len(self.buffer_escrita) >= 8:
            ## I didn't find a way to transform the binary (string) straight to byte, that's why these conversions ##
            # Transform binary to integer
            inteiro = int(self.buffer_escrita[:8], 2)
           # Convert integer to byte
            byte = bytes([inteiro])

            self.arquivo_destino.write(byte)

            # Remove the 8 bits from the buffer that were saved in the file
            self.buffer_escrita = self.buffer_escrita[8:]

       # If it is the last part of the file, try to reach 8 bits and save
        if final:
            self.buffer_escrita = codificador_final()
            inteiro = int(self.buffer_escrita, 2)
            byte = bytes([inteiro])
            self.arquivo_destino.write(byte)

    def _int_para_str_binario(self, inteiro):
        # Transforma inteiro em binario no formado string
        return bin(inteiro)[2:].zfill(8) # Formato string com len = 8

     ################ CODIFIERS #################
    # Receive full binary value and return encoded binary
    """
        Basic rules of all encoders:
            - Everyone receives an integer value from 0 to 255, which represents a byte
            - Each byte exists in the reading file
            - Everyone must return binary in String format ('111001'), the
                which will be added to the encoded file
        Uza_final == When it is not possible to complete an entire byte with the
            last part of the encoded bits, then some
            treatment to fill the byte or when decoding can
            give some problem
        If it is necessary to use the binary instead of the entire value, it can be
            the "_int_para_str_binario" method was used to receive the
            integer value in string format (input: 10, return: '00001010')
    """

    # Golomb -> prefix (unario) + 1 + suffix (binary)
    def _golomb(self, value ):
        # Calculates the quotient
        quotient = int(value  / self.golomb_divisor)
        # Calculates the rest
        rest = bin(value  % self.golomb_divisor)[2:].zfill(self.logDivisor)
        # Returns the encoded value
        return '1'.zfill(quotient + 1) + str(rest)

    # Write Golomb in the buffer
    def _trata_final_golomb(self):
        return self.buffer_escrita.ljust(8, '0')









