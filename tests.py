"""Testes unitários básicos para estruturas de dados e serviços."""

import unittest
from datetime import datetime, timedelta

from models.fila import Fila, FilaPrioridade
from models.lista_encadeada import ListaEncadeada
from models.pilha import Pilha
from models.vetor_ordenado import VetorOrdenado, merge_sort
from services.atendimento_service import GerenciadorAtendimento


class TestFila(unittest.TestCase):
    def test_fifo_basico(self):
        fila = Fila()
        fila.enfileirar("A")
        fila.enfileirar("B")
        fila.enfileirar("C")
        self.assertEqual(fila.desenfileirar(), "A")
        self.assertEqual(fila.desenfileirar(), "B")
        self.assertEqual(len(fila), 1)

    def test_fila_vazia(self):
        fila = Fila()
        self.assertTrue(fila.esta_vazia())
        self.assertIsNone(fila.desenfileirar())


class TestFilaPrioridade(unittest.TestCase):
    def test_prioridade_respeita_ordem_chegada(self):
        fila = FilaPrioridade(niveis=3)
        fila.enfileirar("Cliente1-P2", prioridade=2)
        fila.enfileirar("Cliente2-P1", prioridade=1)
        fila.enfileirar("Cliente3-P1", prioridade=1)
        fila.enfileirar("Cliente4-P2", prioridade=2)

        # Prioridade 1 primeiro, na ordem de chegada.
        self.assertEqual(fila.desenfileirar(), "Cliente2-P1")
        self.assertEqual(fila.desenfileirar(), "Cliente3-P1")
        # Depois prioridade 2, na ordem de chegada.
        self.assertEqual(fila.desenfileirar(), "Cliente1-P2")
        self.assertEqual(fila.desenfileirar(), "Cliente4-P2")

    def test_prioridade_invalida(self):
        fila = FilaPrioridade(niveis=3)
        with self.assertRaises(ValueError):
            fila.enfileirar("X", prioridade=5)


class TestListaEncadeada(unittest.TestCase):
    def test_inserir_e_buscar(self):
        lista = ListaEncadeada()
        lista.inserir_fim(10)
        lista.inserir_fim(20)
        lista.inserir_fim(30)
        self.assertEqual(len(lista), 3)
        self.assertEqual(lista.buscar(lambda x: x == 20), 20)

    def test_remover(self):
        lista = ListaEncadeada()
        lista.inserir_fim(1)
        lista.inserir_fim(2)
        lista.inserir_fim(3)
        removido = lista.remover(lambda x: x == 2)
        self.assertEqual(removido, 2)
        self.assertEqual(lista.para_lista(), [1, 3])
        self.assertIsNone(lista.remover(lambda x: x == 99))


class TestPilha(unittest.TestCase):
    def test_lifo(self):
        pilha = Pilha()
        pilha.empilhar("primeiro")
        pilha.empilhar("segundo")
        pilha.empilhar("terceiro")
        self.assertEqual(pilha.desempilhar(), "terceiro")
        self.assertEqual(pilha.desempilhar(), "segundo")
        self.assertEqual(len(pilha), 1)

    def test_pilha_vazia(self):
        pilha = Pilha()
        self.assertTrue(pilha.esta_vazia())
        self.assertIsNone(pilha.desempilhar())


class TestVetorOrdenadoEBuscaBinaria(unittest.TestCase):
    def test_insercao_mantem_ordem(self):
        vetor = VetorOrdenado(chave=lambda x: x)
        for valor in [5, 1, 3, 2, 4]:
            vetor.inserir(valor)
        self.assertEqual(vetor.para_lista(), [1, 2, 3, 4, 5])

    def test_busca_binaria_encontra(self):
        vetor = VetorOrdenado(chave=lambda x: x)
        for valor in [10, 20, 30, 40, 50]:
            vetor.inserir(valor)
        self.assertEqual(vetor.busca_binaria(30), 30)
        self.assertIsNone(vetor.busca_binaria(99))


class TestMergeSort(unittest.TestCase):
    def test_ordenacao_simples(self):
        dados = [5, 3, 1, 4, 2]
        resultado = merge_sort(dados)
        self.assertEqual(resultado, [1, 2, 3, 4, 5])

    def test_lista_original_inalterada(self):
        dados = [5, 3, 1]
        merge_sort(dados)
        self.assertEqual(dados, [5, 3, 1])

    def test_ordenacao_por_chave(self):
        dados = [("b", 2), ("a", 1), ("c", 3)]
        resultado = merge_sort(dados, chave=lambda item: item[1])
        self.assertEqual(resultado, [("a", 1), ("b", 2), ("c", 3)])


class TestGerenciadorAtendimento(unittest.TestCase):
    def setUp(self):
        self.gerenciador = GerenciadorAtendimento()

    def test_cadastro_e_busca_cliente(self):
        cliente = self.gerenciador.cadastrar_cliente("Maria", prioridade=1)
        encontrado = self.gerenciador.buscar_cliente_por_id(cliente.id)
        self.assertEqual(encontrado.nome, "Maria")

    def test_fluxo_atendimento_completo(self):
        self.gerenciador.cadastrar_cliente("João", prioridade=2)
        atendente = self.gerenciador.cadastrar_atendente("Pedro")

        cliente, atendimento = self.gerenciador.chamar_proximo()
        self.assertEqual(cliente.nome, "João")
        self.assertTrue(cliente.atendimento_ativo)

        finalizado = self.gerenciador.finalizar_atendimento(atendente.id)
        self.assertFalse(cliente.atendimento_ativo)
        self.assertIsNotNone(finalizado.duracao_minutos)
        self.assertEqual(len(self.gerenciador.historico_geral), 1)

    def test_finalizar_sem_atendimento_levanta_erro(self):
        with self.assertRaises(ValueError):
            self.gerenciador.finalizar_atendimento(1)

    def test_chamar_proximo_fila_vazia_levanta_erro(self):
        with self.assertRaises(ValueError):
            self.gerenciador.chamar_proximo()

    def test_remover_cliente_em_atendimento_levanta_erro(self):
        cliente = self.gerenciador.cadastrar_cliente("Lucas", prioridade=3)
        self.gerenciador.chamar_proximo()
        with self.assertRaises(ValueError):
            self.gerenciador.remover_cliente(cliente.id)

    def test_desfazer_ultima_finalizacao(self):
        self.gerenciador.cadastrar_cliente("Sofia", prioridade=1)
        atendente = self.gerenciador.cadastrar_atendente("Carla")

        cliente, _ = self.gerenciador.chamar_proximo()
        self.gerenciador.finalizar_atendimento(atendente.id)
        self.assertEqual(len(self.gerenciador.historico_geral), 1)

        cliente_desfeito, atendimento_desfeito = self.gerenciador.desfazer_ultima_finalizacao()
        self.assertEqual(cliente_desfeito.id, cliente.id)
        self.assertTrue(cliente_desfeito.atendimento_ativo)
        self.assertEqual(len(self.gerenciador.historico_geral), 0)
        self.assertIsNotNone(self.gerenciador.atendimento_atual)

    def test_desfazer_sem_acoes_levanta_erro(self):
        with self.assertRaises(ValueError):
            self.gerenciador.desfazer_ultima_finalizacao()

    def test_tempo_medio_atendimento(self):
        self.gerenciador.cadastrar_cliente("Cliente A", prioridade=2)
        atendente = self.gerenciador.cadastrar_atendente("Atendente A")
        self.gerenciador.chamar_proximo()
        atendimento = self.gerenciador.finalizar_atendimento(atendente.id)
        # Força uma duração conhecida para o teste.
        atendimento.duracao_minutos = 10.0
        self.gerenciador.historico_geral[0].duracao_minutos = 10.0
        media = self.gerenciador.tempo_medio_atendimento()
        self.assertEqual(media, 10.0)

    def test_filtrar_por_data_invalida(self):
        agora = datetime.now()
        with self.assertRaises(ValueError):
            self.gerenciador.filtrar_por_data(agora, agora - timedelta(days=1))


if __name__ == "__main__":
    unittest.main()
