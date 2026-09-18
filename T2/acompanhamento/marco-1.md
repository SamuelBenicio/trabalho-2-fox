# Marco 1 — Problema e conhecimento prévio

## Problema escolhido

**Fox And Names — Codeforces 510C**

Dada uma lista de nomes que aparece na ordem apresentada, deve-se descobrir se existe uma ordem personalizada para as 26 letras minúsculas do alfabeto que torne essa lista lexicograficamente ordenada. Caso exista, qualquer permutação válida das letras deve ser exibida. Caso contrário, deve ser exibida a palavra `Impossible`.

## Entrada, saída e restrições

### Entrada

- A primeira linha contém um inteiro `n`, a quantidade de nomes.
- As `n` linhas seguintes contêm um nome por linha.
- Cada nome possui apenas letras minúsculas de `a` a `z`.

### Saída

- Uma permutação das 26 letras, representando a nova ordem do alfabeto; ou
- `Impossible`, quando nenhuma ordem consegue deixar os nomes em ordem lexicográfica.

### Restrições

- `1 <= n <= 100`;
- `1 <= tamanho(nome) <= 100`;
- todos os nomes são distintos;
- existem somente 26 letras possíveis;
- a comparação entre dois nomes considera a primeira posição em que eles diferem;
- se um nome for prefixo do outro, o nome menor deve vir primeiro.

## Modelagem em grafos

### Vértices

Cada vértice representa uma letra minúscula do alfabeto. Portanto, o grafo possui 26 vértices: `a`, `b`, ..., `z`, mesmo que algumas letras não apareçam nos nomes.

### Arestas

Os nomes consecutivos devem ser comparados, pois a lista já está na ordem em que precisa permanecer. Para um par de nomes `s` e `t`, encontra-se a primeira posição em que eles são diferentes. Se nessa posição aparecer `x` em `s` e `y` em `t`, cria-se a aresta direcionada `x -> y`, indicando que `x` deve aparecer antes de `y` na nova ordem alfabética.

Se um nome for um prefixo do nome seguinte, nenhuma aresta é criada, pois essa relação já é válida pela regra lexicográfica. Porém, se o nome maior vier antes do seu próprio prefixo, o caso é impossível.

### Classificação do grafo

O grafo é:

- direcionado, porque a restrição `x -> y` tem sentido único;
- simples, pois arestas repetidas entre o mesmo par de letras não acrescentam uma nova restrição;
- pequeno e de ordem fixa, com no máximo 26 vértices;
- inicialmente possivelmente cíclico, mas precisa ser um DAG (grafo direcionado acíclico) para que exista uma resposta.

Uma ordenação topológica do DAG representa uma ordem válida para as letras. Se houver um ciclo, as restrições são contraditórias e a resposta é `Impossible`.

## Resultado de aprendizagem aferido

O resultado de aprendizagem principal é reconhecer que uma condição de ordenação pode ser representada como um grafo de precedência e resolvida por ordenação topológica. O problema também avalia a capacidade de:

- extrair restrições a partir da primeira diferença entre strings;
- modelar essas restrições como arestas direcionadas;
- identificar inconsistências por meio de ciclos;
- lidar corretamente com o caso de prefixo;
- interpretar a ordenação topológica como uma solução do problema original.

## Participação de DFS/BFS na solução

DFS ou BFS pode participar da etapa de ordenação topológica:

- com **DFS**, cada vértice é visitado e colocado em uma pilha após todos os seus sucessores. Uma aresta para um vértice em processamento indica um ciclo;
- com **BFS**, aplica-se o algoritmo de Kahn: colocam-se na fila os vértices com grau de entrada zero, removem-se suas arestas e adicionam-se à fila os novos vértices sem predecessores. Se nem todos os 26 vértices forem processados, existe um ciclo.

Assim, a busca não é usada para comparar todos os caracteres entre si. Ela percorre o grafo de restrições para produzir a ordem das letras ou detectar que essa ordem é impossível. A implementação poderá usar BFS/Kahn por ser uma forma direta de acompanhar os graus de entrada.

## Instância pequena

### Entrada

```text
4
baa
abcd
abca
cab
```

### Restrições obtidas

1. Comparando `baa` e `abcd`, a primeira diferença é `b` contra `a`: `b -> a`.
2. Comparando `abcd` e `abca`, a primeira diferença é `d` contra `a`: `d -> a`.
3. Comparando `abca` e `cab`, a primeira diferença é `a` contra `c`: `a -> c`.

O subgrafo relevante possui as relações `b -> a`, `d -> a` e `a -> c`. Uma ordenação topológica possível começa por `b`, `d`, `a`, `c`; as outras letras podem ser colocadas nas posições restantes, desde que essas três restrições sejam mantidas.

### Uma saída possível

```text
bdacefghijklmnopqrstuvwxyz
```

Nessa saída, `b` vem antes de `a`, `d` vem antes de `a` e `a` vem antes de `c`, portanto os quatro nomes ficam em ordem lexicográfica segundo o alfabeto personalizado.
