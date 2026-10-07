"""
Executa src/main.py em cada caso de dados/casos-de-teste.txt e verifica a saída.

Execução (a partir da pasta T2):  python3 dados/testar.py

- esperado "Impossible": a saída deve ser exatamente Impossible;
- esperado "valido": a saída deve ser uma permutação das 26 letras e os nomes
  devem ficar em ordem lexicográfica segundo essa permutação.
"""

import os
import subprocess
import sys

PASTA = os.path.dirname(os.path.abspath(__file__))
MAIN = os.path.join(PASTA, '..', 'src', 'main.py')
CASOS = os.path.join(PASTA, 'casos-de-teste.txt')


def ler_casos():
    linhas = [l.rstrip('\n') for l in open(CASOS, encoding='utf-8')
              if not l.startswith('#')]
    casos, atual = [], []
    for linha in linhas + ['']:
        if linha.strip():
            atual.append(linha.strip())
        elif atual:
            descricao = atual[0].split(':', 1)[1].strip()
            esperado = atual[1].split(':', 1)[1].strip()
            entrada = '\n'.join(atual[2:]) + '\n'
            casos.append((descricao, esperado, entrada))
            atual = []
    return casos


def ordenados(nomes, alfabeto):
    posicao = {c: i for i, c in enumerate(alfabeto)}
    chaves = [[posicao[c] for c in nome] for nome in nomes]
    return all(a <= b for a, b in zip(chaves, chaves[1:]))


def verificar(esperado, entrada, saida):
    if esperado == 'Impossible':
        return saida == 'Impossible'
    if sorted(saida) != [chr(ord('a') + i) for i in range(26)]:
        return False
    nomes = entrada.split()[1:]
    return ordenados(nomes, saida)


def main():
    falhas = 0
    casos = ler_casos()
    for descricao, esperado, entrada in casos:
        saida = subprocess.run([sys.executable, MAIN], input=entrada,
                               capture_output=True, text=True).stdout.strip()
        ok = verificar(esperado, entrada, saida)
        falhas += not ok
        print('%s  %s\n      saída: %s' % ('OK   ' if ok else 'FALHA', descricao, saida))
    print('\n%d de %d casos corretos' % (len(casos) - falhas, len(casos)))
    sys.exit(1 if falhas else 0)


if __name__ == '__main__':
    main()
