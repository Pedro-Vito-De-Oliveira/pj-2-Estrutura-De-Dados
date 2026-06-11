"""Entidades de domínio: Cliente, Atendente e Atendimento."""

from datetime import datetime


class Cliente:
    """Representa um cliente do sistema de atendimento."""

    def __init__(self, id_cliente, nome, prioridade=3):
        """`prioridade`: 1 (alta/urgente) a 3 (normal)."""
        self.id = id_cliente
        self.nome = nome
        self.prioridade = prioridade
        self.ativo = True
        self.atendimento_ativo = False
        # Histórico é uma lista encadeada de objetos Atendimento.
        from models.lista_encadeada import ListaEncadeada
        self.historico = ListaEncadeada()

    def __repr__(self):
        status = "ativo" if self.ativo else "inativo"
        return (f"Cliente(id={self.id}, nome='{self.nome}', "
                f"prioridade={self.prioridade}, status={status})")

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "prioridade": self.prioridade,
            "ativo": self.ativo,
            "atendimento_ativo": self.atendimento_ativo,
        }


class Atendente:
    """Representa um atendente responsável por finalizar atendimentos."""

    def __init__(self, id_atendente, nome):
        self.id = id_atendente
        self.nome = nome

    def __repr__(self):
        return f"Atendente(id={self.id}, nome='{self.nome}')"

    def to_dict(self):
        return {"id": self.id, "nome": self.nome}


class Atendimento:
    """Representa um atendimento realizado a um cliente."""

    def __init__(self, id_atendimento, cliente_id, atendente_id,
                 inicio=None, fim=None, duracao_minutos=None):
        self.id = id_atendimento
        self.cliente_id = cliente_id
        self.atendente_id = atendente_id
        self.inicio = inicio or datetime.now()
        self.fim = fim
        self.duracao_minutos = duracao_minutos

    def finalizar(self, atendente_id, fim=None):
        """Marca o atendimento como finalizado, calculando a duração."""
        self.atendente_id = atendente_id
        self.fim = fim or datetime.now()
        delta = self.fim - self.inicio
        self.duracao_minutos = round(delta.total_seconds() / 60, 2)

    def __repr__(self):
        return (f"Atendimento(id={self.id}, cliente_id={self.cliente_id}, "
                f"atendente_id={self.atendente_id}, "
                f"duracao={self.duracao_minutos})")

    def to_dict(self):
        return {
            "id": self.id,
            "cliente_id": self.cliente_id,
            "atendente_id": self.atendente_id,
            "inicio": self.inicio.strftime("%Y-%m-%d %H:%M:%S") if self.inicio else "",
            "fim": self.fim.strftime("%Y-%m-%d %H:%M:%S") if self.fim else "",
            "duracao_minutos": self.duracao_minutos if self.duracao_minutos is not None else "",
        }
