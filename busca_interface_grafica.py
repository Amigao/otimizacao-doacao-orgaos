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
from funcoes.Paciente import carregar_pacientes, ordenar_pacientes, Paciente

largura, altura = 500, 280

def sangue_compativel(paciente_tipo, orgao_tipo):
    """
    Verifica se o tipo sanguíneo do órgão (doador) é compatível com o do paciente (receptor).
    
    Parâmetros:
    paciente_tipo (str): Tipo sanguíneo do paciente (receptor).
    orgao_tipo (str): Tipo sanguíneo do doador (órgão).

    Retorna:
    bool: True se compatível, False caso contrário.
    """
    compatibilidade = {
        'A': ['A', 'O'],
        'B': ['B', 'O'],
        'AB': ['A', 'B', 'AB', 'O'],  # Receptor universal
        'O': ['O']  # Pode receber apenas de O
    }

    return orgao_tipo in compatibilidade.get(paciente_tipo, [])


def somente_inteiros_positivos(valor):
    return valor.isdigit() and int(valor) > 0 if valor else True  # permite vazio temporariamente

def mostrar_aviso(paciente, orgao, melhor_hospital):
    resposta = None
    aviso = tk.Toplevel()
    aviso.title("Atenção")
    aviso.withdraw()

    # Widgets já no lugar antes de posicionar
    frame = tk.Frame(aviso, padx=10, pady=10)
    frame.pack(expand=True, fill="both")

    icone = tk.Label(frame, text="⚠️", font=("Arial", 24))
    icone.grid(row=0, column=0, sticky="n")

    texto_principal = tk.Label(
        frame,
        text=f"Transporte especial necessário para o paciente {paciente.nome}.",
        font=("Arial", 10, "bold"),
        justify="center",
        wraplength=largura - 60
    )
    texto_principal.grid(row=0, column=1, sticky="w", padx=10)

    texto_extra = tk.Label(
        frame,
        text=(
            f"\nExiste um {orgao.nome} disponível em {melhor_hospital}.\n"
            f"Entretanto, será preciso utilizar transporte especial para chegar em no máximo {orgao.tempo_isquemia} horas."
            f"\n\n\nO transporte especial vai ser utilizado?"
        ),
        font=("Arial", 10),
        justify="left",
        wraplength=largura - 20
    )
    texto_extra.grid(row=1, column=0, columnspan=2, sticky="w", pady=(10, 0))

    # Funções dos botões
    def escolher_sim():
        nonlocal resposta
        resposta = True
        aviso.destroy()

    def escolher_nao():
        nonlocal resposta
        resposta = False
        aviso.destroy()

    # Botões Sim e Não
    botoes = tk.Frame(aviso)
    botoes.pack(pady=20)

    btn_sim = tk.Button(botoes, text="Sim", width=10, command=escolher_sim)
    btn_sim.grid(row=0, column=0, padx=10)

    btn_nao = tk.Button(botoes, text="Não", width=10, command=escolher_nao)
    btn_nao.grid(row=0, column=1, padx=10)

    largura_tela = aviso.winfo_screenwidth()
    altura_tela = aviso.winfo_screenheight()
    x = (largura_tela // 2) - (largura // 2)
    y = (altura_tela // 2) - (altura // 2)
    aviso.geometry(f"{largura}x{altura}+{x}+{y}")
    # aviso.minsize(largura, altura)
    # aviso.maxsize(largura, altura)

    aviso.deiconify() 
    aviso.grab_set()
    aviso.focus_force()
    aviso.wait_window()
    
    # Aqui você decide o que fazer com a resposta
    if resposta is True:
        print("Usuário escolheu usar transporte especial.")
        pacientes.remove(paciente)
        orgaos.remove(orgao)
        return True
    elif resposta is False:
        print("Usuário NÃO vai usar transporte especial.")
        return False
    else:
        print("Janela foi fechada sem resposta.")  # Caso o usuário feche no X

def mostrar_resultado_final(paciente, orgao, melhor_hospital, melhor_algoritmo, melhor_caminho, menor_custo, menor_tempo):
    janela = tk.Toplevel()
    janela.withdraw()
    janela.title(f"Melhor Resultado - {melhor_algoritmo}")

    frame = tk.Frame(janela, padx=15, pady=15)
    frame.pack()

    # Título
    titulo = tk.Label(frame, text="✓ Órgão encontrado!", font=("Arial", 12, "bold"))
    titulo.pack(pady=(0, 10))

    # Infos formatadas
    infos = [
        ("Nome do paciente:", paciente.nome),
        ("Órgão:", orgao.nome),
        ("Hospital:", f"{melhor_hospital.nome} ({melhor_hospital.cidade})"),
        ("Algoritmo utilizado:", melhor_algoritmo),
        ("Caminho:", " -> ".join(melhor_caminho)),
        ("Custo total:", f"{menor_custo:.1f} km"),
        ("Tempo de busca:", f"{menor_tempo:.6f} s"),
    ]

    for titulo, valor in infos:
        linha = tk.Frame(frame)
        linha.pack(anchor="w", fill="x")
        label_titulo = tk.Label(linha, text=titulo, font=("Arial", 10, "bold"))
        label_titulo.pack(side="left")
        label_valor = tk.Label(linha, text=f" {valor}", font=("Arial", 10), wraplength=300, justify="left")
        label_valor.pack(side="left")

    # --- Gráfico do Matplotlib ---
    fig, ax = plt.subplots(figsize=(5, 3.5))
    desenhar_grafo(ax, coordenadas, distancias_cidades, caminho=melhor_caminho)
    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.draw()
    canvas.get_tk_widget().pack(pady=(20, 10))

    # Botão para fechar
    botao = tk.Button(frame, text="Fechar", width=12, command=janela.destroy)
    botao.pack(pady=(10, 0))

    # Centralizar janela
    largura_tela = janela.winfo_screenwidth()
    altura_tela = janela.winfo_screenheight()
    x = (largura_tela // 2) - (largura // 2)
    y = (altura_tela // 2) - (altura + 350 // 2)
    janela.wm_geometry(f"{largura}x{altura + 350}+{x}+{y}")
    # janela.minsize(largura, altura + 350)
    # janela.maxsize(largura, altura + 350)
    # janela.resizable(False, False)
    
    janela.deiconify() 
    janela.grab_set()
    janela.focus_force()
    janela.wait_window()

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
    for paciente in list(pacientes):  # Iterar sobre uma cópia da lista, pois a função realizar_busca remove pacientes da lista original
        if (realizar_busca(paciente, cidade_via_cep(hospitais, paciente.cep), paciente.orgao_solicitado)):
            print(f"Paciente {paciente.nome} removido da lista de espera.")
            print(f"Órgão {paciente.orgao_solicitado} encontrado para o paciente {paciente.nome}.\n")
    
    print("Banco de dados atualizado!")
    atualizar_treeviews()

def salvar_orgao(nome, cep, tipo_sanguineo):
    for o in orgaos_possiveis: 
        if (nome == o.nome): 
            tempo = o.tempo_isquemia
    novo_orgao = Orgao(nome, tempo, tipo_sanguineo, cep)
    orgaos.append(novo_orgao)
    print(f"Órgão adicionado: {nome}, {tempo} hr, CEP {cep}")
    
    pacientes_aguardando_orgao = []
    for paciente in pacientes:
        if (paciente.orgao_solicitado == novo_orgao.nome):
            pacientes_aguardando_orgao.append(paciente)
    ordenar_pacientes(pacientes_aguardando_orgao, hospitais, cidade_via_cep(hospitais, novo_orgao.cep))
    
    for paciente in list(pacientes_aguardando_orgao):
        orgaos_com_hospital = []
        hosp = next((h for h in hospitais if h.cep == novo_orgao.cep), None)
        if hosp:
            orgaos_com_hospital.append((novo_orgao, hosp))

        if (buscar_por_paciente(paciente, cidade_via_cep(hospitais, paciente.cep), orgaos_com_hospital)):
            pacientes_aguardando_orgao.remove(paciente)
            break
    atualizar_treeviews()

def atualizar_treeviews():
    # Limpa as treeviews
    tree_pacientes.delete(*tree_pacientes.get_children())
    tree_orgaos.delete(*tree_orgaos.get_children())

    # Adiciona pacientes
    for p in pacientes:
        tree_pacientes.insert("", "end", values=(p.nome, p.idade, p.orgao_solicitado, p.estado_gravidade, p.tipo_sanguineo, p.data_entrada.strftime("%d/%m/%Y")))

    # Adiciona órgãos
    for o in orgaos:
        tree_orgaos.insert("", "end", values=(o.nome, o.tempo_isquemia, o.tipo_sanguineo))

# Função do botão
def realizar_busca_interface():
    nome = entry_nome.get().strip()
    origem = var_cidade.get()
    idade = var_idade.get()
    orgao = var_orgao.get()
    tipos_sanguineo = combo_sangue.get()
    estado_gravidade = combo_gravidade.get()
    orgao = [o for o in orgaos_possiveis if o.nome == orgao]
    nome_orgao = var_orgao.get()
    
    if not nome or not origem or not nome_orgao:
        messagebox.showerror("Erro", "Preencha todos os campos.")
        return

    #datetime.combine(date.today(), datetime.min.time()) usado para garantir compatibilidade com o formato de data e permitir comparação entre datas na ordenação
    novo_paciente = Paciente(nome, datetime.combine(date.today(), datetime.min.time()), idade, cep_via_cidade(hospitais, origem), nome_orgao, tipos_sanguineo, estado_gravidade)
    pacientes.append(novo_paciente)
    atualizar_treeviews()

    if not orgaos:
        messagebox.showerror("Banco de doações vazio", "Não há órgãos disponíveis, paciente adicionado à lista de espera.")
        return False
    else:
        realizar_busca(novo_paciente, origem, nome_orgao)
    
def realizar_busca(paciente, cidade_origem, nome_orgao):
    if not orgaos:
        print("Não há órgãos disponíveis.")
        return False
    orgaos_disponiveis = [o for o in orgaos if o.nome == nome_orgao]

    if not orgaos_disponiveis:
        messagebox.showerror("Erro", f"Não há órgãos disponíveis do tipo {nome_orgao}.")
        return

    orgaos_com_hospital = []
    for orgao in orgaos_disponiveis:
        hosp = next((h for h in hospitais if h.cep == orgao.cep), None)
        if hosp:
            orgaos_com_hospital.append((orgao, hosp))

    if not orgaos_com_hospital:
        messagebox.showerror("Erro", "Nenhum hospital encontrado para os órgãos disponíveis.")
        return

    return buscar_por_paciente(paciente, cidade_origem, orgaos_com_hospital)

def buscar_por_paciente(paciente, cidade_origem, orgaos_com_hospital):
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
        print(f"\n  -> Buscando rotas até hospital: {hosp.nome} ({destino}). Paciente: {paciente.nome} ({paciente.estado_gravidade})")
        
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

                if sangue_compativel(paciente.tipo_sanguineo, orgao.tipo_sanguineo):
                    if custo < menor_custo:
                        melhor_hospital = hosp
                        melhor_algoritmo = nome_algoritmo
                        melhor_caminho = caminho
                        menor_custo = custo
                        menor_tempo = tempo_de_busca
                        orgao_final = orgao
                else:
                    print(f"    [X] {nome_algoritmo}: Sangue incompatível entre paciente ({paciente.tipo_sanguineo}) e órgão ({orgao.tipo_sanguineo}).")

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
        return mostrar_aviso(paciente, orgao, melhor_hospital)
    elif not melhor_caminho:
        print(f"[!] Nenhum caminho encontrado para o órgão {orgao.nome}.")
        messagebox.showerror("Erro", f"Pacientes incompatíveis com o órgão {orgao.nome}. Adicionado ao banco de órgãos")
        return False
    else:
        print(f"\n>>> Melhor resultado para {orgao.nome}:")
        print(f"    Paciente: {paciente.nome}")
        print(f"    Hospital escolhido: {melhor_hospital.nome} ({melhor_hospital.cidade})")
        print(f"    Algoritmo escolhido: {melhor_algoritmo}")
        print(f"    Custo total: {menor_custo:.1f} km")
        print(f"    Tempo de busca: {menor_tempo:.6f} s")

        mostrar_resultado_final(
            paciente, orgao, melhor_hospital, melhor_algoritmo, melhor_caminho, menor_custo, menor_tempo
        )

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

if not hospitais:
    raise RuntimeError("Falha ao carregar dados dos hospitais.")

if not orgaos:
    raise RuntimeError("Falha ao carregar dados dos órgãos.")

if not pacientes:
    raise RuntimeError("Falha ao carregar dados dos pacientes.")

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

# Tipo Sanguíneo
tk.Label(frame_busca, text="Tipo Sanguíneo:").pack(anchor='w', pady=(5, 0))
tipos_sanguineos = ["A", "B", "AB", "O"]
var_sangue = tk.StringVar(root)
var_sangue.set(tipos_sanguineos[0])
combo_sangue = ttk.Combobox(frame_busca, textvariable=var_sangue, values=tipos_sanguineos, state="readonly")
combo_sangue.pack(fill='x')

# Estado de Gravidade
tk.Label(frame_busca, text="Estado de Gravidade:").pack(anchor='w', pady=(5, 0))
estados_gravidade = ["crítico", "urgente", "moderado", "estável"]
var_gravidade = tk.StringVar(root)
var_gravidade.set(estados_gravidade[0])
combo_gravidade = ttk.Combobox(frame_busca, textvariable=var_gravidade, values=estados_gravidade, state="readonly")
combo_gravidade.pack(fill='x')

btn_busca = tk.Button(frame_busca, text="Realizar Busca", command=realizar_busca_interface)
btn_busca.pack(pady=(10, 0))

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
    entry_orgao.pack(fill='x')

    tk.Label(nova_janela, text="CEP de Origem:").pack(pady=5)
    var_cep = tk.StringVar(nova_janela)
    var_cep.set(f"{hospitais[0].cidade} - {hospitais[0].cep}") 
    entry_cep = ttk.Combobox(nova_janela, textvariable=var_cep, values=[f"{h.cidade} - {h.cep}" for h in hospitais], state="readonly")
    entry_cep.pack(fill='x')

    # Tipo Sanguíneo
    tk.Label(nova_janela, text="Tipo Sanguíneo:").pack(pady=5)
    tipos_sanguineos = ["A", "B", "AB", "O"]
    var_sangue = tk.StringVar(nova_janela)
    var_sangue.set(tipos_sanguineos[0])  
    combo_sangue = ttk.Combobox(nova_janela, textvariable=var_sangue, values=tipos_sanguineos, state="readonly")
    combo_sangue.pack(fill='x')

    btn_salvar = tk.Button(
        nova_janela, 
        text="Salvar", 
        command=lambda: (
            salvar_orgao(entry_orgao.get(), var_cep.get().split(" - ")[1], var_sangue.get()), 
            nova_janela.destroy()
        )
    )
    btn_salvar.pack(pady=10)
    largura_nova_janela = nova_janela.winfo_width()
    altura_nova_janela = nova_janela.winfo_height()

    largura_tela = nova_janela.winfo_screenwidth()
    altura_tela = nova_janela.winfo_screenheight()

    x = (largura_tela // 2) - (largura_nova_janela // 2)
    y = (altura_tela // 2) - (altura_nova_janela // 2)

    nova_janela.wm_geometry(f"{largura}x{altura}+{x}+{y}")

# --- Treeview de Pacientes ---
tk.Label(right_frame, text="Fila de Espera:").pack(anchor="w", padx=5, pady=(10, 0))

tree_pacientes = ttk.Treeview(
    right_frame, columns=("nome", "idade", "orgao", "gravidade", "tipo", "data"), show="headings", height=8
)
tree_pacientes.heading("nome", text="Nome", anchor='center')
tree_pacientes.heading("idade", text="Idade", anchor='center')
tree_pacientes.heading("orgao", text="Órgão Solicitado", anchor='center')
tree_pacientes.heading("gravidade", text="Estado", anchor='center')
tree_pacientes.heading("tipo", text="Tipo Sanguíneo", anchor='center')
tree_pacientes.heading("data", text="Data Entrada", anchor='center')

tree_pacientes.column("nome", anchor='center')
tree_pacientes.column("idade", anchor='center')
tree_pacientes.column("orgao", anchor='center')
tree_pacientes.column("gravidade", anchor='center')
tree_pacientes.column("tipo", anchor='center')
tree_pacientes.column("data", anchor='center')

tree_pacientes.pack(fill='x', padx=5, pady=5)

# --- Treeview de Órgãos disponíveis ---
tk.Label(right_frame, text="Órgãos Disponíveis:").pack(anchor="w", padx=5, pady=(10, 0))

tree_orgaos = ttk.Treeview(
    right_frame, columns=("nome", "tempo", "tipo"), show="headings", height=5
)
tree_orgaos.heading("nome", text="Nome", anchor='center')
tree_orgaos.heading("tempo", text="Tempo Isquemia (hrs)", anchor='center')
tree_orgaos.heading("tipo", text="Tipo Sanguíneo", anchor='center')

tree_orgaos.column("nome", anchor='center')
tree_orgaos.column("tempo", anchor='center')
tree_orgaos.column("tipo", anchor='center')

tree_orgaos.pack(fill='x', padx=5, pady=5)

btn_atualizar = tk.Button(right_frame, text="Atualizar fila de espera", command=lambda: atualizar_banco_de_dados(pacientes, hospitais))
btn_atualizar.pack(fill='x', padx=5, pady=(10, 0))

# --- Centralizar janela principal ---
root.update_idletasks()
largura_janela_principal = root.winfo_width()
altura_janela_principal = root.winfo_height()

largura_tela = root.winfo_screenwidth()
altura_tela = root.winfo_screenheight()

x = (largura_tela // 2) - (largura_janela_principal // 2)
y = (altura_tela // 2) - (altura_janela_principal // 2)

root.geometry(f"+{x}+{y}")

# --- Inicializa os dados nas tabelas ---
atualizar_treeviews()

root.mainloop()
