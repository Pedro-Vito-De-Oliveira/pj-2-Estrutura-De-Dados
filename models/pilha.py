"""Implementação manual de uma Pilha (Stack) baseada em nós encadeados."""

from models.no import No


class Pilha:
    """Pilha LIFO usada para a funcionalidade 'Desfazer última ação'."""

    def __init__(self):
        self.topo = None
        self.tamanho = 0

    def empilhar(self, dado):
        """Insere um elemento no topo da pilha. O(1)."""
        novo = No(dado)
        novo.proximo = self.topo
        self.topo = novo
        self.tamanho += 1

    def desempilhar(self):
        """Remove e retorna o elemento do topo. O(1).

        Retorna None se a pilha estiver vazia.
        """
        if self.topo is None:
            return None

        no_removido = self.topo
        self.topo = self.topo.proximo
        self.tamanho -= 1
        return no_removido.dado

    def espiar(self):
        """Retorna o elemento do topo sem removê-lo. O(1)."""
        return self.topo.dado if self.topo is not None else None

    def esta_vazia(self):
        return self.tamanho == 0

    def __len__(self):
        return self.tamanho
