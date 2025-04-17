import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Importa o A* e os dados do grafo
from busca_Astar import astar, distancias_cidades, coordenadas, grafo

# Carrega hospitais (estado, cidade, nome, cep)
def carregar_hospitais(arquivo):
    hospitais = []
    try:
        with open(arquivo, 'r') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                partes = [p.strip() for p in line.split(',')]
                if len(partes) < 3:
                    continue
                estado = partes[0]
                cidade = partes[1]
                cep    = partes[-1]
                nome   = ", ".join(partes[2:-1])
                hospitais.append((estado, cidade, nome, cep))
    except Exception as e:
        print("Erro ao carregar hospitais:", e)
    return hospitais

# Carrega órgãos (orgão, data, cep)
def carregar_orgaos(arquivo):
    orgaos = []
    try:
        with open(arquivo, 'r') as f:
            for line in f:
                partes = [p.strip() for p in line.split(',')]
                if len(partes) < 3:
                    continue
                orgao   = partes[0]
                data    = partes[1]
                cep_org = partes[2]
                orgaos.append((orgao, data, cep_org))
    except Exception as e:
        print("Erro ao carregar órgãos:", e)
    return orgaos

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
    ax.set_title("Rotas A*"); ax.grid(True)

# Função do botão
def realizar_busca():
    nome   = entry_nome.get().strip()
    origem = var_cidade.get()
    orgao  = var_orgao.get()
    if not nome or not origem or not orgao:
        messagebox.showerror("Erro", "Preencha todos os campos.")
        return

    info = next((o for o in orgaos if o[0] == orgao), None)
    if not info:
        messagebox.showerror("Erro", "Órgão não cadastrado.")
        return

    cep_org = info[2]
    # encontra cidade do hospital com mesmo CEP
    hosp = next((h for h in hospitais if h[3] == cep_org), None)
    if not hosp:
        messagebox.showerror("Erro", "Hospital não encontrado para esse órgão.")
        return

    destino = hosp[1]
    caminho, custo = astar(grafo, origem, destino, coordenadas)
    if not caminho:
        messagebox.showerror("Erro", "Caminho não encontrado.")
        return

    messagebox.showinfo(
        "Resultado",
        f"Caminho: {' -> '.join(caminho)}\nCusto total = {custo:.1f} km"
    )
    desenhar_grafo(ax, coordenadas, distancias_cidades, caminho)
    canvas.draw()

# Carrega dados
hospitais = carregar_hospitais("hospitais.txt")
orgaos    = carregar_orgaos("mock_orgaos.txt")
if not hospitais or not orgaos:
    raise RuntimeError("Falha ao carregar dados.")

# Configura GUI
root = tk.Tk()
root.title("Busca de Rotas por Órgão")

tk.Label(root, text="Nome do Paciente:").pack(padx=5, pady=2)
entry_nome = tk.Entry(root); entry_nome.pack(fill='x', padx=5)

tk.Label(root, text="Cidade de Origem:").pack(padx=5, pady=2)
var_cidade = tk.StringVar(root)
var_cidade.set(hospitais[0][1])
opt_cidade = tk.OptionMenu(root, var_cidade, *(h[1] for h in hospitais))
opt_cidade.pack(fill='x', padx=5)

tk.Label(root, text="Órgão Necessário:").pack(padx=5, pady=2)
var_orgao = tk.StringVar(root)
var_orgao.set(orgaos[0][0])
opt_orgao = tk.OptionMenu(root, var_orgao, *(o[0] for o in orgaos))
opt_orgao.pack(fill='x', padx=5)

btn = tk.Button(root, text="Realizar Busca", command=realizar_busca)
btn.pack(pady=8)

# Matplotlib no Tk
fig, ax = plt.subplots(figsize=(6, 4))
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(fill='both', expand=True, padx=5, pady=5)

root.mainloop()