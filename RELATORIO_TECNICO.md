# Relatório Técnico de Estruturas de Dados e Complexidade (Big-O)

## 1. Lista Encadeada (Clientes Ativos)

**Justificativa:** clientes são frequentemente removidos (inativados) do
meio da coleção quando finalizam seu vínculo com o sistema. Uma lista
encadeada permite remoção sem necessidade de deslocar elementos
subsequentes (como ocorreria em um array), e seu crescimento é dinâmico,
sem necessidade de realocação.

**Complexidades:**
- Inserção no fim: O(n) — percorre até o último nó (poderia ser O(1) com
  ponteiro de cauda, mas o tamanho da lista de clientes ativos é pequeno
  o suficiente para não justificar a complexidade adicional).
- Busca por condição: O(n) — percurso sequencial.
- Remoção por condição: O(n) — busca + ajuste de ponteiros, sem cópia de
  elementos.

## 2. Fila Simples (Fila)

**Justificativa:** representa naturalmente o comportamento FIFO (First
In, First Out) de uma fila de espera. A implementação com ponteiros de
frente e traseira evita o custo O(n) de remoção no início que ocorreria
com um array Python (`list.pop(0)`).

**Complexidades:**
- Enfileirar: O(1)
- Desenfileirar: O(1)
- Espiar (peek): O(1)

## 3. Fila de Prioridade (FilaPrioridade)

**Justificativa:** o sistema exige que clientes de maior prioridade sejam
atendidos primeiro, mas que, dentro do mesmo nível de prioridade, a ordem
de chegada seja respeitada. A solução adotada — um array de filas FIFO
simples, uma para cada nível de prioridade — atende exatamente a esse
requisito sem necessidade de heaps (que não preservariam a ordem de
chegada de forma trivial) e mantém as operações extremamente simples e
eficientes.

**Complexidades:**
- Enfileirar: O(1) — insere diretamente na fila do nível correspondente.
- Desenfileirar: O(P), onde P é o número de níveis de prioridade
  (constante, P=3 no projeto) — na prática O(1).
- Espiar: O(P) ≈ O(1).

## 4. Pilha (Pilha — Desfazer)

**Justificativa:** a operação "desfazer" segue naturalmente a semântica
LIFO (Last In, First Out): a última ação realizada é a primeira a ser
revertida. A pilha encadeada permite empilhar/desempilhar em tempo
constante, sem limite de tamanho pré-definido.

**Complexidades:**
- Empilhar: O(1)
- Desempilhar: O(1)
- Espiar: O(1)

## 5. Vetor Ordenado + Busca Binária (Busca por ID)

**Justificativa:** consultas por ID de cliente são uma operação
frequente (validações, finalização de atendimento, relatórios). Manter
um vetor ordenado por ID permite usar Busca Binária, reduzindo
drasticamente o custo de busca em relação a uma busca linear,
especialmente à medida que a base de clientes cresce.

**Complexidades:**
- Inserção (mantendo ordenação): O(n) — busca da posição correta (O(n)
  na implementação atual, que usa busca linear para encontrar o ponto de
  inserção) + deslocamento de elementos no array (`list.insert`).
- Busca Binária (recursiva): O(log n) — a cada chamada recursiva, o
  espaço de busca é dividido pela metade.
- Remoção: O(n) — busca linear + remoção com deslocamento.

> Trade-off: a inserção é mais cara que em uma lista encadeada, mas em
> compensação a busca por ID — operação muito mais frequente no sistema
> — passa de O(n) para O(log n).

## 6. MergeSort (Relatórios e Ordenações)

**Justificativa:** o MergeSort foi escolhido por ser um algoritmo
**estável** (preserva a ordem relativa de elementos com chaves iguais,
importante por exemplo no relatório de Top 5 clientes), com complexidade
de pior caso garantida de O(n log n), independentemente da distribuição
dos dados de entrada — diferente do QuickSort, cujo pior caso é O(n²).

**Complexidades:**
- Tempo: O(n log n) em todos os casos (melhor, médio e pior).
- Espaço: O(n) — cria sublistas auxiliares durante a divisão e a
  combinação (merge).

## 7. Recursão

A recursão foi aplicada em dois pontos centrais do sistema:

1. **Busca Binária** (`VetorOrdenado._busca_binaria_rec`): a cada chamada,
   o intervalo de busca `[inicio, fim]` é reduzido pela metade, com caso
   base quando `inicio > fim` (não encontrado) ou quando o elemento do
   meio é igual ao valor procurado.
2. **MergeSort** (`merge_sort`): a lista é dividida recursivamente ao
   meio até sublistas de tamanho 0 ou 1 (caso base), que são então
   combinadas (merge) de volta, em ordem, na recursão de retorno.

## 8. Resumo das Operações Principais do Sistema

| Operação                                   | Estrutura            | Complexidade |
|--------------------------------------------|----------------------|--------------|
| Cadastrar cliente                          | Lista Encadeada + Vetor Ordenado | O(n) |
| Buscar cliente por ID                      | Vetor Ordenado (Busca Binária)   | O(log n) |
| Remover cliente da lista de ativos         | Lista Encadeada      | O(n) |
| Inserir cliente na fila de espera          | Fila de Prioridade   | O(1) |
| Chamar próximo cliente (desenfileirar)     | Fila de Prioridade   | O(P) ≈ O(1) |
| Finalizar atendimento (empilhar p/ desfazer)| Pilha               | O(1) |
| Desfazer última finalização                | Pilha                | O(1) |
| Ordenar atendimentos por duração/relatórios| MergeSort            | O(n log n) |
