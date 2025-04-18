# Importa os algoritmos
from algoritmos.A_estrela import A_estrela
# ADICIONAR IMPORTS DE ALGORITMOS AQUI!

ALGORITMOS = [A_estrela]


import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from time import time

# Importa os dados das cidades
from dados.cidades import distancias_cidades, coordenadas, grafo_distancias

# Funções das classes Hospital e Orgao
from funcoes.Hospital import carregar_hospitais
from funcoes.Orgao import carregar_orgaos

# Desenha o grafo e destaca o caminho
def desenhar_grafo(ax, coords, arestas, caminho=None):
    ax.clear()
    # vértices
    for cidade, (x, y) in coords.items():
        ax.plot(x, y, 'bo')
        ax.text(x+2, y+2, cidade, fontsize=8)
    # arestas
    desenhadas = set()
    for o, d, c in arestas:
        chave = tuple(sorted((o, d)))
        if chave in desenhadas:
            continue
        desenhadas.add(chave)
        x1, y1 = coords[o]; x2, y2 = coords[d]
        ax.plot([x1, x2], [y1, y2], 'k-', lw=1)
    # caminho
    if caminho:
        for i in range(len(caminho)-1):
            p, q = caminho[i], caminho[i+1]
            x1, y1 = coords[p]; x2, y2 = coords[q]
            ax.plot([x1, x2], [y1, y2], 'r-', lw=3)
    ax.set_xlabel("X"); ax.set_ylabel("Y")
    ax.set_title("Rota"); ax.grid(True)

# Função do botão
def realizar_busca():
    nome = entry_nome.get().strip()
    origem = var_cidade.get()
    orgao = var_orgao.get()
    algoritmo_escolhido = var_algoritmo.get()

    if not nome or not origem or not orgao:
        messagebox.showerror("Erro", "Preencha todos os campos.")
        return

    orgao_escolhido = next((o for o in orgaos if o.nome == orgao), None)
    if not orgao_escolhido:
        messagebox.showerror("Erro", "Órgão não cadastrado.")
        return

    cep_org = orgao_escolhido.cep

    # encontra cidade do hospital com mesmo CEP
    hosp = next((h for h in hospitais if h.cep == cep_org), None)
    if not hosp:
        messagebox.showerror("Erro", "Hospital não encontrado para esse órgão.")
        return

    destino = hosp.cidade

    # BUSCA PELO MELHOR CAMINHO COM O ALGORITMO ESCOLHIDO
    funcao_algoritmo = [f_alg for f_alg in ALGORITMOS if f_alg.__name__ == algoritmo_escolhido][0]
    tempo_pre_busca = time()
    caminho, custo = funcao_algoritmo(grafo_distancias, origem, destino)
    tempo_de_busca = time() - tempo_pre_busca

    if not caminho:
        messagebox.showerror("Erro", "Caminho não encontrado.")
        return

    messagebox.showinfo(
        "Resultado",
        f"Caminho: {' -> '.join(caminho)}\nCusto total = {custo:.1f} km\nTempo de Busca = {tempo_de_busca:.2f}s"
    )
    desenhar_grafo(ax, coordenadas, distancias_cidades, caminho)
    canvas.draw()

# Carrega dados
hospitais = carregar_hospitais("dados/hospitais.txt")
orgaos = carregar_orgaos("dados/mock_orgaos.txt")

if not hospitais or not orgaos:
    raise RuntimeError("Falha ao carregar dados.")

# Configura GUI
root = tk.Tk()
root.title("Busca de Rotas por Órgão")

tk.Label(root, text="Nome do Paciente:").pack(padx=5, pady=2)
entry_nome = tk.Entry(root); entry_nome.pack(fill='x', padx=5)

tk.Label(root, text="Cidade de Origem:").pack(padx=5, pady=2)
var_cidade = tk.StringVar(root)
var_cidade.set(hospitais[0].cidade)
opt_cidade = tk.OptionMenu(root, var_cidade, *(h.cidade for h in hospitais))
opt_cidade.pack(fill='x', padx=5)

tk.Label(root, text="Órgão Necessário:").pack(padx=5, pady=2)
var_orgao = tk.StringVar(root)
var_orgao.set(orgaos[0].nome)
opt_orgao = tk.OptionMenu(root, var_orgao, *(o.nome for o in orgaos))
opt_orgao.pack(fill='x', padx=5)

tk.Label(root, text="Algorítmo de Busca:").pack(padx=5, pady=2)
var_algoritmo = tk.StringVar(root)
var_algoritmo.set(ALGORITMOS[0].__name__)
opt_algoritmo = tk.OptionMenu(root, var_algoritmo, *(alg.__name__ for alg in ALGORITMOS))
opt_algoritmo.pack(fill='x', padx=5)

btn = tk.Button(root, text="Realizar Busca", command=realizar_busca)
btn.pack(pady=8)

# Matplotlib no Tk
fig, ax = plt.subplots(figsize=(6, 4))
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(fill='both', expand=True, padx=5, pady=5)

root.mainloop()