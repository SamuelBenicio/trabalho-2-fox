# Marco 3

**Problema:** *Fox And Names* (Codeforces 510C).

**Escopo deste marco:** o grafo real do problema é **direcionado** e tem sempre **26 vértices** (as letras). Neste marco, seguindo a aula A5 (Grafos Eulerianos), deixamos esse grafo de lado e usamos uma **instância representativa não dirigida**, com vértices nomeados por letras, para rastrear manualmente o **algoritmo de Hierholzer** como foi apresentado em aula.

---

## 1. Propriedade estrutural central

**Circuito de Euler:** um passeio fechado que usa **todas as arestas exatamente uma vez**.

**Critério de reconhecimento (Teorema 2 da aula):** um grafo conexo tem circuito de Euler **se e somente se todo vértice tem grau par**.

- Se exatamente dois vértices têm grau ímpar, existe apenas **trilha** de Euler (Teorema 3), começando em um ímpar e terminando no outro.
- Se o grafo for desconexo (desconsiderando vértices isolados), não há circuito.

**Por que o grau par garante o funcionamento do Hierholzer:** cada vez que o passeio entra em um vértice por uma aresta, ele consome duas arestas desse vértice (entrada e saída). Com todos os graus pares, o único vértice onde o passeio pode "travar" (ficar sem aresta livre) é o vértice onde ele começou. Por isso cada passeio construído é sempre um **ciclo fechado**.

**Relação com o problema real:** no *Fox And Names*, a propriedade exigida é outra — o grafo de precedência precisa ser um **DAG**, e a resposta é uma **ordenação topológica**; a existência de ciclo leva a `Impossible` (ver Marco 1).

---

## 2. Implementações de referência (`algs4`)

Sem implementar código nesta etapa.

| Classe `algs4` | Papel | Adaptação prevista |
|---|---|---|
| `Graph` | Grafo não dirigido por listas de adjacência | Nenhuma; usado na instância deste marco |
| `EulerianCycle` | Hierholzer para grafo não dirigido (versão iterativa com pilha) | Nenhuma; serve de referência para o rastreamento |
| `Digraph` | Grafo direcionado das 26 letras (problema real) | Evitar arestas repetidas entre o mesmo par de letras |
| `DirectedCycle` | Detecta ciclo no dígrafo → `Impossible` | Nenhuma |
| `Topological` (`topological.py` no Python) | Ordem topológica → permutação do alfabeto | Converter índices `0..25` de volta para letras |

**Observação sobre `EulerianCycle`:** a implementação do `algs4` usa uma pilha e marca cada aresta como usada (`isUsed`). A ideia é a mesma do pseudocódigo da aula: quando o passeio trava, ele volta pela pilha até um vértice que ainda tem aresta livre e começa um subciclo ali. A diferença é que a "inserção" do subciclo `H` em `C` acontece implicitamente pela ordem em que os vértices saem da pilha.

---

## 3. Instância representativa

**V = 6, E = 9**, grafo simples, não dirigido e conexo.

```mermaid
graph LR
    a --- b
    b --- c
    c --- a
    b --- d
    d --- e
    e --- b
    c --- e
    e --- f
    f --- c
```

Arestas: `a-b`, `b-c`, `c-a`, `b-d`, `d-e`, `e-b`, `c-e`, `e-f`, `f-c`.

> **Entrada que gera a instância:**
>
> ```
> 10
> a
> b
> d
> e
> c
> f
> ea
> ba
> ca
> aa
> ```
>
> Comparando nomes consecutivos, obtêm-se as arestas dirigidas `a→b, b→d, d→e, e→c, c→f, f→e, e→b, b→c, c→a`.
> Ignorando o sentido, chega-se ao grafo acima.
> No problema real a saída seria `Impossible`, pois há ciclo (ex.: `a→b→c→a`) — a instância serve apenas para exercitar o Hierholzer.

### 3.1 Listas de adjacência (em ordem alfabética)

| Vértice | Adjacentes | Grau |
|---|---|---|
| a | b, c | 2 |
| b | a, c, d, e | 4 |
| c | a, b, e, f | 4 |
| d | b, e | 2 |
| e | b, c, d, f | 4 |
| f | c, e | 2 |

Soma dos graus = 18 = 2 · 9 ✔

### 3.2 Verificação do critério

- Conexo: sim (todos alcançáveis a partir de `a`).
- Todos os graus são pares.

Pelo Teorema 2, o grafo **é euleriano** → podemos aplicar Hierholzer.

### 3.3 Regra de escolha

O pseudocódigo da aula escolhe as arestas "aleatoriamente". Para o rastreamento ser reproduzível, fixamos: **sempre seguir a aresta livre para o vizinho de menor letra**, e, para escolher o vértice de início de um novo subciclo, **percorrer `C` da esquerda para a direita** e pegar o primeiro vértice com grau > 0 no grafo reduzido `K`.

---

## 4. Rastreamento manual do Hierholzer

Estruturas mantidas:
- `C`: ciclo principal (sequência de vértices).
- `H`: subciclo da iteração atual.
- `K`: grafo reduzido (arestas ainda não percorridas) e o grau `d(v)` de cada vértice em `K`.

### Passos 1–2: ciclo inicial a partir de `v = a`

| Passo | Vértice atual | Arestas livres | Escolha | Aresta removida | Passeio |
|---|---|---|---|---|---|
| 1 | a | b, c | b | a-b | a, b |
| 2 | b | c, d, e | c | b-c | a, b, c |
| 3 | c | a, e, f | a | c-a | a, b, c, a |
| 4 | a | — | trava no início | — | fechado |

`C = (a, b, c, a)` — 3 arestas.

### Passos 3–4: grafo reduzido `K`

Arestas restantes `A1`: `b-d`, `d-e`, `e-b`, `c-e`, `e-f`, `f-c` (6 arestas).

| v | a | b | c | d | e | f |
|---|---|---|---|---|---|---|
| d(v) em K | 0 | 2 | 2 | 2 | 4 | 2 |

`A1 ≠ ∅` → entra no laço.

### Iteração 1

**Escolha do vértice (passo 6):** percorrendo `C = (a, b, c, a)`: `a` tem grau 0; `b` tem grau 2 → **v = b**.

**Construção de H (passo 7):**

| Vértice atual | Arestas livres | Escolha | Aresta removida | Passeio |
|---|---|---|---|---|
| b | d, e | d | b-d | b, d |
| d | e | e | d-e | b, d, e |
| e | b, c, f | b | e-b | b, d, e, b |
| b | — | trava no início | — | fechado |

`H = (b, d, e, b)`

**União (passo 9):** substitui-se a primeira ocorrência de `b` em `C` por `H`:

```
C = (a, [b], c, a)  +  H = (b, d, e, b)
C = (a, b, d, e, b, c, a)
```

**K atualizado:** arestas restantes `c-e`, `e-f`, `f-c`.

| v | a | b | c | d | e | f |
|---|---|---|---|---|---|---|
| d(v) em K | 0 | 0 | 2 | 0 | 2 | 2 |

`A1 ≠ ∅` → continua.

### Iteração 2

**Escolha do vértice:** percorrendo `C = (a, b, d, e, b, c, a)`: `a` 0, `b` 0, `d` 0, `e` 2 → **v = e**.

**Construção de H:**

| Vértice atual | Arestas livres | Escolha | Aresta removida | Passeio |
|---|---|---|---|---|
| e | c, f | c | e-c | e, c |
| c | f | f | c-f | e, c, f |
| f | e | e | f-e | e, c, f, e |
| e | — | trava no início | — | fechado |

`H = (e, c, f, e)`

**União:** substitui-se a primeira ocorrência de `e` em `C` por `H`:

```
C = (a, b, d, [e], b, c, a)  +  H = (e, c, f, e)
C = (a, b, d, e, c, f, e, b, c, a)
```

**K atualizado:** nenhuma aresta restante → `A1 = ∅` → **fim do laço**.

### Resultado

**Circuito de Euler:** `a → b → d → e → c → f → e → b → c → a`

**Verificação:** 10 vértices na sequência = 9 arestas, e cada aresta aparece uma única vez:

| # | Aresta |
|---|---|
| 1 | a-b |
| 2 | b-d |
| 3 | d-e |
| 4 | e-c |
| 5 | c-f |
| 6 | f-e |
| 7 | e-b |
| 8 | b-c |
| 9 | c-a |

Todas as 9 arestas do grafo foram usadas exatamente uma vez, e o passeio começa e termina em `a` ✔

**Decisões do algoritmo, resumidas:**
- Os vértices de grau 4 (`b`, `c`, `e`) são exatamente os que aparecem duas vezes no circuito final — cada visita consome 2 arestas.
- `e` só foi escolhido como início da iteração 2 porque já pertencia a `C`; um subciclo sempre começa em um vértice de `C`, o que garante que a união continue sendo um único passeio fechado.

---

## 5. Complexidade

Sejam `V` vértices e `E` arestas.

**Tempo:**
- Verificar o critério (graus pares + conexidade por DFS): `O(V + E)`.
- Hierholzer: cada aresta é percorrida e removida uma única vez. Com listas encadeadas (como indicado na aula) ou com a marcação `isUsed` do `algs4`, a remoção e a consulta de adjacência custam `O(1)` amortizado, e a união de `H` em `C` é feita por ajuste de ponteiros em `O(1)`.
- **Total: `O(V + E)`**.

**Memória:**
- **Representação do grafo:** listas de adjacência, `O(V + E)` (em grafo não dirigido, cada aresta aparece em duas listas).
- **Memória auxiliar:** marcação de arestas usadas `O(E)`, ciclo `C` com `E + 1` vértices `O(E)`, pilha/subciclo `H` `O(E)` no pior caso, graus em `K` `O(V)`. Total auxiliar: `O(V + E)`.

**Na instância:** 9 arestas → 9 remoções; o ciclo final tem 10 posições.

**Problema real (para comparação):** o dígrafo tem `V = 26` fixo e no máximo 99 arestas (uma por par de nomes consecutivos). A coleta das arestas custa `O(n · L)` (`n ≤ 100`, `L ≤ 100`) e a ordenação topológica `O(V + E)`, ou seja, praticamente constante.
