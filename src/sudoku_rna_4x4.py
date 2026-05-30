
"""
# Sudoku 4x4 com RNA Multicamadas

Este arquivo contém uma solução completa para o problema proposto.

A solução usa uma Rede Neural Artificial multicamadas, implementada com
MLPClassifier do scikit-learn, para reconhecer se um tabuleiro completo
de Sudoku 4x4 é válido ou inválido.

A resolução do tabuleiro inicial é feita com backtracking, pois Sudoku
é um problema lógico de satisfação de restrições.
"""

import random
import os
import numpy as np
import matplotlib.pyplot as plt

from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix


# ============================================================
# Classe responsável pelas regras do Sudoku 4x4
# ============================================================

class Sudoku4x4:
    """
    Classe com funções para validar, gerar e resolver Sudokus 4x4.

    A grade usa valores:
    - 0 para célula vazia;
    - 1, 2, 3, 4 para células preenchidas.
    """

    N = 4
    SUB = 2
    VALORES = {1, 2, 3, 4}

    @staticmethod
    def matriz_vazia():
        return [[0 for _ in range(Sudoku4x4.N)] for _ in range(Sudoku4x4.N)]

    @staticmethod
    def imprimir(tabuleiro, titulo="Tabuleiro"):
        print(f"\n{titulo}")
        print("-" * 13)
        for i, linha in enumerate(tabuleiro):
            texto = ""
            for j, valor in enumerate(linha):
                texto += str(valor) if valor != 0 else "."
                texto += " "
                if j == 1:
                    texto += "| "
            print(texto)
            if i == 1:
                print("-" * 13)

    @staticmethod
    def linha_valida(tabuleiro, linha):
        valores = [v for v in tabuleiro[linha] if v != 0]
        return len(valores) == len(set(valores))

    @staticmethod
    def coluna_valida(tabuleiro, coluna):
        valores = [tabuleiro[i][coluna] for i in range(Sudoku4x4.N) if tabuleiro[i][coluna] != 0]
        return len(valores) == len(set(valores))

    @staticmethod
    def subgrupo_valido(tabuleiro, linha, coluna):
        inicio_linha = (linha // Sudoku4x4.SUB) * Sudoku4x4.SUB
        inicio_coluna = (coluna // Sudoku4x4.SUB) * Sudoku4x4.SUB

        valores = []
        for i in range(inicio_linha, inicio_linha + Sudoku4x4.SUB):
            for j in range(inicio_coluna, inicio_coluna + Sudoku4x4.SUB):
                if tabuleiro[i][j] != 0:
                    valores.append(tabuleiro[i][j])

        return len(valores) == len(set(valores))

    @staticmethod
    def pode_colocar(tabuleiro, linha, coluna, numero):
        if numero not in Sudoku4x4.VALORES:
            return False

        # A célula deve estar vazia
        if tabuleiro[linha][coluna] != 0:
            return False

        # Testa temporariamente o número
        tabuleiro[linha][coluna] = numero

        valido = (
            Sudoku4x4.linha_valida(tabuleiro, linha)
            and Sudoku4x4.coluna_valida(tabuleiro, coluna)
            and Sudoku4x4.subgrupo_valido(tabuleiro, linha, coluna)
        )

        # Desfaz o teste
        tabuleiro[linha][coluna] = 0

        return valido

    @staticmethod
    def solucao_completa_valida(tabuleiro):
        """
        Verifica se o tabuleiro completo é uma solução válida.

        Cada linha, coluna e subgrupo precisa conter exatamente {1, 2, 3, 4}.
        """
        esperado = Sudoku4x4.VALORES

        # Verifica linhas
        for linha in tabuleiro:
            if set(linha) != esperado:
                return False

        # Verifica colunas
        for col in range(Sudoku4x4.N):
            coluna = {tabuleiro[lin][col] for lin in range(Sudoku4x4.N)}
            if coluna != esperado:
                return False

        # Verifica subgrupos 2x2
        for lin_ini in range(0, Sudoku4x4.N, Sudoku4x4.SUB):
            for col_ini in range(0, Sudoku4x4.N, Sudoku4x4.SUB):
                valores = set()
                for i in range(lin_ini, lin_ini + Sudoku4x4.SUB):
                    for j in range(col_ini, col_ini + Sudoku4x4.SUB):
                        valores.add(tabuleiro[i][j])
                if valores != esperado:
                    return False

        return True

    @staticmethod
    def encontrar_vazio(tabuleiro):
        for i in range(Sudoku4x4.N):
            for j in range(Sudoku4x4.N):
                if tabuleiro[i][j] == 0:
                    return i, j
        return None

    @staticmethod
    def resolver(tabuleiro):
        """
        Resolve o Sudoku usando backtracking.

        Retorna True quando encontra uma solução.
        """
        posicao = Sudoku4x4.encontrar_vazio(tabuleiro)

        if posicao is None:
            return Sudoku4x4.solucao_completa_valida(tabuleiro)

        linha, coluna = posicao
        numeros = list(Sudoku4x4.VALORES)
        random.shuffle(numeros)

        for numero in numeros:
            if Sudoku4x4.pode_colocar(tabuleiro, linha, coluna, numero):
                tabuleiro[linha][coluna] = numero

                if Sudoku4x4.resolver(tabuleiro):
                    return True

                tabuleiro[linha][coluna] = 0

        return False


# ============================================================
# Funções de geração de soluções válidas e inválidas
# ============================================================

def gerar_todas_solucoes_4x4():
    """
    Gera todas as soluções válidas do Sudoku 4x4 usando backtracking.
    """
    solucoes = []
    tabuleiro = Sudoku4x4.matriz_vazia()

    def backtracking():
        posicao = Sudoku4x4.encontrar_vazio(tabuleiro)

        if posicao is None:
            if Sudoku4x4.solucao_completa_valida(tabuleiro):
                solucoes.append([linha[:] for linha in tabuleiro])
            return

        linha, coluna = posicao

        for numero in range(1, 5):
            if Sudoku4x4.pode_colocar(tabuleiro, linha, coluna, numero):
                tabuleiro[linha][coluna] = numero
                backtracking()
                tabuleiro[linha][coluna] = 0

    backtracking()
    return solucoes


def gerar_exemplo_invalido(solucao):
    """
    Gera um tabuleiro inválido a partir de uma solução válida.

    A estratégia é alterar uma célula para causar repetição em linha,
    coluna ou subgrupo.
    """
    tabuleiro = [linha[:] for linha in solucao]

    linha = random.randint(0, 3)
    coluna = random.randint(0, 3)

    valor_original = tabuleiro[linha][coluna]
    valores_possiveis = [v for v in range(1, 5) if v != valor_original]

    tabuleiro[linha][coluna] = random.choice(valores_possiveis)

    return tabuleiro


def gerar_dataset():
    """
    Gera o conjunto de dados com exemplos válidos e inválidos.
    """
    solucoes_validas = gerar_todas_solucoes_4x4()

    X = []
    y = []

    # Exemplos válidos
    for solucao in solucoes_validas:
        X.append(codificar_one_hot(solucao))
        y.append(1)

    # Exemplos inválidos
    for solucao in solucoes_validas:
        invalido = gerar_exemplo_invalido(solucao)
        X.append(codificar_one_hot(invalido))
        y.append(0)

    return np.array(X), np.array(y), solucoes_validas


# ============================================================
# Codificação do tabuleiro para entrada da RNA
# ============================================================

def codificar_one_hot(tabuleiro):
    """
    Converte o tabuleiro 4x4 em vetor one-hot.

    Cada célula possui 4 posições:
    - número 1 -> [1, 0, 0, 0]
    - número 2 -> [0, 1, 0, 0]
    - número 3 -> [0, 0, 1, 0]
    - número 4 -> [0, 0, 0, 1]

    Como são 16 células e 4 valores possíveis:
    entrada = 16 * 4 = 64 atributos.
    """
    vetor = []

    for linha in tabuleiro:
        for valor in linha:
            one_hot = [0, 0, 0, 0]
            if valor in [1, 2, 3, 4]:
                one_hot[valor - 1] = 1
            vetor.extend(one_hot)

    return vetor


# ============================================================
# Classe da Rede Neural Artificial Multicamadas
# ============================================================

class RNAValidadoraSudoku:
    """
    RNA multicamadas para classificar tabuleiros completos como válidos ou inválidos.
    """

    def __init__(self):
        self.modelo = MLPClassifier(
            hidden_layer_sizes=(64, 32),
            activation="relu",
            solver="adam",
            max_iter=2000,
            random_state=42
        )

    def treinar(self, X_train, y_train):
        self.modelo.fit(X_train, y_train)

    def prever(self, tabuleiro):
        entrada = np.array([codificar_one_hot(tabuleiro)])
        predicao = self.modelo.predict(entrada)[0]
        probabilidade = self.modelo.predict_proba(entrada)[0]

        return predicao, probabilidade

    def avaliar(self, X_test, y_test):
        y_pred = self.modelo.predict(X_test)

        print("\nAcurácia no teste:", accuracy_score(y_test, y_pred))
        print("\nRelatório de classificação:")
        print(classification_report(y_test, y_pred))

        print("\nMatriz de confusão:")
        print(confusion_matrix(y_test, y_pred))

        return y_pred


# ============================================================
# Geração de tabuleiro inicial aleatório
# ============================================================

def gerar_tabuleiro_inicial(solucao, quantidade_removida=8):
    """
    Recebe uma solução válida e remove algumas células para formar
    um tabuleiro inicial de Sudoku.
    """
    tabuleiro = [linha[:] for linha in solucao]

    posicoes = [(i, j) for i in range(4) for j in range(4)]
    random.shuffle(posicoes)

    for i in range(quantidade_removida):
        linha, coluna = posicoes[i]
        tabuleiro[linha][coluna] = 0

    return tabuleiro


# ============================================================
# Função para salvar imagem do tabuleiro
# ============================================================

def salvar_imagem_tabuleiro(tabuleiro, nome_arquivo, titulo):
    """
    Salva uma imagem simples do tabuleiro em formato PNG.
    """
    os.makedirs(os.path.dirname(nome_arquivo), exist_ok=True)
    fig, ax = plt.subplots(figsize=(4, 4))
    ax.set_xlim(0, 4)
    ax.set_ylim(0, 4)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title(titulo)

    for i in range(5):
        largura = 2 if i % 2 == 0 else 1
        ax.plot([i, i], [0, 4], linewidth=largura)
        ax.plot([0, 4], [i, i], linewidth=largura)

    for i in range(4):
        for j in range(4):
            valor = tabuleiro[i][j]
            if valor != 0:
                ax.text(
                    j + 0.5,
                    3.5 - i,
                    str(valor),
                    ha="center",
                    va="center",
                    fontsize=18
                )

    plt.savefig(nome_arquivo, bbox_inches="tight")
    plt.close()


# ============================================================
# Código principal
# ============================================================

def main():
#random.seed(42)
#np.random.seed(42)

    print("# Gerando dataset")
    X, y, solucoes_validas = gerar_dataset()

    print("Total de exemplos:", len(X))
    print("Exemplos válidos:", sum(y == 1))
    print("Exemplos inválidos:", sum(y == 0))
    print("Tamanho da entrada da RNA:", X.shape[1])

    print("\n# Separando treino e teste")
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.25,
        random_state=42,
        stratify=y
    )

    print("Treino:", len(X_train))
    print("Teste:", len(X_test))

    print("\n# Treinando RNA")
    rna = RNAValidadoraSudoku()
    rna.treinar(X_train, y_train)

    print("\n# Avaliando RNA")
    rna.avaliar(X_test, y_test)

    print("\n# Gerando tabuleiro inicial aleatório")
    solucao_base = random.choice(solucoes_validas)
    tabuleiro_inicial = gerar_tabuleiro_inicial(solucao_base, quantidade_removida=8)

    Sudoku4x4.imprimir(tabuleiro_inicial, "Tabuleiro inicial")

    print("\n# Resolvendo tabuleiro")
    tabuleiro_resolvido = [linha[:] for linha in tabuleiro_inicial]
    encontrou = Sudoku4x4.resolver(tabuleiro_resolvido)

    if encontrou:
        Sudoku4x4.imprimir(tabuleiro_resolvido, "Solução gerada")

        predicao, probabilidade = rna.prever(tabuleiro_resolvido)

        print("\n# Reconhecimento pela RNA")
        print("Classe prevista:", predicao)
        print("Probabilidades [inválido, válido]:", probabilidade)

        if predicao == 1:
            print("A RNA reconheceu o tabuleiro final como VÁLIDO.")
        else:
            print("A RNA reconheceu o tabuleiro final como INVÁLIDO.")
    else:
        print("Não foi possível resolver o tabuleiro inicial.")

    salvar_imagem_tabuleiro(tabuleiro_inicial, "imagens/tabuleiro_inicial.png", "Tabuleiro Inicial")
    salvar_imagem_tabuleiro(tabuleiro_resolvido, "imagens/tabuleiro_resolvido.png", "Tabuleiro Resolvido")

    print("\nImagens salvas na pasta imagens/.")


if __name__ == "__main__":
    main()

