
# Sudoku 4x4 com Rede Neural Artificial Multicamadas

Este projeto propõe uma solução em Python usando uma Rede Neural Artificial multicamadas para reconhecer soluções válidas de Sudoku 4x4, com números do conjunto:

\[
S = \{1, 2, 3, 4\}
\]

A grade é composta por 4 linhas, 4 colunas e subgrupos 2x2.

## Objetivo

A RNA é treinada para classificar tabuleiros completos como:

- `1`: Sudoku válido;
- `0`: Sudoku inválido.

Depois disso, o sistema gera um tabuleiro inicial aleatório, remove alguns números e usa um solucionador com restrições de Sudoku para testar possibilidades. Ao final, a RNA treinada é usada para reconhecer se a solução encontrada é válida.

## Regras consideradas

1. Cada célula deve conter apenas um número de `S = {1, 2, 3, 4}`.
2. Não pode haver repetição em linhas, colunas ou subgrupos 2x2.
3. Cada linha e cada coluna da grade 4x4 devem conter exatamente uma vez cada número de `S`.
4. O sistema gera dados de treinamento e teste.
5. O sistema gera tabuleiros iniciais aleatórios e apresenta a solução final reconhecida pela RNA.

## Estrutura do projeto

```text
sudoku_rna_4x4/
│
├── README.md
├── requirements.txt
├── src/
│   └── sudoku_rna_4x4.py
│
└── notebooks/
    └── sudoku_rna_4x4.ipynb
```

## Como executar

Instale as dependências:

```bash
pip install -r requirements.txt
```

Execute o programa principal:

```bash
python src/sudoku_rna_4x4.py
```

## Ideia da solução

O problema do Sudoku é um problema de raciocínio lógico e satisfação de restrições. Uma RNA multicamadas, sozinha, não garante raciocínio lógico completo, porque ela aprende padrões estatísticos a partir de exemplos.

Por isso, este projeto usa uma abordagem híbrida:

1. Gera todas as soluções válidas do Sudoku 4x4.
2. Gera exemplos inválidos por embaralhamento e alteração de soluções.
3. Treina uma MLP para reconhecer tabuleiros válidos e inválidos.
4. Gera um tabuleiro inicial aleatório com algumas células vazias.
5. Usa backtracking para construir uma solução candidata.
6. Usa a RNA treinada para validar/reconhecer a solução final.

## Por que não basta gerar amostras e testá-las?

Porque o Sudoku não é apenas um problema de classificação. Ele exige raciocínio sobre restrições:

- cada número só pode aparecer uma vez por linha;
- cada número só pode aparecer uma vez por coluna;
- cada número só pode aparecer uma vez por subgrupo;
- cada escolha afeta as próximas escolhas.

Gerar amostras aleatórias e testá-las pode funcionar em um Sudoku 4x4, pois o espaço de busca é pequeno. Porém, ao generalizar para Sudoku NxN, o número de combinações cresce muito rapidamente. Assim, a força bruta se torna inviável.

Para uma grade 4x4, existem 16 células e 4 possibilidades por célula:

\[
4^{16} = 4.294.967.296
\]

Mesmo no caso 4x4, testar todas as combinações já é grande. Para grades maiores, como 9x9, isso explode para:

\[
9^{81}
\]

Por isso, tratar o Sudoku apenas como geração e teste ignora a natureza lógica do problema.

## Dificuldade de generalizar de 4x4 para NxN

A solução 4x4 usa subgrupos 2x2. Para um Sudoku NxN genérico, é necessário que:

\[
N = k^2
\]

Assim, os subgrupos terão tamanho:

\[
k \times k
\]

Exemplos:

- 4x4: subgrupos 2x2;
- 9x9: subgrupos 3x3;
- 16x16: subgrupos 4x4.

Ao aumentar N, surgem dificuldades:

1. O número de células aumenta de \(N^2\).
2. O número de valores possíveis aumenta para \(N\).
3. A entrada da rede cresce muito, pois a codificação one-hot passa a ter \(N^3\) posições.
4. O número de combinações possíveis cresce exponencialmente.
5. A RNA pode reconhecer padrões, mas não garante solução lógica correta para casos muito diferentes dos exemplos de treino.

Portanto, para NxN, uma solução mais robusta deveria combinar:

- RNA;
- regras lógicas;
- backtracking;
- programação por restrições;
- ou algoritmos de busca com heurísticas.

## Equipe

- Integrante 1:
- Integrante 2:
- Integrante 3:
- Integrante 4:
