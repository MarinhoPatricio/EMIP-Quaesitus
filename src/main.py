import tkinter as tk
from tkinter import ttk
import pandas as pd

from pesquisa import PesquisaAlunos

pesquisa = PesquisaAlunos("alunos.csv")


janela = tk.Tk()
janela.title("Busca de Ex-Alunos")
janela.geometry("900x600")
janela.iconbitmap("icon.ico")



titulo = ttk.Label(
    janela,
    text="Pesquisar aluno",
    font=("Segoe UI",16)
)
titulo.pack(pady=10)


entrada = ttk.Entry(
    janela,
    font=("Segoe UI",14)
)

entrada.pack(fill="x",padx=20)


lista = tk.Listbox(
    janela,
    font=("Segoe UI",12),
    height=20
)

lista.pack(
    fill="both",
    expand=True,
    padx=20,
    pady=20
)


status = ttk.Label(janela)
status.pack()


resultados_atuais=[]


def pesquisar(event=None):

    global resultados_atuais

    lista.delete(0,tk.END)

    texto = entrada.get()

    if len(texto)==0:
        return

    resultados = pesquisa.pesquisar(texto)

    resultados_atuais=resultados

    for score,linha in resultados:

        lista.insert(
            tk.END,
            f"{score:.0f}%   {linha.iloc[0]}"
        )

    status.config(
        text=f"{len(resultados)} resultado(s)"
    )


entrada.bind("<KeyRelease>",pesquisar)


def abrir(event):

    if not lista.curselection():
        return

    indice = lista.curselection()[0]

    score,linha = resultados_atuais[indice]

    janela2=tk.Toplevel()

    janela2.title(linha.iloc[0])

    janela2.geometry("600x450")

    texto=tk.Text(
        janela2,
        font=("Segoe UI",11)
    )

    texto.pack(fill="both",expand=True)

    for coluna,valor in zip(linha.index,linha):

        if pd.isna(valor):
            valor = "Nenhuma"
        texto.insert(
            tk.END,
            f"{coluna}: {valor}\n\n"
        )    

    texto.config(state="disabled")


lista.bind("<Double-Button-1>",abrir)

janela.mainloop()