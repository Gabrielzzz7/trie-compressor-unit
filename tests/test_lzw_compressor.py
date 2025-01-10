import os
from FileManager.FileManager import FileManager
import pytest # type: ignore
from LZW.Compressor import LZWCompressor
from tests.helpers.file_manager_helpers import remove_temp_file

# Variáveis de controle
SIGMA_SIZE = 256
DEFAULT_CODE_BITS = 12
INITIAL_BITS_SIZE = 9
CODE_CONTROL_BITS = 32
MAX_DYNAMIC_BITS = 16

def test_compressing_with_fixed_size():
    compressor = LZWCompressor(SIGMA_SIZE, CODE_CONTROL_BITS, DEFAULT_CODE_BITS, DEFAULT_CODE_BITS)
    content = "Em Algoritmos II, falhar nos testes não é o fim — é apenas uma oportunidade para otimizar o código e melhorar a complexidade!"
    result = compressor.Compress(content)
    _, compressed = LZWCompressor.ExtractCodeLenghtAndContent(result, CODE_CONTROL_BITS)
    assert compressed == "001000101001101101000100000001000001001101100001100111001101111001110010001101001001110100001101101001101111001110011000100000001001001001001001000101100000100000001100110001100001001101100001101000001100001001110010000100000001101110100001011000100000001110100001100101001110011100011100100001100001101110011100011001101111000100000011101001000100000100100011001100110001101001100000001100101011100100100000100000001100001001110000001100101001101110001100001100001100001110101001101101001100001100100110001110000100000110001110100001110101001101110001101001001100100001100001001100100001100101000100000001110000100010110100110111001101111001110100100101001001101001001111010100010110100100110000100000001100011011110011001100100001101001100000101000100000101000010001101101001100101100010100100000110101001100100110111001100011001101111001101101001110000001101100001100101001111000100111110101000000001100101000100001"
    
def test_compressing_with_empty_string():
    compressor = LZWCompressor(SIGMA_SIZE, CODE_CONTROL_BITS, DEFAULT_CODE_BITS, DEFAULT_CODE_BITS)
    result = compressor.Compress("")
    _, compressed = LZWCompressor.ExtractCodeLenghtAndContent(result, CODE_CONTROL_BITS)
    assert compressed == ""

def test_compressing_with_repeated_characters():
    compressor = LZWCompressor(SIGMA_SIZE, CODE_CONTROL_BITS, DEFAULT_CODE_BITS, DEFAULT_CODE_BITS)
    result = compressor.Compress("AAAAAA")
    _, compressed = LZWCompressor.ExtractCodeLenghtAndContent(result, CODE_CONTROL_BITS)
    assert compressed == "001000001100000000100000001"

def test_compressing_with_numerical_sequence():
    compressor = LZWCompressor(SIGMA_SIZE, CODE_CONTROL_BITS, DEFAULT_CODE_BITS, DEFAULT_CODE_BITS)
    result = compressor.Compress("12345678901234567890")
    _, compressed = LZWCompressor.ExtractCodeLenghtAndContent(result, CODE_CONTROL_BITS)
    assert compressed == "000110001000110010000110011000110100000110101000110110000110111000111000000111001000110000100000000100000010100000100100000110100001000"

def test_compressing_with_special_characters():
    compressor = LZWCompressor(SIGMA_SIZE, CODE_CONTROL_BITS, DEFAULT_CODE_BITS, DEFAULT_CODE_BITS)
    result = compressor.Compress("!@#$%^&*()_+-=[]{}|;:',.<>/?")
    _, compressed = LZWCompressor.ExtractCodeLenghtAndContent(result, CODE_CONTROL_BITS)
    assert compressed == "000100001001000000000100011000100100000100101001011110000100110000101010000101000000101001001011111000101011000101101000111101001011011001011101001111011001111101001111100000111011000111010000100111000101100000101110000111100000111110000101111000111111"

def test_compressing_with_long_string():
    compressor = LZWCompressor(SIGMA_SIZE, CODE_CONTROL_BITS, DEFAULT_CODE_BITS, DEFAULT_CODE_BITS)
    content = "A" * 10000  # 10.000 caracteres 'A'
    result = compressor.Compress(content)
    _, compressed = LZWCompressor.ExtractCodeLenghtAndContent(result, CODE_CONTROL_BITS)
    assert compressed == "001000001100000000100000001100000010100000011100000100100000101100000110100000111100001000100001001100001010100001011100001100100001101100001110100001111100010000100010001100010010100010011100010100100010101100010110100010111100011000100011001100011010100011011100011100100011101100011110100011111100100000100100001100100010100100011100100100100100101100100110100100111100101000100101001100101010100101011100101100100101101100101110100101111100110000100110001100110010100110011100110100100110101100110110100110111100111000100111001100111010100111011100111100100111101100111110100111111101000000101000001101000010101000011101000100101000101101000110101000111101001000101001001101001010101001011101001100101001101101001110101001111101010000101010001101010010101010011101010100101010101101010110101010111101011000101011001101011010101011011101011100101011101101011110101011111101100000101100001101100010101100011101100100101100101101100110101100111101101000101101001101101010101101011101101100101101101101101110101101111101110000101110001101110010101110011101110100101110101101110110101110111101111000101111001101111010101111011101111100101111101101111110101111111110000000110000001110000010110000011110000100110000101110000110110000111110001000110001001110001010110000000"

def test_extract_code_control_bits_empty_compressing():
    compressor = LZWCompressor(SIGMA_SIZE, CODE_CONTROL_BITS, DEFAULT_CODE_BITS, DEFAULT_CODE_BITS)
    result = compressor.Compress("")
    code_control_bits, _ = LZWCompressor.ExtractCodeLenghtAndContent(result, CODE_CONTROL_BITS)
    assert INITIAL_BITS_SIZE == code_control_bits

def test_extract_code_control_bits_compressing():
    compressor = LZWCompressor(SIGMA_SIZE, CODE_CONTROL_BITS, DEFAULT_CODE_BITS, DEFAULT_CODE_BITS)
    content = "Em Algoritmos II, falhar nos testes não é o fim — é apenas uma oportunidade para otimizar o código e melhorar a complexidade!"
    result = compressor.Compress(content)
    code_control_bits, _ = LZWCompressor.ExtractCodeLenghtAndContent(result, CODE_CONTROL_BITS)
    assert code_control_bits == 9

# Testes de integração:
# Todos os testes abaixo são de integração.

def test_compressing_dynamic_code_lenght_set_right_code_lenght_16_bits():
    content = FileManager.ReadFile('tests/files/dynamic_input_16_bits.txt')
    compressor = LZWCompressor(SIGMA_SIZE, CODE_CONTROL_BITS, DEFAULT_CODE_BITS, MAX_DYNAMIC_BITS, incrementableBits=True)
    result = compressor.Compress(content)
    code_control_bits, _ = LZWCompressor.ExtractCodeLenghtAndContent(result, CODE_CONTROL_BITS)
    assert code_control_bits == 16

def test_compressing_dynamic_code_lenght_set_right_code_lenght_14_bits():
    content = FileManager.ReadFile('tests/files/dynamic_input_14_bits.txt')
    compressor = LZWCompressor(SIGMA_SIZE, CODE_CONTROL_BITS, DEFAULT_CODE_BITS, MAX_DYNAMIC_BITS, incrementableBits=True)
    result = compressor.Compress(content)
    code_control_bits, _ = LZWCompressor.ExtractCodeLenghtAndContent(result, CODE_CONTROL_BITS)
    assert code_control_bits == 14

def test_decompressor_with_enabled_statatistics():
    compressor = LZWCompressor(SIGMA_SIZE, CODE_CONTROL_BITS, DEFAULT_CODE_BITS, DEFAULT_CODE_BITS, enableStatistics=True)
    content = "Em Algoritmos II \n , falhar nos testes não é o fim"
    result = compressor.Compress(content)

    file_name = 'compressed-statistics.csv'
    assert os.path.exists(file_name)
    remove_temp_file(file_name)