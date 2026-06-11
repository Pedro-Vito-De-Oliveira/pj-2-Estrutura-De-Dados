"""Implementação manual de Fila Simples e Fila de Prioridade.

Ambas baseadas em nós encadeados (sem uso de queue.Queue ou collections.deque).
"""

from models.no import No


class Fila:
    """Fila FIFO clássica baseada em nós encadeados.

    Mantém ponteiros para início (frente) e fim (traseira) para que
    enfileirar e desenfileirar sejam operações O(1).
    """

    def __init__(self):
        self.frente = None
        self.traseira = None
        self.tamanho = 0

    def enfileirar(self, dado):
        """Insere um elemento no final da fila. O(1)."""
        novo = No(dado)
        if self.traseira is None:
            self.frente = novo
            self.traseira = novo
        else:
            self.traseira.proximo = novo
            self.traseira = novo
        self.tamanho += 1

    def desenfileirar(self):
        """Remove e retorna o elemento da frente da fila. O(1).

        Retorna None se a fila estiver vazia.
        """
        if self.frente is None:
            return None

        no_removido = self.frente
        self.frente = self.frente.proximo
        if self.frente is None:
            self.traseira = None
        self.tamanho -= 1
        return no_removido.dado

    def espiar(self):
        """Retorna o elemento da frente sem removê-lo. O(1)."""
        return self.frente.dado if self.frente is not None else None

    def esta_vazia(self):
        return self.tamanho == 0

    def __len__(self):
        return self.tamanho

    def __iter__(self):
        atual = self.frente
        while atual is not None:
            yield atual.dado
            atual = atual.proximo


class FilaPrioridade:
    """Fila de prioridade baseada em múltiplas filas internas (FIFO por nível).

    Cada nível de prioridade possui sua própria Fila comum, garantindo
    que, dentro do mesmo nível, a ordem de chegada (FIFO) seja preservada.
    Quanto MENOR o número de prioridade, MAIOR a urgência (1 = mais urgente).
    """

    def __init__(self, niveis=3):
        """Cria a fila de prioridade com `niveis` níveis (1..niveis)."""
        self.niveis = niveis
        # Uma fila comum para cada nível de prioridade.
        self.filas = [Fila() for _ in range(niveis)]
        self.tamanho = 0

    def _validar_prioridade(self, prioridade):
        if not isinstance(prioridade, int) or prioridade < 1 or prioridade > self.niveis:
            raise ValueError(
                f"Prioridade deve ser um inteiro entre 1 e {self.niveis}."
            )

    def enfileirar(self, dado, prioridade):
        """Insere um elemento respeitando a prioridade. O(1).

        Dentro do mesmo nível, a ordem de chegada é preservada (FIFO).
        """
        self._validar_prioridade(prioridade)
        self.filas[prioridade - 1].enfileirar(dado)
        self.tamanho += 1

    def desenfileirar(self):
        """Remove e retorna o elemento de maior prioridade mais antigo.

        Complexidade: O(P), onde P é o número de níveis de prioridade
        (constante e pequeno na prática).
        """
        for fila in self.filas:
            if not fila.esta_vazia():
                self.tamanho -= 1
                return fila.desenfileirar()
        return None

    def espiar(self):
        """Retorna o próximo elemento a ser atendido sem removê-lo. O(P)."""
        for fila in self.filas:
            if not fila.esta_vazia():
                return fila.espiar()
        return None

    def esta_vazia(self):
        return self.tamanho == 0

    def __len__(self):
        return self.tamanho

    def __iter__(self):
        """Itera respeitando a ordem de atendimento (prioridade -> chegada)."""
        for fila in self.filas:
            for item in fila:
                yield item
