"""Interface de usuário via terminal (menu interativo)."""

from datetime import datetime

from services.atendimento_service import GerenciadorAtendimento


def linha():
    print("-" * 50)


def menu_principal():
    print("\n" + "=" * 50)
    print("   SISTEMA DE ATENDIMENTO E ANÁLISE")
    print("=" * 50)
    print("1. Cadastrar cliente")
    print("2. Cadastrar atendente")
    print("3. Listar clientes ativos")
    print("4. Listar fila de espera")
    print("5. Chamar próximo cliente")
    print("6. Finalizar atendimento atual")
    print("7. Desfazer última finalização")
    print("8. Remover cliente")
    print("9. Buscar cliente por ID (Busca Binária)")
    print("10. Relatório: tempo médio de atendimento")
    print("11. Relatório: atendimentos ordenados por duração")
    print("12. Relatório: top 5 clientes mais atendidos")
    print("13. Relatório: filtrar atendimentos por data")
    print("14. Exportar relatório para CSV")
    print("15. Salvar dados (JSON)")
    print("0. Sair")
    linha()


def ler_inteiro(mensagem):
    """Lê um inteiro do usuário com tratamento de erro."""
    while True:
        try:
            return int(input(mensagem).strip())
        except ValueError:
            print("Entrada inválida. Digite um número inteiro.")


def ler_data(mensagem):
    """Lê uma data no formato dd/mm/aaaa."""
    while True:
        try:
            texto = input(mensagem).strip()
            return datetime.strptime(texto, "%d/%m/%Y")
        except ValueError:
            print("Formato inválido. Use dd/mm/aaaa (ex: 25/12/2025).")


def acao_cadastrar_cliente(gerenciador):
    nome = input("Nome do cliente: ").strip()
    print("Prioridade: 1 = Alta, 2 = Média, 3 = Normal")
    prioridade = ler_inteiro("Prioridade (1-3): ")
    try:
        cliente = gerenciador.cadastrar_cliente(nome, prioridade)
        print(f"Cliente cadastrado com sucesso: {cliente}")
    except ValueError as erro:
        print(f"Erro: {erro}")


def acao_cadastrar_atendente(gerenciador):
    nome = input("Nome do atendente: ").strip()
    try:
        atendente = gerenciador.cadastrar_atendente(nome)
        print(f"Atendente cadastrado com sucesso: {atendente}")
    except ValueError as erro:
        print(f"Erro: {erro}")


def acao_listar_clientes_ativos(gerenciador):
    clientes = gerenciador.clientes_ativos.para_lista()
    if not clientes:
        print("Nenhum cliente ativo no momento.")
        return
    linha()
    for cliente in clientes:
        print(cliente)
    linha()


def acao_listar_fila_espera(gerenciador):
    if gerenciador.fila_espera.esta_vazia():
        print("A fila de espera está vazia.")
        return
    linha()
    posicao = 1
    for cliente in gerenciador.fila_espera:
        print(f"{posicao}. {cliente.nome} (ID {cliente.id}, prioridade {cliente.prioridade})")
        posicao += 1
    linha()


def acao_chamar_proximo(gerenciador):
    try:
        cliente, atendimento = gerenciador.chamar_proximo()
        print(f"Cliente chamado: {cliente.nome} (ID {cliente.id})")
        print(f"Atendimento iniciado em: {atendimento.inicio.strftime('%d/%m/%Y %H:%M:%S')}")
    except ValueError as erro:
        print(f"Erro: {erro}")


def acao_finalizar_atendimento(gerenciador):
    if gerenciador.atendimento_atual is None:
        print("Não há atendimento em andamento.")
        return

    if not gerenciador.atendentes:
        print("Não há atendentes cadastrados. Cadastre um atendente primeiro.")
        return

    print("Atendentes disponíveis:")
    for atendente in gerenciador.atendentes:
        print(f"  ID {atendente.id} - {atendente.nome}")

    id_atendente = ler_inteiro("ID do atendente responsável: ")
    try:
        atendimento = gerenciador.finalizar_atendimento(id_atendente)
        print(f"Atendimento finalizado. Duração: {atendimento.duracao_minutos} minutos.")
    except ValueError as erro:
        print(f"Erro: {erro}")


def acao_desfazer(gerenciador):
    try:
        cliente, atendimento = gerenciador.desfazer_ultima_finalizacao()
        print(f"Última finalização desfeita. Cliente '{cliente.nome}' "
              f"voltou ao atendimento (atendimento ID {atendimento.id}).")
    except ValueError as erro:
        print(f"Erro: {erro}")


def acao_remover_cliente(gerenciador):
    id_cliente = ler_inteiro("ID do cliente a remover: ")
    try:
        removido = gerenciador.remover_cliente(id_cliente)
        if removido is None:
            print("Cliente não encontrado.")
        else:
            print(f"Cliente removido: {removido.nome}")
    except ValueError as erro:
        print(f"Erro: {erro}")


def acao_buscar_cliente(gerenciador):
    id_cliente = ler_inteiro("ID do cliente a buscar: ")
    cliente = gerenciador.buscar_cliente_por_id(id_cliente)
    if cliente is None:
        print("Cliente não encontrado.")
    else:
        print(f"Cliente encontrado: {cliente}")


def acao_tempo_medio(gerenciador):
    media = gerenciador.tempo_medio_atendimento()
    print(f"Tempo médio de atendimento: {media} minutos.")


def acao_relatorio_duracao(gerenciador):
    ordenados = gerenciador.relatorio_ordenado_por_duracao()
    if not ordenados:
        print("Nenhum atendimento finalizado ainda.")
        return
    linha()
    for atendimento in ordenados:
        print(f"Atendimento {atendimento.id} - Cliente {atendimento.cliente_id} "
              f"- Duração: {atendimento.duracao_minutos} min")
    linha()


def acao_top5(gerenciador):
    top5 = gerenciador.top5_clientes_mais_atendidos()
    if not top5:
        print("Nenhum atendimento finalizado ainda.")
        return
    linha()
    for posicao, (cliente_id, nome, total) in enumerate(top5, start=1):
        print(f"{posicao}. {nome} (ID {cliente_id}) - {total} atendimento(s)")
    linha()


def acao_filtrar_por_data(gerenciador):
    print("Informe o intervalo de datas para o filtro.")
    data_inicio = ler_data("Data de início (dd/mm/aaaa): ")
    data_fim = ler_data("Data de fim (dd/mm/aaaa): ")
    # Ajusta para incluir o dia inteiro na data final.
    data_fim = data_fim.replace(hour=23, minute=59, second=59)

    try:
        resultados = gerenciador.filtrar_por_data(data_inicio, data_fim)
        if not resultados:
            print("Nenhum atendimento encontrado nesse intervalo.")
            return
        linha()
        for atendimento in resultados:
            print(f"Atendimento {atendimento.id} - Cliente {atendimento.cliente_id} "
                  f"- Fim: {atendimento.fim.strftime('%d/%m/%Y %H:%M')}")
        linha()
    except ValueError as erro:
        print(f"Erro: {erro}")


def acao_exportar_csv(gerenciador):
    try:
        caminho = gerenciador.exportar_relatorio_csv()
        print(f"Relatório exportado para: {caminho}")
    except OSError as erro:
        print(f"Erro ao exportar: {erro}")


def acao_salvar_dados(gerenciador):
    try:
        gerenciador.salvar_dados()
        print("Dados salvos com sucesso na pasta /data.")
    except OSError as erro:
        print(f"Erro ao salvar dados: {erro}")


def executar_menu(gerenciador: GerenciadorAtendimento):
    """Loop principal do menu interativo."""
    acoes = {
        "1": acao_cadastrar_cliente,
        "2": acao_cadastrar_atendente,
        "3": acao_listar_clientes_ativos,
        "4": acao_listar_fila_espera,
        "5": acao_chamar_proximo,
        "6": acao_finalizar_atendimento,
        "7": acao_desfazer,
        "8": acao_remover_cliente,
        "9": acao_buscar_cliente,
        "10": acao_tempo_medio,
        "11": acao_relatorio_duracao,
        "12": acao_top5,
        "13": acao_filtrar_por_data,
        "14": acao_exportar_csv,
        "15": acao_salvar_dados,
    }

    while True:
        menu_principal()
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "0":
            print("Encerrando o sistema. Até logo!")
            break

        acao = acoes.get(opcao)
        if acao is None:
            print("Opção inválida. Tente novamente.")
            continue

        try:
            acao(gerenciador)
        except Exception as erro:  # pylint: disable=broad-except
            print(f"Ocorreu um erro inesperado: {erro}")

        input("\nPressione ENTER para continuar...")
