# Sistema Completo de Atendimento e Análise

## Objetivo

Projeto acadêmico/pedagógico que implementa, **manualmente** (sem usar
`queue.Queue`, `collections.deque` ou `.sort()`), as principais estruturas
de dados clássicas — Lista Encadeada, Fila Simples, Fila de Prioridade,
Pilha, Vetor Ordenado com Busca Binária e MergeSort — aplicadas a um
sistema realista de gerenciamento de filas de atendimento ao cliente.

## Pré-requisitos

- Python 3.8 ou superior
- Nenhuma dependência externa (apenas biblioteca padrão)

## Como executar

```bash
# A partir da pasta raiz do projeto (sistema/)
python3 main.py
```

O sistema inicia com dados de exemplo (clientes, atendentes e histórico)
já carregados, exibindo um menu interativo no terminal.

### Executando os testes

```bash
python3 -m unittest tests.py -v
```

## Estrutura do Projeto

```
sistema/
├── data/                     # Persistência (JSON/CSV) e logs (gerados em runtime)
├── models/
│   ├── no.py                 # Nó genérico para estruturas encadeadas
│   ├── lista_encadeada.py     # Lista Encadeada Simples
│   ├── fila.py               # Fila comum e Fila de Prioridade
│   ├── pilha.py               # Pilha (LIFO)
│   ├── vetor_ordenado.py      # Vetor Ordenado + Busca Binária + MergeSort
│   └── entidades.py           # Cliente, Atendente, Atendimento
├── services/
│   ├── persistencia.py        # Salvar/carregar JSON, exportar CSV, logging
│   └── atendimento_service.py # Regras de negócio (GerenciadorAtendimento)
├── view/
│   └── menu.py                # Interface de terminal (menu interativo)
├── dados_exemplo.py           # Dados iniciais para teste imediato
├── main.py                    # Ponto de entrada
├── tests.py                   # Testes unitários
├── requirements.txt
└── README.md
```

## Funcionalidades

- Cadastro de clientes (com prioridade 1-3) e atendentes.
- Fila de prioridade: clientes com prioridade mais alta são chamados
  primeiro; dentro do mesmo nível, a ordem de chegada (FIFO) é preservada.
- Fluxo completo: cliente entra na fila → é chamado → atendimento é
  finalizado (registrando atendente, data e duração) → vai para o
  histórico do cliente.
- **Desfazer**: reverte a última finalização usando uma Pilha,
  retornando o atendimento ao estado "em andamento".
- Regras de integridade: não é possível finalizar sem cliente em
  atendimento, nem remover cliente com atendimento ativo.
- Busca de cliente por ID via Busca Binária recursiva sobre vetor
  ordenado.
- Relatórios: tempo médio de atendimento, ordenação por duração
  (MergeSort), Top 5 clientes mais atendidos, filtro por intervalo de
  datas e exportação para CSV.
- Persistência em JSON (`/data`) e log de operações (`/data/sistema.log`).

## Observações de Implementação

Todas as estruturas (`ListaEncadeada`, `Fila`, `FilaPrioridade`, `Pilha`,
`VetorOrdenado`) e algoritmos (`merge_sort`, `busca_binaria`) foram
implementados do zero usando POO, com recursão aplicada na **Busca
Binária** e no **MergeSort**.
