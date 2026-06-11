"""Serviço de persistência (JSON/CSV) e configuração de logging.

Centraliza a leitura/escrita dos dados do sistema na pasta /data.
"""

import csv
import json
import logging
import os
from datetime import datetime

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
CLIENTES_JSON = os.path.join(DATA_DIR, "clientes.json")
ATENDENTES_JSON = os.path.join(DATA_DIR, "atendentes.json")
ATENDIMENTOS_JSON = os.path.join(DATA_DIR, "atendimentos.json")
LOG_FILE = os.path.join(DATA_DIR, "sistema.log")


def configurar_logging():
    """Configura o logger principal do sistema (arquivo + console)."""
    os.makedirs(DATA_DIR, exist_ok=True)

    logger = logging.getLogger("atendimento")
    logger.setLevel(logging.INFO)

    if logger.handlers:
        return logger  # evita handlers duplicados em chamadas repetidas

    formato = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
    )

    arquivo = logging.FileHandler(LOG_FILE, encoding="utf-8")
    arquivo.setFormatter(formato)

    console = logging.StreamHandler()
    console.setFormatter(formato)

    logger.addHandler(arquivo)
    logger.addHandler(console)
    return logger


logger = configurar_logging()


def _salvar_json(caminho, dados):
    """Salva uma lista de dicionários em um arquivo JSON."""
    try:
        os.makedirs(DATA_DIR, exist_ok=True)
        with open(caminho, "w", encoding="utf-8") as arquivo:
            json.dump(dados, arquivo, ensure_ascii=False, indent=2)
    except OSError as erro:
        logger.error("Erro ao salvar arquivo %s: %s", caminho, erro)
        raise


def _carregar_json(caminho):
    """Carrega uma lista de dicionários de um arquivo JSON. Retorna [] se não existir."""
    if not os.path.exists(caminho):
        return []
    try:
        with open(caminho, "r", encoding="utf-8") as arquivo:
            return json.load(arquivo)
    except (OSError, json.JSONDecodeError) as erro:
        logger.error("Erro ao carregar arquivo %s: %s", caminho, erro)
        return []


def salvar_clientes(clientes_dicts):
    _salvar_json(CLIENTES_JSON, clientes_dicts)


def carregar_clientes():
    return _carregar_json(CLIENTES_JSON)


def salvar_atendentes(atendentes_dicts):
    _salvar_json(ATENDENTES_JSON, atendentes_dicts)


def carregar_atendentes():
    return _carregar_json(ATENDENTES_JSON)


def salvar_atendimentos(atendimentos_dicts):
    _salvar_json(ATENDIMENTOS_JSON, atendimentos_dicts)


def carregar_atendimentos():
    return _carregar_json(ATENDIMENTOS_JSON)


def exportar_atendimentos_csv(atendimentos_dicts, nome_arquivo=None):
    """Exporta a lista de atendimentos (dicts) para um arquivo CSV em /data."""
    os.makedirs(DATA_DIR, exist_ok=True)

    if nome_arquivo is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        nome_arquivo = f"relatorio_atendimentos_{timestamp}.csv"

    caminho = os.path.join(DATA_DIR, nome_arquivo)

    if not atendimentos_dicts:
        colunas = ["id", "cliente_id", "atendente_id", "inicio", "fim", "duracao_minutos"]
    else:
        colunas = list(atendimentos_dicts[0].keys())

    try:
        with open(caminho, "w", newline="", encoding="utf-8") as arquivo:
            escritor = csv.DictWriter(arquivo, fieldnames=colunas)
            escritor.writeheader()
            for linha in atendimentos_dicts:
                escritor.writerow(linha)
        logger.info("Relatório CSV exportado para %s", caminho)
        return caminho
    except OSError as erro:
        logger.error("Erro ao exportar CSV: %s", erro)
        raise
