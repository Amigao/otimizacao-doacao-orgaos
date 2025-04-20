# Importa os algoritmos
from algoritmos.A_estrela import A_estrela
from algoritmos.largura import busca_em_largura
# ADICIONAR IMPORTS DE ALGORITMOS AQUI!

ALGORITMOS = [A_estrela, busca_em_largura]


import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from time import time
from datetime import datetime, date

# Importa os dados das cidades
from dados.cidades import distancias_cidades, coordenadas, grafo_distancias

# Funções das classes Hospital e Orgao
from funcoes.Hospital import carregar_hospitais, cidade_via_cep, cep_via_cidade
from funcoes.Orgao import carregar_orgaos, calcular_tempo_compatibilidade, Orgao
from funcoes.Paciente import carregar_pacientes, Paciente

def somente_inteiros_positivos(valor):
    return valor.isdigit() and int(valor) > 0 if valor else True  # permite vazio temporariamente

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

def atualizar_banco_de_dados(pacientes, hospitais):
    for paciente in pacientes:
        if (realizar_busca(paciente, cidade_via_cep(hospitais, paciente.cep), paciente.orgao_solicitado)):
            pacientes.remove(paciente)
            print(f"Paciente {paciente.nome} removido da lista de espera.")
            print(f"Órgão {paciente.orgao_solicitado} encontrado para o paciente {paciente.nome}.\n")
    
    print("Banco de dados atualizado!")
    atualizar_treeviews()

def atualizar_treeviews():
    # Limpa as treeviews
    tree_pacientes.delete(*tree_pacientes.get_children())
    tree_orgaos.delete(*tree_orgaos.get_children())

    # Adiciona pacientes
    for p in pacientes:
        tree_pacientes.insert("", "end", values=(p.nome, p.idade, p.orgao_solicitado, p.cep, p.data_entrada.strftime("%d/%m/%Y")))

    # Adiciona órgãos
    for o in orgaos:
        tree_orgaos.insert("", "end", values=(o.nome, o.tempo_isquemia, cidade_via_cep(hospitais, o.cep)))

# Função do botão
def realizar_busca_interface():
    nome = entry_nome.get().strip()
    origem = var_cidade.get()
    idade = var_idade.get()
    orgao = var_orgao.get()
    orgao = [o for o in orgaos_possiveis if o.nome == orgao]
    nome_orgao = var_orgao.get()
    
    if not nome or not origem or not nome_orgao:
        messagebox.showerror("Erro", "Preencha todos os campos.")
        return

    novo_paciente = Paciente(nome, date.today(), idade, cep_via_cidade(hospitais, origem), nome_orgao)
    pacientes.append(novo_paciente)
    atualizar_treeviews()

    realizar_busca(novo_paciente, origem, nome_orgao)
    
def realizar_busca(paciente, cidade_origem, nome_orgao):
    orgaos_disponiveis = [o for o in orgaos if o.nome == nome_orgao]

    if not orgaos_disponiveis:
        messagebox.showerror("Erro", f"Não há órgãos cadastrados do tipo {nome_orgao}.")
        return

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
            pacientes.remove(paciente)
        atualizar_treeviews()
        return True

# Carrega dados
hospitais = carregar_hospitais("dados/hospitais.txt")
orgaos_possiveis = carregar_orgaos("dados/orgaos.txt")

orgaos = carregar_orgaos("dados/mock_orgaos.txt")
pacientes = carregar_pacientes("dados/mock_pacientes.txt")

if not hospitais or not orgaos or not pacientes:
    raise RuntimeError("Falha ao carregar dados.")

# Suponha que hospitais e orgaos já existam
root = tk.Tk()
root.title("Busca de Rotas por Órgão")

# --- Layout base com frames ---
main_frame = tk.Frame(root)
main_frame.pack(padx=10, pady=10, fill='both', expand=True)

left_frame = tk.Frame(main_frame)
left_frame.grid(row=0, column=0, sticky='n')

right_frame = tk.Frame(main_frame)
right_frame.grid(row=0, column=1, sticky='n')

# 1. Frame lateral esquerdo como "box" de busca
frame_busca = tk.LabelFrame(left_frame, text="Buscar por Órgão", padx=10, pady=10)
frame_busca.pack(fill="x", padx=10, pady=10)

tk.Label(frame_busca, text="Nome do Paciente:").pack(anchor='w')
entry_nome = tk.Entry(frame_busca)
entry_nome.pack(fill='x')

tk.Label(frame_busca, text="Idade do paciente:").pack(anchor='w')
vcmd = (frame_busca.register(somente_inteiros_positivos), "%P")
var_idade = tk.Entry(frame_busca, validate="key", validatecommand=vcmd)
var_idade.pack(fill='x')

tk.Label(frame_busca, text="Cidade de Origem:").pack(anchor='w', pady=(5,0))
var_cidade = tk.StringVar(root)
var_cidade.set(hospitais[0].cidade)
combo_cidade = ttk.Combobox(frame_busca, textvariable=var_cidade, values=[h.cidade for h in hospitais], state="readonly")
combo_cidade.pack(fill='x')

tk.Label(frame_busca, text="Órgão Necessário:").pack(anchor='w', pady=(5,0))
nomes_unicos = list({o.nome for o in orgaos_possiveis})
var_orgao = tk.StringVar(root)
var_orgao.set(nomes_unicos[0])
combo_orgao = ttk.Combobox(frame_busca, textvariable=var_orgao, values=nomes_unicos, state="readonly")
combo_orgao.pack(fill='x')

btn_busca = tk.Button(frame_busca, text="Realizar Busca", command=realizar_busca_interface)
btn_busca.pack(pady=(10, 0))

btn_atualizar = tk.Button(text="Atualizar fila de espera", command=lambda: atualizar_banco_de_dados(pacientes, hospitais))
btn_atualizar.pack(pady=5)

# 2. Outro box pra adicionar órgão
frame_add_orgao = tk.LabelFrame(left_frame, text="Doação de Órgao", padx=10, pady=10)
frame_add_orgao.pack(fill="x", padx=10, pady=10)

btn_nova_janela = tk.Button(frame_add_orgao, text="Adicionar Órgão", command=lambda: abrir_janela_adicionar_orgao())
btn_nova_janela.pack()

# Função que abre nova janela
def abrir_janela_adicionar_orgao():
    nova_janela = tk.Toplevel()
    nova_janela.title("Adicionar Órgão")

    tk.Label(nova_janela, text="Órgão:").pack(pady=5)
    nomes_unicos = list({o.nome for o in orgaos_possiveis})
    var_orgao = tk.StringVar(nova_janela)
    var_orgao.set(nomes_unicos[0])
    entry_orgao = ttk.Combobox(nova_janela, textvariable=var_orgao, values=nomes_unicos, state="readonly")
    entry_orgao.pack()

    tk.Label(nova_janela, text="CEP de Origem:").pack(pady=5)
    var_cep = tk.StringVar(nova_janela)
    var_cep.set(hospitais[0].cep)
    entry_cep = ttk.Combobox(
        nova_janela, 
        textvariable=var_cep, 
        values=[f"{h.cidade} - {h.cep}" for h in hospitais], 
        state="readonly"
    )
    entry_cep.pack()

    btn_salvar = tk.Button(
        nova_janela, 
        text="Salvar", 
        command=lambda: (
            salvar_orgao(entry_orgao.get(), var_cep.get().split(" - ")[0]), 
            nova_janela.destroy()
        )
    )
    btn_salvar.pack(pady=10)

def salvar_orgao(nome, cep):
    # aqui você salva no seu sistema!
    for o in orgaos_possiveis: 
        if (nome == o.nome): 
            tempo = o.tempo_isquemia
    novo_orgao = Orgao(nome, tempo, cep)
    orgaos.append(novo_orgao)
    print(f"Órgão adicionado: {nome}, {tempo} hr, CEP {cep}")
    atualizar_treeviews()


# # --- Entrada de dados (centralizados) ---
# tk.Label(left_frame, text="Nome do Paciente:").pack(padx=5, pady=2)
# entry_nome = tk.Entry(left_frame, justify="center")
# entry_nome.pack(fill='x', padx=5)

# tk.Label(left_frame, text="Cidade de Origem:").pack(padx=5, pady=2)
# var_cidade = tk.StringVar(root)
# var_cidade.set(hospitais[0].cidade)
# opt_cidade = tk.OptionMenu(left_frame, var_cidade, *(h.cidade for h in hospitais))
# opt_cidade.pack(fill='x', padx=5)

# tk.Label(left_frame, text="Órgão Necessário:").pack(padx=5, pady=2)
# nomes_unicos = list({o.nome for o in orgaos})
# var_orgao = tk.StringVar(root)
# var_orgao.set(nomes_unicos[0])
# tk.OptionMenu(left_frame, var_orgao, *nomes_unicos).pack(fill='x', padx=5)

# # --- Botões ---
# tk.Button(left_frame, text="Realizar Busca", command=realizar_busca_interface).pack(pady=(10, 5))
# tk.Button(left_frame, text="Atualizar fila de espera", command=lambda: atualizar_banco_de_dados(pacientes, hospitais)).pack(pady=(0, 10))
# --- Treeview de Pacientes ---
tk.Label(right_frame, text="Fila de Espera:").pack(anchor="w", padx=5, pady=(10, 0))

tree_pacientes = ttk.Treeview(
    right_frame, columns=("nome", "idade", "orgao", "cep", "data"), show="headings", height=8
)
tree_pacientes.heading("nome", text="Nome", anchor='center')
tree_pacientes.heading("idade", text="Idade", anchor='center')
tree_pacientes.heading("orgao", text="Órgão Solicitado", anchor='center')
tree_pacientes.heading("cep", text="CEP", anchor='center')
tree_pacientes.heading("data", text="Data Entrada", anchor='center')

tree_pacientes.column("nome", anchor='center')
tree_pacientes.column("idade", anchor='center')
tree_pacientes.column("orgao", anchor='center')
tree_pacientes.column("cep", anchor='center')
tree_pacientes.column("data", anchor='center')

tree_pacientes.pack(fill='x', padx=5, pady=5)

# --- Treeview de Órgãos disponíveis ---
tk.Label(right_frame, text="Órgãos Disponíveis:").pack(anchor="w", padx=5, pady=(10, 0))

tree_orgaos = ttk.Treeview(
    right_frame, columns=("nome", "tempo", "cidade"), show="headings", height=5
)
tree_orgaos.heading("nome", text="Nome", anchor='center')
tree_orgaos.heading("tempo", text="Tempo Isquemia (hrs)", anchor='center')
tree_orgaos.heading("cidade", text="Cidade", anchor='center')

tree_orgaos.column("nome", anchor='center')
tree_orgaos.column("tempo", anchor='center')
tree_orgaos.column("cidade", anchor='center')

tree_orgaos.pack(fill='x', padx=5, pady=5)


# --- Gráfico do Matplotlib (oculto inicialmente) ---
fig, ax = plt.subplots(figsize=(6, 4))
canvas = FigureCanvasTkAgg(fig, master=root)
# Só será exibido quando a busca for realizada com sucesso

# --- Inicializa os dados nas tabelas ---
atualizar_treeviews()

root.mainloop()
