from Trie.Trie import Trie

class LZWCompressor:
    def __init__(self, sigmaSize, codeBits, initialBitsSize, incrementableBits = False):
        self.dict = Trie()
        self.sigmaSize = sigmaSize
        self.codeBits = codeBits
        self.initialBitsSize = initialBitsSize
        self.incrementableBits = incrementableBits

        # Adicionando os códigos iniciais
        for index in range(sigmaSize):
            self.dict[chr(index)] = index

    def __convertIntegerToBinaryString(self, integer, size = 0):
        binary_str = bin(integer)[2:]

        if size != 0:
            binary_str = binary_str.zfill(size)
        
        return binary_str

    def Compress(self, content):
        compressedcontent = []

        prefix = ""
        biggestCode = self.sigmaSize
        #currentBits = self.initialBitsSize
        #maxIntegerForCurrentBits = (2 ** currentBits) - 1

        for char in content:
            prefix_with_char = prefix + char

            if self.dict.ContainsKey(prefix_with_char):
                prefix = prefix_with_char
            else:
                value = self.__convertIntegerToBinaryString(self.dict[prefix], 12)
                compressedcontent.append(value)

                #if self.incrementableBits and maxIntegerForCurrentBits == biggestCode:
                #    currentBits += 1
                #    maxIntegerForCurrentBits = (2 ** currentBits) - 1

                self.dict[prefix_with_char] = biggestCode
                biggestCode += 1

                prefix = char
            
        if prefix:
            value = self.__convertIntegerToBinaryString(self.dict[prefix], 12)
            compressedcontent.append(value)

        return ''.join(compressedcontent)