"""Definição do nó genérico utilizado pelas estruturas encadeadas."""


class No:
    """Nó genérico para uso em listas encadeadas, filas e pilhas."""

    def __init__(self, dado):
        self.dado = dado
        self.proximo = None
