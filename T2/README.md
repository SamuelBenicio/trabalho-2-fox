# Trabalho 2 — Fox And Names

## Problema

**Codeforces 510C — Fox And Names** (<https://codeforces.com/problemset/problem/510/C>).

Dada uma lista de nomes, decidir se existe uma ordem para as 26 letras que torne a lista lexicograficamente ordenada e, se existir, exibir uma dessas ordens. Caso contrário, exibir `Impossible`.

## Integrantes

- Samuel Ribeiro Benicio - 2310281
- Adriel Medeiros Lins – 2013246
- Manoel Sergio Costa Lima - 2422973

## Linguagem

Python 3, usando as implementações de referência de `algs4-py`.

## Execução

A partir da pasta `T2`:

```bash
# executar com uma entrada
python3 src/main.py < entrada.txt

# exemplo
printf '3\nrivest\nshamir\nadleman\n' | python3 src/main.py

# executar todos os casos de teste
python3 dados/testar.py
```

Não há dependências externas.

## Modelagem

- **Vértices:** as 26 letras (`a` → 0, …, `z` → 25).
- **Arestas:** para cada par de nomes consecutivos, a primeira posição em que diferem gera a aresta `x -> y` ("`x` vem antes de `y`").
- **Classificação:** grafo direcionado, simples (arestas repetidas são descartadas), não ponderado e possivelmente desconexo.

## Propriedade estrutural

Existe resposta se e somente se o grafo de precedência é um **DAG** (não possui ciclo direcionado). Um ciclo representa restrições contraditórias. Se o grafo é um DAG, qualquer **ordenação topológica** é uma resposta válida.

## Algoritmo

1. Comparar nomes consecutivos e criar as arestas; se um nome aparece antes de um prefixo seu, responder `Impossible`.
2. Detectar ciclo com DFS (`DirectedCycle`, vetor `on_stack`); se houver, responder `Impossible`.
3. Caso contrário, obter a pós-ordem reversa da DFS (`DepthFirstOrder`) e convertê-la em letras.

## Implementação de referência

`algs4-py/algs4`: `Bag`, `Digraph`, `DirectedCycle`, `DepthFirstOrder` e `Topological` (além de `Node` e `LinkIterator`, dependências de `Bag`). As classes foram copiadas para `src/main.py`, pois o Codeforces aceita apenas um arquivo.

## Alterações e justificativas

Nenhuma classe teve a lógica alterada; foram removidos apenas trechos não usados: blocos `__main__`, leitura de grafo por arquivo, `__str__`, métodos auxiliares de `Digraph` e o uso de `SymbolDigraph` em `Topological`. O código específico do problema (`construir_grafo`, `resolver`, `main`) faz a extração das arestas, o teste de prefixo, o descarte de arestas repetidas e a conversão para letras. Detalhes em [`acompanhamento/marco-4.md`](acompanhamento/marco-4.md).

## Complexidade

- **Tempo:** `O(nL + V + E)`, com `V = 26` e `E ≤ n - 1`.
- **Memória:** `O(V + E)` para o grafo e `O(V² + nL)` auxiliar (matriz de arestas repetidas e nomes lidos).

## Casos especiais

- Nome maior antes do seu prefixo (`abc`, `ab`): `Impossible` sem executar a busca.
- Prefixo válido (`ab`, `abc`): nenhuma aresta.
- Letras que não aparecem: vértices isolados, entram em qualquer posição.
- Um único nome: qualquer permutação é válida.
- Arestas repetidas: descartadas.
- Ciclos de qualquer tamanho: `Impossible`.

## Evidência do `Accepted`

- **Submissão:** [393638964](https://codeforces.com/problemset/submission/510/393638964) — `Accepted`, Python 3, 62 ms, 800 KB
- **Captura:** [`evidencias/accepted.png`](evidencias/accepted.png)

## Uso de IA

_Declarar aqui como a IA foi usada no trabalho._

## Estrutura

- `acompanhamento/`: registros dos marcos do trabalho.
- `src/`: código-fonte da solução.
- `evidencias/`: evidência do `Accepted`.
- `apresentacao/`: arquivo da apresentação.
- `dados/`: casos de teste e verificador.
