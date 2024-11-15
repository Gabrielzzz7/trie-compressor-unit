import pytest # type: ignore
from LZW.Compressor import LZWCompressor

# Variáveis de controle
SIGMA_SIZE = 256
DEFAULT_CODE_BITS = 12
INITIAL_BITS_SIZE = 9

# Variáveis para testes
CONTENT = "Em Algoritmos II, falhar nos testes não é o fim — é apenas uma oportunidade para otimizar o código e melhorar a complexidade!"
CONTENT_BITS = "0100010101101101001000000100000101101100011001110110111101110010011010010111010001101101011011110111001100100000010010010100100100101100001000000110011001100001011011000110100001100001011100100010000001101110011011110111001100100000011101000110010101110011011101000110010101110011001000000110111011000011101000110110111100100000110000111010100100100000011011110010000001100110011010010110110100100000111000101000000010010100001000001100001110101001001000000110000101110000011001010110111001100001011100110010000001110101011011010110000100100000011011110111000001101111011100100111010001110101011011100110100101100100011000010110010001100101001000000111000001100001011100100110000100100000011011110111010001101001011011010110100101111010011000010111001000100000011011110010000001100011110000111011001101100100011010010110011101101111001000000110010100100000011011010110010101101100011010000110111101110010011000010111001000100000011000010010000001100011011011110110110101110000011011000110010101111000011010010110010001100001011001000110010100100001"
COMPRESSED_CONTENT = "001000101001101101000100000001000001001101100001100111001101111001110010001101001001110100001101101001101111001110011000100000001001001001001001000101100000100000001100110001100001001101100001101000001100001001110010000100000001101110100001011000100000001110100001100101001110011100011100100001100001101110011100011001101111000100000011101001000100000100100011001100110001101001100000001100101011100100100000100000001100001001110000001100101001101110001100001100001100001110101001101101001100001100100110001110000100000110001110100001110101001101110001101001001100100001100001001100100001100101000100000001110000100010110100110111001101111001110100100101001001101001001111010100010110100100110000100000001100011011110011001100100001101001100000101000100000101000010001101101001100101100010100100000110101001100100110111001100011001101111001101101001110000001101100001100101001111000100111110101000000001100101000100001"
REQUIRED_BITS = 9

def test_compressing_with_fixed_size():
    compressor = LZWCompressor(SIGMA_SIZE, DEFAULT_CODE_BITS, INITIAL_BITS_SIZE)
    compressed = compressor.Compress(CONTENT)
    assert COMPRESSED_CONTENT == compressed
    
def test_compressing_with_empty_string():
    compressor = LZWCompressor(SIGMA_SIZE, DEFAULT_CODE_BITS, INITIAL_BITS_SIZE)
    compressed = compressor.Compress("")
    assert compressed == ""

def test_compressing_with_repeated_characters():
    compressor = LZWCompressor(SIGMA_SIZE, DEFAULT_CODE_BITS, INITIAL_BITS_SIZE)
    compressed = compressor.Compress("AAAAAA")
    assert compressed == "001000001100000000100000001"

def test_compressing_with_numerical_sequence():
    compressor = LZWCompressor(SIGMA_SIZE, DEFAULT_CODE_BITS, INITIAL_BITS_SIZE)
    compressed = compressor.Compress("12345678901234567890")
    assert compressed == "000110001000110010000110011000110100000110101000110110000110111000111000000111001000110000100000000100000010100000100100000110100001000"

def test_compressing_with_special_characters():
    compressor = LZWCompressor(SIGMA_SIZE, DEFAULT_CODE_BITS, INITIAL_BITS_SIZE)
    compressed = compressor.Compress("!@#$%^&*()_+-=[]{}|;:',.<>/?")
    assert compressed == "000100001001000000000100011000100100000100101001011110000100110000101010000101000000101001001011111000101011000101101000111101001011011001011101001111011001111101001111100000111011000111010000100111000101100000101110000111100000111110000101111000111111"

def test_compressing_with_long_string():
    compressor = LZWCompressor(SIGMA_SIZE, DEFAULT_CODE_BITS, INITIAL_BITS_SIZE)
    content = "A" * 10000  # 10.000 caracteres 'A'
    compressed = compressor.Compress(content)
    assert compressed == "001000001100000000100000001100000010100000011100000100100000101100000110100000111100001000100001001100001010100001011100001100100001101100001110100001111100010000100010001100010010100010011100010100100010101100010110100010111100011000100011001100011010100011011100011100100011101100011110100011111100100000100100001100100010100100011100100100100100101100100110100100111100101000100101001100101010100101011100101100100101101100101110100101111100110000100110001100110010100110011100110100100110101100110110100110111100111000100111001100111010100111011100111100100111101100111110100111111101000000101000001101000010101000011101000100101000101101000110101000111101001000101001001101001010101001011101001100101001101101001110101001111101010000101010001101010010101010011101010100101010101101010110101010111101011000101011001101011010101011011101011100101011101101011110101011111101100000101100001101100010101100011101100100101100101101100110101100111101101000101101001101101010101101011101101100101101101101101110101101111101110000101110001101110010101110011101110100101110101101110110101110111101111000101111001101111010101111011101111100101111101101111110101111111110000000110000001110000010110000011110000100110000101110000110110000111110001000110001001110001010110000000"