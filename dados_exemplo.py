"""Script de dados de exemplo para popular o sistema imediatamente."""

from datetime import datetime, timedelta

from services.atendimento_service import GerenciadorAtendimento


def popular_dados_exemplo(gerenciador: GerenciadorAtendimento):
    """Popula o gerenciador com clientes, atendentes e histórico de exemplo."""

    # Atendentes
    ana = gerenciador.cadastrar_atendente("Ana Souza")
    bruno = gerenciador.cadastrar_atendente("Bruno Lima")

    # Clientes (variando prioridades)
    gerenciador.cadastrar_cliente("Carlos Pereira", prioridade=2)
    gerenciador.cadastrar_cliente("Daniela Alves", prioridade=1)
    gerenciador.cadastrar_cliente("Eduardo Santos", prioridade=3)
    gerenciador.cadastrar_cliente("Fernanda Costa", prioridade=1)
    gerenciador.cadastrar_cliente("Gustavo Lima", prioridade=2)

    # Simula alguns atendimentos já finalizados (histórico) manipulando
    # diretamente o histórico geral, para fins de demonstração de relatórios.
    agora = datetime.now()

    cliente1 = gerenciador.buscar_cliente_por_id(1)
    cliente2 = gerenciador.buscar_cliente_por_id(2)

    from models.entidades import Atendimento

    atendimento_a = Atendimento(
        id_atendimento=gerenciador._proximo_id_atendimento,
        cliente_id=cliente1.id,
        atendente_id=ana.id,
        inicio=agora - timedelta(days=2, minutes=20),
        fim=agora - timedelta(days=2, minutes=5),
    )
    atendimento_a.duracao_minutos = 15.0
    gerenciador._proximo_id_atendimento += 1

    atendimento_b = Atendimento(
        id_atendimento=gerenciador._proximo_id_atendimento,
        cliente_id=cliente2.id,
        atendente_id=bruno.id,
        inicio=agora - timedelta(days=1, minutes=30),
        fim=agora - timedelta(days=1, minutes=10),
    )
    atendimento_b.duracao_minutos = 20.0
    gerenciador._proximo_id_atendimento += 1

    cliente1.historico.inserir_fim(atendimento_a)
    cliente2.historico.inserir_fim(atendimento_b)
    gerenciador.historico_geral.append(atendimento_a)
    gerenciador.historico_geral.append(atendimento_b)

    return gerenciador
