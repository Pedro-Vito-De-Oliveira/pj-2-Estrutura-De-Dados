"""Implementação manual de Vetor Ordenado com Busca Binária e MergeSort.

Todas as operações de ordenação e busca são implementadas manualmente,
sem uso de `sorted()`, `.sort()` ou módulos prontos de busca.
"""


class VetorOrdenado:
    """Vetor (lista Python usada apenas como array bruto) mantido ordenado
    por uma chave (ex.: ID do cliente), permitindo Busca Binária recursiva.
    """

    def __init__(self, chave=lambda item: item):
        """`chave` é uma função que extrai o valor de comparação do item."""
        self._dados = []
        self._chave = chave

    def inserir(self, item):
        """Insere mantendo a ordenação (busca posição + deslocamento). O(n)."""
        posicao = self._encontrar_posicao_insercao(item)
        self._dados.insert(posicao, item)

    def _encontrar_posicao_insercao(self, item):
        """Encontra a posição correta via busca linear. O(n)."""
        valor = self._chave(item)
        i = 0
        while i < len(self._dados) and self._chave(self._dados[i]) < valor:
            i += 1
        return i

    def remover(self, valor_chave):
        """Remove o item cuja chave seja igual a `valor_chave`. O(n)."""
        for i in range(len(self._dados)):
            if self._chave(self._dados[i]) == valor_chave:
                return self._dados.pop(i)
        return None

    def busca_binaria(self, valor_chave):
        """Busca binária recursiva pelo valor de chave. O(log n)."""
        return self._busca_binaria_rec(valor_chave, 0, len(self._dados) - 1)

    def _busca_binaria_rec(self, valor_chave, inicio, fim):
        """Implementação recursiva da busca binária."""
        if inicio > fim:
            return None

        meio = (inicio + fim) // 2
        chave_meio = self._chave(self._dados[meio])

        if chave_meio == valor_chave:
            return self._dados[meio]
        elif chave_meio < valor_chave:
            return self._busca_binaria_rec(valor_chave, meio + 1, fim)
        else:
            return self._busca_binaria_rec(valor_chave, inicio, meio - 1)

    def para_lista(self):
        """Retorna uma cópia da lista interna (já ordenada)."""
        return list(self._dados)

    def __len__(self):
        return len(self._dados)

    def __iter__(self):
        return iter(self._dados)


def merge_sort(lista, chave=lambda item: item):
    """Ordena `lista` usando MergeSort recursivo (estável). O(n log n).

    Retorna uma NOVA lista ordenada; não modifica a lista original.
    """
    if len(lista) <= 1:
        return list(lista)

    meio = len(lista) // 2
    esquerda = merge_sort(lista[:meio], chave)
    direita = merge_sort(lista[meio:], chave)

    return _combinar(esquerda, direita, chave)


def _combinar(esquerda, direita, chave):
    """Combina (merge) duas listas ordenadas em uma única lista ordenada."""
    resultado = []
    i = j = 0

    while i < len(esquerda) and j < len(direita):
        if chave(esquerda[i]) <= chave(direita[j]):
            resultado.append(esquerda[i])
            i += 1
        else:
            resultado.append(direita[j])
            j += 1

    while i < len(esquerda):
        resultado.append(esquerda[i])
        i += 1

    while j < len(direita):
        resultado.append(direita[j])
        j += 1

    return resultado
