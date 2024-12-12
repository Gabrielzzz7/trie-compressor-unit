import pytest # type: ignore
from BinaryConversor.BinaryConversor import BinaryConversor

# Variáveis para testes
CONTENT = "Em Algoritmos II, falhar nos testes não é o fim — é apenas uma oportunidade para otimizar o código e melhorar a complexidade!"
CONTENT_BITS = "0100010101101101001000000100000101101100011001110110111101110010011010010111010001101101011011110111001100100000010010010100100100101100001000000110011001100001011011000110100001100001011100100010000001101110011011110111001100100000011101000110010101110011011101000110010101110011001000000110111011000011101000110110111100100000110000111010100100100000011011110010000001100110011010010110110100100000111000101000000010010100001000001100001110101001001000000110000101110000011001010110111001100001011100110010000001110101011011010110000100100000011011110111000001101111011100100111010001110101011011100110100101100100011000010110010001100101001000000111000001100001011100100110000100100000011011110111010001101001011011010110100101111010011000010111001000100000011011110010000001100011110000111011001101100100011010010110011101101111001000000110010100100000011011010110010101101100011010000110111101110010011000010111001000100000011000010010000001100011011011110110110101110000011011000110010101111000011010010110010001100001011001000110010100100001"
    
def test_convert_binary_to_string():
    converted = BinaryConversor.ConvertBinaryToString(CONTENT_BITS)
    assert converted == CONTENT

def test_convert_string_to_binary():
    converted = BinaryConversor.ConvertBinaryToString(CONTENT_BITS)
    assert converted == CONTENT

def test_convert_none_binary_returns_empty():
    converted = BinaryConversor.ConvertBinaryToString(None)
    assert converted == ""

def test_convert_binary_to_string():
    converted = BinaryConversor.ConvertBinaryToString(CONTENT_BITS)
    assert converted == CONTENT

def test_convert_integer_to_binary_string():
    converted = BinaryConversor.ConvertIntegerToBinaryString(65, 8)
    assert converted == "01000001"

def test_convert_prefix_to_binary_string():
    converted = BinaryConversor.ConvertPrefixToBinaryString("ABC")
    assert converted == "100000110000101000011"

def test_convert_none_binary_returns_empty():
    converted = BinaryConversor.ConvertBinaryToString(None)
    assert converted == ""

def test_convert_empty_binary_returns_empty():
    converted = BinaryConversor.ConvertBinaryToString("")
    assert converted == ""

def test_convert_exclamation_prefix_to_binary():
    converted = BinaryConversor.ConvertPrefixToBinaryString("!")
    assert converted == '100001'
