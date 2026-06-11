"""Implementação manual de uma Lista Encadeada Simples."""

from models.no import No


class ListaEncadeada:
    """Lista encadeada simples para gerenciar clientes ativos.

    Permite inserção no início/fim, busca, remoção e iteração,
    sem uso de estruturas prontas do Python.
    """

    def __init__(self):
        self.cabeca = None
        self.tamanho = 0

    def inserir_fim(self, dado):
        """Insere um elemento ao final da lista. O(n)."""
        novo = No(dado)
        if self.cabeca is None:
            self.cabeca = novo
        else:
            atual = self.cabeca
            while atual.proximo is not None:
                atual = atual.proximo
            atual.proximo = novo
        self.tamanho += 1

    def remover(self, condicao):
        """Remove o primeiro elemento que satisfaça `condicao(dado)`. O(n).

        Retorna o dado removido ou None se não encontrado.
        """
        anterior = None
        atual = self.cabeca

        while atual is not None:
            if condicao(atual.dado):
                if anterior is None:
                    self.cabeca = atual.proximo
                else:
                    anterior.proximo = atual.proximo
                self.tamanho -= 1
                return atual.dado
            anterior = atual
            atual = atual.proximo

        return None

    def buscar(self, condicao):
        """Retorna o primeiro dado que satisfaça `condicao(dado)`. O(n)."""
        atual = self.cabeca
        while atual is not None:
            if condicao(atual.dado):
                return atual.dado
            atual = atual.proximo
        return None

    def para_lista(self):
        """Converte a lista encadeada em uma lista Python (apenas p/ exibição)."""
        resultado = []
        atual = self.cabeca
        while atual is not None:
            resultado.append(atual.dado)
            atual = atual.proximo
        return resultado

    def __len__(self):
        return self.tamanho

    def __iter__(self):
        atual = self.cabeca
        while atual is not None:
            yield atual.dado
            atual = atual.proximo
