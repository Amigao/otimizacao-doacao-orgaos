# Importa os algoritmos
from algoritmos.A_estrela import A_estrela
from algoritmos.largura import busca_em_largura
# ADICIONAR IMPORTS DE ALGORITMOS AQUI!

ALGORITMOS = [A_estrela, busca_em_largura]


import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from time import time

# Importa os dados das cidades
from dados.cidades import distancias_cidades, coordenadas, grafo_distancias

# Funções das classes Hospital e Orgao
from funcoes.Hospital import carregar_hospitais, cidade_via_cep
from funcoes.Orgao import carregar_orgaos, calcular_tempo_compatibilidade
from funcoes.Paciente import carregar_pacientes

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
def realizar_busca_interface():
    nome = entry_nome.get().strip()
    origem = var_cidade.get()
    orgao = var_orgao.get()
    orgao = [o for o in orgaos if o.nome == orgao]

    if not nome or not origem or not orgao:
        messagebox.showerror("Erro", "Preencha todos os campos.")
        return

    # Pega o nome do órgão escolhido no menu (ex: "Coração")
    nome_orgao = var_orgao.get()

    realizar_busca(nome, origem, nome_orgao)
    
def realizar_busca(nome_paciente, cidade_origem, nome_orgao):
    # Filtra todos os órgãos disponíveis desse tipo
    orgaos_disponiveis = [o for o in orgaos if o.nome == nome_orgao]

    if not orgaos_disponiveis:
        messagebox.showerror("Erro", f"Não há órgãos cadastrados do tipo {nome_orgao}.")
        return

    # Associa cada órgão a seu hospital, via CEP
    orgaos_com_hospital = []
    for orgao in orgaos_disponiveis:
        hosp = next((h for h in hospitais if h.cep == orgao.cep), None)
        if hosp:
            orgaos_com_hospital.append((orgao, hosp))

    if not orgaos_com_hospital:
        messagebox.showerror("Erro", "Nenhum hospital encontrado para os órgãos disponíveis.")
        return

    melhor_hospital = None
    melhor_algoritmo = None
    melhor_caminho = None
    menor_custo = float("inf")
    menor_tempo = float("inf")
    transporte_especial = False
    tempos_de_execucao = {}
    custos_dos_caminhos = {}
    orgao_final = None
    for orgao, hosp in orgaos_com_hospital:
        destino = hosp.cidade
        print(f"\n  -> Buscando rotas até hospital: {hosp.nome} ({destino})")
        
        encontrou_caminho_viavel = False  # flag local

        for funcao_algoritmo in ALGORITMOS:
            nome_algoritmo = funcao_algoritmo.__name__
            tempo_pre_busca = time()

            caminho, custo = funcao_algoritmo(grafo_distancias, cidade_origem, destino)
            tempo_de_busca = time() - tempo_pre_busca

            if not caminho:
                print(f"    [X] {nome_algoritmo}: Caminho não encontrado.")
                continue

            if calcular_tempo_compatibilidade(orgao, custo):
                encontrou_caminho_viavel = True

                print(f"    [✓] {nome_algoritmo}:")
                print(f"        Caminho: {' -> '.join(caminho)}")
                print(f"        Custo: {custo:.1f} km | Tempo de busca: {tempo_de_busca:.6f} s")

                if custo < menor_custo:
                    melhor_hospital = hosp
                    melhor_algoritmo = nome_algoritmo
                    melhor_caminho = caminho
                    menor_custo = custo
                    menor_tempo = tempo_de_busca
                    orgao_final = orgao

                tempos_de_execucao[nome_algoritmo] = min(
                    tempos_de_execucao.get(nome_algoritmo, float('inf')),
                    tempo_de_busca
                )
                custos_dos_caminhos[nome_algoritmo] = min(
                    custos_dos_caminhos.get(nome_algoritmo, float('inf')),
                    custo
                )
            else:
                melhor_hospital = hosp
                print(f"    [X] {nome_algoritmo}: Órgão encontrado mas incompatível -> Tempo de viagem maior que tempo de isquemia.")

        if not encontrou_caminho_viavel:
            transporte_especial = True

    if transporte_especial:
        print(f"\n[!] Transporte especial necessário para o órgão {orgao.nome}.")
        messagebox.showwarning(
            "Atenção",
            f"Transporte especial necessário para o paciente {paciente.nome}.\n\n"
            f"Existe um {orgao.nome} disponível em {melhor_hospital}.\n"
            f"Entretanto, será preciso utilizar transporte especial para chegar em no máximo {orgao.tempo_isquemia} horas."
        )
        return False
        # TODO: pegar input da interface questionando se o transporte especial será utilizado ou o paciente permanecerá na fila de espera
    elif not melhor_caminho:
        print(f"[!] Nenhum caminho encontrado para o órgão {orgao.nome}.")
        messagebox.showerror("Erro", f"Nenhum caminho encontrado para o órgão {orgao.nome}.")
        return False
    else:
        print(f"\n>>> Melhor resultado para {orgao.nome}:")
        print(f"    Paciente: {paciente.nome}")
        print(f"    Hospital escolhido: {melhor_hospital.nome} ({melhor_hospital.cidade})")
        print(f"    Algoritmo escolhido: {melhor_algoritmo}")
        print(f"    Custo total: {menor_custo:.1f} km")
        print(f"    Tempo de busca: {menor_tempo:.6f} s")

        messagebox.showinfo(
            f"Melhor Resultado - {melhor_algoritmo}",
            f"Nome do paciente: {paciente.nome}\n"
            f"Órgão: {orgao.nome}\n"
            f"Hospital: {melhor_hospital.nome} ({melhor_hospital.cidade})\n"
            f"Algoritmo: {melhor_algoritmo}\n"
            f"Caminho: {' -> '.join(melhor_caminho)}\n"
            f"Custo total = {menor_custo:.1f} km\n"
            f"Tempo de Busca = {menor_tempo:.6f} s"
        )

        desenhar_grafo(ax, coordenadas, distancias_cidades, caminho=melhor_caminho)
        canvas.draw()
        if(orgao_final != None):
            orgaos.remove(orgao_final)
        return True

# Carrega dados
hospitais = carregar_hospitais("dados/hospitais.txt")
orgaos = carregar_orgaos("dados/mock_orgaos.txt")
pacientes = carregar_pacientes("dados/mock_pacientes.txt")

if not hospitais or not orgaos or not pacientes:
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
nomes_unicos = list({o.nome for o in orgaos})
var_orgao = tk.StringVar(root)
var_orgao.set(nomes_unicos[0])
tk.OptionMenu(root, var_orgao, *nomes_unicos).pack(fill='x', padx=5)

# tk.Label(root, text="Algorítmo de Busca:").pack(padx=5, pady=2)
# var_algoritmo = tk.StringVar(root)
# var_algoritmo.set(ALGORITMOS[0].__name__)
# opt_algoritmo = tk.OptionMenu(root, var_algoritmo, *(alg.__name__ for alg in ALGORITMOS))
# opt_algoritmo.pack(fill='x', padx=5)

btn = tk.Button(root, text="Realizar Busca", command=realizar_busca_interface)
btn.pack(pady=8)

# Matplotlib no Tk
fig, ax = plt.subplots(figsize=(6, 4))
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(fill='both', expand=True, padx=5, pady=5)

for paciente in pacientes:
    if (realizar_busca(paciente.nome, cidade_via_cep(hospitais, paciente.cep), paciente.orgao_solicitado)):
        pacientes.remove(paciente)
        print(f"Paciente {paciente.nome} removido da lista de espera.")
        print(f"Órgão {paciente.orgao_solicitado} encontrado para o paciente {paciente.nome}.\n")

root.mainloop()