"""Serviço principal: regras de negócio do sistema de atendimento.

Integra Lista Encadeada (clientes ativos), Fila de Prioridade (espera),
Pilha (desfazer), Vetor Ordenado + Busca Binária (consulta por ID) e
MergeSort (relatórios).
"""

from datetime import datetime

from models.entidades import Atendimento, Atendente, Cliente
from models.fila import FilaPrioridade
from models.lista_encadeada import ListaEncadeada
from models.pilha import Pilha
from models.vetor_ordenado import VetorOrdenado, merge_sort
from services import persistencia
from services.persistencia import logger


class GerenciadorAtendimento:
    """Classe central que orquestra clientes, atendentes, filas e histórico."""

    def __init__(self):
        # Lista encadeada de clientes ativos (permite remoção eficiente).
        self.clientes_ativos = ListaEncadeada()

        # Vetor ordenado por ID para busca binária rápida.
        self.vetor_clientes = VetorOrdenado(chave=lambda c: c.id)

        # Fila de prioridade de espera (1 = urgente, 3 = normal).
        self.fila_espera = FilaPrioridade(niveis=3)

        # Pilha para desfazer a última finalização de atendimento.
        self.pilha_desfazer = Pilha()

        # Lista (Python simples) de atendentes - cadastro pequeno.
        self.atendentes = []

        # Histórico geral de atendimentos finalizados (para relatórios).
        self.historico_geral = []

        # Atendimento atualmente em curso (None se ninguém sendo atendido).
        self.atendimento_atual = None

        # Contadores de IDs.
        self._proximo_id_cliente = 1
        self._proximo_id_atendente = 1
        self._proximo_id_atendimento = 1

    # ------------------------------------------------------------------
    # Cadastro de Clientes
    # ------------------------------------------------------------------
    def cadastrar_cliente(self, nome, prioridade=3):
        """Cadastra um novo cliente e o coloca na fila de espera."""
        if not nome or not nome.strip():
            raise ValueError("Nome do cliente não pode ser vazio.")
        if prioridade not in (1, 2, 3):
            raise ValueError("Prioridade deve ser 1 (alta), 2 (média) ou 3 (normal).")

        cliente = Cliente(self._proximo_id_cliente, nome.strip(), prioridade)
        self._proximo_id_cliente += 1

        self.clientes_ativos.inserir_fim(cliente)
        self.vetor_clientes.inserir(cliente)
        self.fila_espera.enfileirar(cliente, prioridade)

        logger.info("Cliente cadastrado: %s (prioridade %s)", cliente, prioridade)
        return cliente

    def remover_cliente(self, id_cliente):
        """Remove (inativa) um cliente, desde que não esteja em atendimento."""
        cliente = self.buscar_cliente_por_id(id_cliente)
        if cliente is None:
            raise ValueError(f"Cliente com ID {id_cliente} não encontrado.")

        if cliente.atendimento_ativo:
            raise ValueError(
                f"Não é possível remover o cliente {cliente.nome}: "
                "ele possui um atendimento ativo."
            )

        removido = self.clientes_ativos.remover(lambda c: c.id == id_cliente)
        if removido is not None:
            removido.ativo = False
            logger.info("Cliente removido (inativado): %s", removido)
        return removido

    # ------------------------------------------------------------------
    # Cadastro de Atendentes
    # ------------------------------------------------------------------
    def cadastrar_atendente(self, nome):
        """Cadastra um novo atendente."""
        if not nome or not nome.strip():
            raise ValueError("Nome do atendente não pode ser vazio.")

        atendente = Atendente(self._proximo_id_atendente, nome.strip())
        self._proximo_id_atendente += 1
        self.atendentes.append(atendente)

        logger.info("Atendente cadastrado: %s", atendente)
        return atendente

    def buscar_atendente_por_id(self, id_atendente):
        """Busca linear de atendente (lista pequena, não exige estrutura especial)."""
        for atendente in self.atendentes:
            if atendente.id == id_atendente:
                return atendente
        return None

    # ------------------------------------------------------------------
    # Busca de Clientes (Vetor Ordenado + Busca Binária)
    # ------------------------------------------------------------------
    def buscar_cliente_por_id(self, id_cliente):
        """Busca um cliente por ID usando Busca Binária recursiva. O(log n)."""
        return self.vetor_clientes.busca_binaria(id_cliente)

    # ------------------------------------------------------------------
    # Fluxo de Atendimento
    # ------------------------------------------------------------------
    def chamar_proximo(self):
        """Remove o próximo cliente da fila de prioridade e inicia o atendimento.

        Levanta ValueError se a fila estiver vazia ou se já houver um
        atendimento em curso.
        """
        if self.atendimento_atual is not None:
            raise ValueError(
                "Já existe um atendimento em andamento. "
                "Finalize-o antes de chamar o próximo."
            )

        if self.fila_espera.esta_vazia():
            raise ValueError("Não há clientes na fila de espera.")

        cliente = self.fila_espera.desenfileirar()
        cliente.atendimento_ativo = True

        atendimento = Atendimento(
            id_atendimento=self._proximo_id_atendimento,
            cliente_id=cliente.id,
            atendente_id=None,
            inicio=datetime.now(),
        )
        self._proximo_id_atendimento += 1
        self.atendimento_atual = atendimento

        logger.info("Atendimento iniciado: cliente=%s, atendimento_id=%s",
                     cliente.nome, atendimento.id)
        return cliente, atendimento

    def finalizar_atendimento(self, id_atendente):
        """Finaliza o atendimento atual, registrando atendente e duração.

        Move o atendimento para o histórico do cliente e empilha a operação
        para possível 'Desfazer'.
        """
        if self.atendimento_atual is None:
            raise ValueError("Não há atendimento em andamento para finalizar.")

        atendente = self.buscar_atendente_por_id(id_atendente)
        if atendente is None:
            raise ValueError(f"Atendente com ID {id_atendente} não encontrado.")

        cliente = self.buscar_cliente_por_id(self.atendimento_atual.cliente_id)
        if cliente is None:
            raise ValueError("Cliente do atendimento atual não foi encontrado.")

        atendimento = self.atendimento_atual
        atendimento.finalizar(atendente_id=atendente.id)

        cliente.historico.inserir_fim(atendimento)
        cliente.atendimento_ativo = False
        self.historico_geral.append(atendimento)

        # Guarda estado anterior para permitir desfazer.
        self.pilha_desfazer.empilhar({
            "cliente": cliente,
            "atendimento": atendimento,
        })

        self.atendimento_atual = None

        logger.info(
            "Atendimento finalizado: cliente=%s, atendente=%s, duracao=%.2f min",
            cliente.nome, atendente.nome, atendimento.duracao_minutos
        )
        return atendimento

    def desfazer_ultima_finalizacao(self):
        """Desfaz a última finalização, retornando o cliente para a fila.

        Remove o atendimento do histórico, retorna o cliente para a fila
        de espera (com a prioridade original) e limpa os dados de
        finalização do atendimento.
        """
        if self.pilha_desfazer.esta_vazia():
            raise ValueError("Não há ações para desfazer.")

        if self.atendimento_atual is not None:
            raise ValueError(
                "Não é possível desfazer enquanto há um atendimento em "
                "andamento. Finalize-o primeiro."
            )

        ultima_acao = self.pilha_desfazer.desempilhar()
        cliente = ultima_acao["cliente"]
        atendimento = ultima_acao["atendimento"]

        # Remove do histórico do cliente e do histórico geral.
        cliente.historico.remover(lambda a: a.id == atendimento.id)
        if atendimento in self.historico_geral:
            self.historico_geral.remove(atendimento)

        # Restaura o atendimento como "em andamento".
        atendimento.fim = None
        atendimento.duracao_minutos = None
        atendimento.atendente_id = None
        cliente.atendimento_ativo = True
        self.atendimento_atual = atendimento

        logger.info("Última finalização desfeita: cliente=%s, atendimento_id=%s",
                     cliente.nome, atendimento.id)
        return cliente, atendimento

    # ------------------------------------------------------------------
    # Relatórios
    # ------------------------------------------------------------------
    def tempo_medio_atendimento(self):
        """Calcula o tempo médio (em minutos) de todos os atendimentos finalizados."""
        finalizados = [a for a in self.historico_geral if a.duracao_minutos is not None]
        if not finalizados:
            return 0.0

        soma = 0.0
        for atendimento in finalizados:
            soma += atendimento.duracao_minutos

        return round(soma / len(finalizados), 2)

    def filtrar_por_data(self, data_inicio, data_fim):
        """Filtra atendimentos finalizados dentro do intervalo [data_inicio, data_fim].

        `data_inicio` e `data_fim` são objetos `datetime`.
        """
        if data_inicio > data_fim:
            raise ValueError("Data de início não pode ser posterior à data de fim.")

        resultado = []
        for atendimento in self.historico_geral:
            if atendimento.fim is None:
                continue
            if data_inicio <= atendimento.fim <= data_fim:
                resultado.append(atendimento)

        return merge_sort(resultado, chave=lambda a: a.fim)

    def relatorio_ordenado_por_duracao(self, decrescente=False):
        """Retorna os atendimentos finalizados ordenados por duração (MergeSort)."""
        finalizados = [a for a in self.historico_geral if a.duracao_minutos is not None]
        ordenados = merge_sort(finalizados, chave=lambda a: a.duracao_minutos)
        if decrescente:
            ordenados = list(reversed(ordenados))
        return ordenados

    def top5_clientes_mais_atendidos(self):
        """Retorna até 5 clientes com mais atendimentos finalizados (MergeSort)."""
        contagem = {}
        for atendimento in self.historico_geral:
            contagem[atendimento.cliente_id] = contagem.get(atendimento.cliente_id, 0) + 1

        pares = list(contagem.items())  # [(cliente_id, total), ...]
        ordenados = merge_sort(pares, chave=lambda par: -par[1])

        resultado = []
        for cliente_id, total in ordenados[:5]:
            cliente = self.buscar_cliente_por_id(cliente_id)
            nome = cliente.nome if cliente else f"Cliente {cliente_id}"
            resultado.append((cliente_id, nome, total))

        return resultado

    def exportar_relatorio_csv(self, nome_arquivo=None):
        """Exporta o histórico geral de atendimentos para CSV."""
        dados = [a.to_dict() for a in self.historico_geral]
        return persistencia.exportar_atendimentos_csv(dados, nome_arquivo)

    # ------------------------------------------------------------------
    # Persistência
    # ------------------------------------------------------------------
    def salvar_dados(self):
        """Salva clientes, atendentes e atendimentos em arquivos JSON."""
        clientes_dicts = [c.to_dict() for c in self.clientes_ativos]
        atendentes_dicts = [a.to_dict() for a in self.atendentes]
        atendimentos_dicts = [a.to_dict() for a in self.historico_geral]

        persistencia.salvar_clientes(clientes_dicts)
        persistencia.salvar_atendentes(atendentes_dicts)
        persistencia.salvar_atendimentos(atendimentos_dicts)

        logger.info("Dados salvos em /data com sucesso.")
