import os
import pytest # type: ignore
from FileManager.FileManager import FileManager
from tests.helpers.file_manager_helpers import create_temp_file, remove_temp_file

# Variáveis para testes
CONTENT = "Em Algoritmos II, falhar nos testes não é o fim — é apenas uma oportunidade para otimizar o código e melhorar a complexidade!"
CONTENT_BITS = "0100010101101101001000000100000101101100011001110110111101110010011010010111010001101101011011110111001100100000010010010100100100101100001000000110011001100001011011000110100001100001011100100010000001101110011011110111001100100000011101000110010101110011011101000110010101110011001000000110111011000011101000110110111100100000110000111010100100100000011011110010000001100110011010010110110100100000111000101000000010010100001000001100001110101001001000000110000101110000011001010110111001100001011100110010000001110101011011010110000100100000011011110111000001101111011100100111010001110101011011100110100101100100011000010110010001100101001000000111000001100001011100100110000100100000011011110111010001101001011011010110100101111010011000010111001000100000011011110010000001100011110000111011001101100100011010010110011101101111001000000110010100100000011011010110010101101100011010000110111101110010011000010111001000100000011000010010000001100011011011110110110101110000011011000110010101111000011010010110010001100001011001000110010100100001"
    
def test_read_file_as_text():
    file_name = 'content.txt'
    create_temp_file (CONTENT, file_name)

    content_read = FileManager.ReadFile(file_name)
    remove_temp_file(file_name)

    assert content_read == CONTENT

def test_read_file_as_text_file_not_found():
    with pytest.raises(FileNotFoundError):
        FileManager.ReadFile('any.txt')

def test_save_file_creates_file():
    file_name = 'content.txt'
    FileManager.SaveTextFile(file_name, CONTENT_BITS)

    assert os.path.exists(file_name)
    remove_temp_file(file_name)

def test_saved_text_file_has_right_content():
    file_name = 'content.txt'
    FileManager.SaveTextFile(file_name, CONTENT)
    
    content = FileManager.ReadFile(file_name)
    remove_temp_file(file_name)

    assert content == CONTENT

def test_save_text_empty_file():
    with pytest.raises(Exception):
        FileManager.SaveTextFile(None, None)

def test_should_save_empty_file():
    file_name = 'content.txt'
    FileManager.SaveTextFile(file_name, "")
    
    assert os.path.exists(file_name)
    remove_temp_file(file_name)

def test_should_read_bmp_file():
    expected = FileManager.ReadFile('tests/files/arcane-expected.txt')
    content = FileManager.ReadFile('tests/files/arcane.bmp')

    assert content == expected