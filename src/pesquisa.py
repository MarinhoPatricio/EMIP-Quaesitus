import os
import pandas as pd
from rapidfuzz import process, fuzz
from utils import normalizar


class PesquisaAlunos:

    def __init__(self, arquivo):

        ext = os.path.splitext(arquivo)[1].lower()

        if ext == ".xlsx":
            self.df = pd.read_excel(arquivo)

        elif ext == ".csv":
            try:
                self.df = pd.read_csv(arquivo, encoding="utf-8")
                print(self.df.columns.tolist())
                print(self.df.head())
            except UnicodeDecodeError:
                self.df = pd.read_csv(arquivo, encoding="latin1")

        else:
            raise Exception("Formato de arquivo não suportado.")

        self.df = self.df.loc[:, ~self.df.columns.str.contains("^Unnamed")]
        self.df.columns = self.df.columns.str.strip()

        self.nomes = self.df["Nome"].fillna("").astype(str).tolist()

        print(self.nomes[:10])
        

        coluna_nome = None

        for coluna in self.df.columns:
            if "nome" in coluna.lower():
                coluna_nome = coluna
                break

        if coluna_nome is None:
            raise Exception("Não foi encontrada uma coluna chamada 'Nome'.")

        self.coluna_nome = coluna_nome

        self.nomes = self.df[self.coluna_nome].fillna("").astype(str).tolist()

        self.nomes_normalizados = [
            normalizar(nome)
            for nome in self.nomes
        ]


    def pesquisar(self, texto):

        texto = normalizar(texto)

        resultados = process.extract(
            texto,
            self.nomes_normalizados,
            scorer=fuzz.WRatio,
            limit=20
        )

        lista = []

        for _, score, indice in resultados:

            if score >= 60:
                linha = self.df.iloc[indice]
                lista.append((score, linha))

        return lista