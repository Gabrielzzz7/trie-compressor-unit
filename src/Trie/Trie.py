import sys
from pympler import asizeof

SIGMA_SIZE = 2
IS_WORD_FULL = "$"
class _trieNode:
    def __init__(self, previous, substring="", value=None):
        """
        Inicializa um nó com uma lista de filhos e um valor associado.
        
        :param previous: Nó anterior no caminho da árvore Trie.
        :param substring: Substring associada ao nó.
        :param value: Valor armazenado no nó, se for uma folha (None se não for).
        """
        self.children = [None] * (SIGMA_SIZE + 1)
        self.substring = substring
        self.lenSubstring = len(substring)
        self.previous = previous
        self._value = value
        self._isLeaf = (value is not None)

    def IsLeaf(self):
        """
        Verifica se o nó é uma folha (ou seja, contém um valor).

        :return: True se o nó for uma folha, False caso contrário.
        """
        return self._isLeaf

    def GetValue(self):
        """
        Retorna o valor armazenado no nó.

        :return: O valor armazenado no nó ou None se não houver valor.
        """
        return self._value

    def SetValue(self, value):
        """
        Define o valor armazenado no nó e atualiza seu estado para folha se o novo valor 
        não for None.

        :param value: O valor a ser armazenado no nó.
        """
        self._value = value
        self._isLeaf = True if value is not None else False

    def SetSubstring(self, value):
        """
        Define o substring do nó e ajusta sua condição de folha.

        :param value: O substring a ser associado ao nó.
        """
        self.substring = value
        self.lenSubstring = len(value)
        self._isLeaf = False if value is None else True

    def GetSubstring(self):
        """
        Retorna o substring associado ao nó.

        :return: O substring armazenado no nó.
        """
        return self.substring

class Trie:
    def __init__(self, detailedReturn = False):
        """
        Inicializa a árvore Trie com a raiz e parâmetros de controle.

        :param detailedReturn: Por padrão é falso. Define o tipo de retorno do método.
        """
        self.root = _trieNode(None)
        self._depth = 1
        self._nodeCount = 1
        self.detailedReturn = detailedReturn  
        
    def SetDetailedReturn(self, value):
        """
        Define se o retorno será detalhado para inserções e buscas.

        :param value: Booleano indicando se o retorno deve ser detalhado.
        """
        self.detailedReturn = value
        
    def GetDetailedReturn(self):
        """
        Retorna o valor atual da configuração de retorno detalhado.

        :return: True se o retorno for detalhado, False caso contrário.
        """
        return self.detailedReturn

    def Insert(self, key, value):  
        """
        Insere uma chave associada a um valor na árvore Trie.

        :param key: A chave a ser inserida (uma sequência binária de 0s e 1s).
        :param value: O valor a ser associado à chave.
        :return: Detalhes do processo de inserção ou o par (key, value) se 'detailedReturn' for False.
        """     
        detailedReturn = self.GetDetailedReturn()
        
        currentNode = self.root
        insertionDepth = 0
        i = 0
        bit = int(key[i])

        lenKey = len(key)
        while i < lenKey:
            if currentNode.children[bit] is None:
                currentNode.children[bit] = _trieNode(currentNode, key[i:], value)
                currentNode = currentNode.children[bit]
                insertionDepth += 1
                self._nodeCount += 1
                self._depth = max(self._depth, insertionDepth)
                return (currentNode.GetSubstring(), currentNode.GetValue()) if not detailedReturn else (key, key, None, value)
            else:
                childNode = currentNode.children[bit]
                substring = childNode.substring
                lenSubstring = childNode.lenSubstring

            j = 0
            while j < lenSubstring and i + j < lenKey:
                if i + j >= lenKey or key[i + j] != substring[j]:
                    prefixMatch = substring[:j]
                    suffixExisting = substring[j:]
                    suffixNew = key[i + j:]

                    breakbitKey = int(key[i + j])
                    breakbitSubstring = 0 if breakbitKey == 1 else 1

                    extraReference  = childNode.children[SIGMA_SIZE]
                    oldChildren = childNode.children                    
                    childNode.SetSubstring(prefixMatch)
                    childNode.children = [None] * (SIGMA_SIZE + 1)

                    newChildExisting = _trieNode(childNode, suffixExisting, childNode.GetValue())
                    newChildExisting.children = oldChildren  
                    childNode.children[breakbitSubstring] = newChildExisting

                    if extraReference  is not None:
                        newChildExisting.children[SIGMA_SIZE] = extraReference 

                    newChildNode = _trieNode(childNode, suffixNew, value)
                    childNode.children[breakbitKey] = newChildNode
                    childNode.SetValue(None)

                    insertionDepth += 1
                    self._nodeCount += 2
                    self._depth = max(self._depth, insertionDepth)

                    return (key, value) if not detailedReturn else (key, suffixNew, suffixExisting, newChildNode.GetValue())
                
                j += 1
            if i + j == (lenKey - 1) and j < lenSubstring:
                bit = substring[j]
                newChildNode = _trieNode(currentNode, IS_WORD_FULL, value)
                childNode.children[2] = newChildNode
                
                newChildExisting = _trieNode(currentNode, substring[j:], value)
                newChildExisting.children = childNode.children[bit].children if childNode.children[bit] is not None else [None] * (SIGMA_SIZE + 1)
                childNode.children[bit] = newChildExisting
                currentNode: _trieNode = childNode.children[bit]
                
                insertionDepth += 1
                self._nodeCount += 2
                self._depth = max(self._depth, insertionDepth)

                return (key, value) if not detailedReturn else (key, IS_WORD_FULL, currentNode.GetSubstring(), currentNode.GetValue())

            i += lenSubstring            
            bit = int(key[i]) if i < lenKey else None
            if bit is not None and childNode.children[bit] is None and childNode.IsLeaf():
                newChildNode = _trieNode(currentNode, IS_WORD_FULL, childNode.GetValue())
                childNode.children[2] = newChildNode
                childNode.children[bit] = _trieNode(currentNode, key[i:], value)
                currentNode: _trieNode = childNode.children[bit]
                
                insertionDepth += 1
                self._nodeCount += 2
                self._depth = max(self._depth, insertionDepth)

                return (key, value) if not detailedReturn else (key, IS_WORD_FULL, currentNode.GetSubstring(), currentNode.GetValue())
            
            currentNode = childNode
        
        insertionDepth += 1
        self._nodeCount += 1
        self._depth = max(self._depth, insertionDepth)
        return (key, value) if not detailedReturn else (key, currentNode.GetSubstring(), None, value)

    def Search(self, key):
        """
        Busca por uma chave na árvore Trie.

        :param key: A chave a ser buscada.
        :return: O valor associado à chave ou None se não for encontrada.
        """
        detailedReturn = self.GetDetailedReturn()
        currentNode = self.root
        i = 0
        lenKey = len(key)

        while i < lenKey:
            bit = int(key[i])
            child = currentNode.children[bit]

            if child is None:
                return None

            substring = child.substring
            lenSubstring = child.lenSubstring

            if key[i:i + lenSubstring] != substring:
                return None

            i += lenSubstring
            currentNode = child

        suffix = (
            currentNode.substring
            if currentNode.children[SIGMA_SIZE] is None
            else currentNode.children[SIGMA_SIZE].substring
        )

        return (key, suffix, currentNode._value, currentNode) if detailedReturn else currentNode._value
    
    def ContainsKey(self, key):
        """
        Verifica se uma chave está presente na árvore Trie.

        :param key: A chave a ser verificada.
        :return: True se a chave estiver presente, False caso contrário.
        """
        return self.Search(key) != None

    def Remove(self, key):
        """
        Remove uma chave da árvore Trie.

        :param key: A chave a ser removida.
        :return: True se a remoção for bem-sucedida, False se a chave não for encontrada.
        :raises: Retorna um conjunto detalhado de informações sobre a remoção se `detailedReturn` for True.
        """
        self.SetDetailedReturn(True)

        search_result = self.Search(key)
        if search_result is None:
            return False
        
        currentNode = search_result[3]
        value = currentNode._value
        currentNode.SetValue(None)
                
        if currentNode.children[SIGMA_SIZE] is None:
            parentNode: _trieNode = currentNode.previous
        else:
            parentNode = currentNode

        if parentNode is self.root and not any(child for child in currentNode.children):
            parentNode.children[int(key[0])] = None
            self._nodeCount -= 1
            return (key, parentNode.GetSubstring(), value) if self.detailedReturn else True

        nonNoneChildrenCount = len([child for child in parentNode.children if child is not None])
        
        if nonNoneChildrenCount - 1 == 1:
            if currentNode.children[SIGMA_SIZE] is None:
                currentNode.children[SIGMA_SIZE] = None
                self._nodeCount -= 1
                bit = int(currentNode.substring[0])
                bitFusion = 0 if bit == 1 else 1
                
                substringFusion = parentNode.children[bitFusion].substring
                substringParentNode = parentNode.substring
                substringParentNode += substringFusion
                parentNode.SetSubstring(substringParentNode)                
            else:
                for i, child in enumerate(currentNode.children):
                    if i != SIGMA_SIZE and child is not None:
                        child_to_fuse = child
                        break
                if child_to_fuse is not None:
                    parentNode = currentNode
                    substringFusion = child_to_fuse.substring
                    substringParentNode = currentNode.substring
                    substringParentNode += substringFusion
                    parentNode.SetSubstring(substringParentNode)

            childCurrentNode = currentNode.children
            parentNode.children = childCurrentNode
            self._nodeCount -= 1
            self._depth -= 1
            
            return (key, parentNode.GetSubstring(), value) if self.detailedReturn else True

        return (key, parentNode.GetSubstring(), value) if self.detailedReturn else True                    

    def __getitem__(self, key):
        """
        Obtém o valor associado a uma chave na árvore Trie.

        :param key: A chave a ser buscada.
        :return: O valor associado à chave, ou levanta uma exceção KeyError se a chave não for encontrada.
        """
        return self.Search(key)

    def __setitem__(self, key, value):
        """
        Insere ou atualiza uma chave na árvore Trie com um valor.

        :param key: A chave a ser inserida ou atualizada.
        :param value: O valor a ser associado à chave.
        """
        self.Insert(key, value)

    def GetNodeCount(self):
        """
        Retorna o número total de nós na árvore Trie.

        :return: O número total de nós na árvore Trie.
        """
        return self._nodeCount

    def GetDepth(self):
        return self._depth
