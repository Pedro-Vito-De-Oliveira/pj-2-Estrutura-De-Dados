"""Ponto de entrada do Sistema Completo de Atendimento e Análise."""

from dados_exemplo import popular_dados_exemplo
from services.atendimento_service import GerenciadorAtendimento
from view.menu import executar_menu


def main():
    gerenciador = GerenciadorAtendimento()
    popular_dados_exemplo(gerenciador)

    print("Sistema iniciado com dados de exemplo carregados.")
    executar_menu(gerenciador)


if __name__ == "__main__":
    main()
