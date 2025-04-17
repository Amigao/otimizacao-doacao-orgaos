import heapq
import math
import matplotlib.pyplot as plt

# Dados das arestas entre cidades (g(n))
distancias_cidades = [
    ("São José do Rio Preto", "Ribeirão Preto", 168),
    ("Ribeirão Preto", "São Paulo", 291),
    ("São Paulo", "São José do Rio Preto", 416),
    ("São Paulo", "BarraMansa", 279),
    ("BarraMansa", "Rio de Janeiro", 79),
    ("Rio de Janeiro", "Vitória", 517),
    ("São José do Rio Preto", "Uberlândia", 318),
    ("Uberlândia", "Belo Horizonte", 240),
]

# Atualize o dicionário de coordenadas para incluir também Uberlândia e Belo Horizonte
coordenadas = {
    "São José do Rio Preto": (64,95),
    "Ribeirão Preto": (150, 80),
    "São Paulo": (200, 50),
    "BarraMansa": (300, 20),
    "Rio de Janeiro": (400, 100),
    "Vitória": (500, 150),
    "Uberlândia": (179, 130),      
    "Belo Horizonte": (300, 120)     
}

# Construindo o grafo (dicionário de vizinhança) a partir da lista de arestas.
grafo = {}
for origem, destino, custo in distancias_cidades:
    if origem not in grafo:
        grafo[origem] = []
    grafo[origem].append((destino, custo))
    if destino not in grafo:
         grafo[destino] = []
    grafo[destino].append((origem, custo))

def calc_heuristica(cidade, meta, coords):
    x1, y1 = coords[cidade]
    x2, y2 = coords[meta]
    return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)

#----------------------------------
# Implementação do algoritmo A*
def astar(grafo, inicio, meta, coords):
    open_set = []
    h_inicial = calc_heuristica(inicio, meta, coords)
    heapq.heappush(open_set, (h_inicial, inicio, 0))
    
    came_from = {}   # Para reconstruir o caminho
    g_score = {inicio: 0}  # Custo real acumulado até cada cidade

    print(f"Inicializando A* com nó de partida: {inicio}")
    
    while open_set:
        f_atual, atual, g_atual = heapq.heappop(open_set)

        # Verifica se já chegou na meta
        if atual == meta:
            caminho = []
            while atual in came_from:
                caminho.append(atual)
                atual = came_from[atual]
            caminho.append(inicio)
            caminho.reverse()
            print("\nMeta alcançada!")
            return caminho, g_score[meta]
        
        # Explora os vizinhos
        for vizinho, custo in grafo.get(atual, []):
            novo_g = g_atual + custo
            h_vizinho = calc_heuristica(vizinho, meta, coords)
            f_vizinho = novo_g + h_vizinho

            if vizinho not in g_score or novo_g < g_score[vizinho]:
                g_score[vizinho] = novo_g
                heapq.heappush(open_set, (f_vizinho, vizinho, novo_g))
                came_from[vizinho] = atual
    return None, float('inf')
#----------------------------------

inicio = "São Paulo"  
meta = "Belo Horizonte"  

caminho, custo_total = astar(grafo, inicio, meta, coordenadas)

if caminho:
    print("Caminho escolhido:", " -> ".join(caminho))
    print("Custo Final:", custo_total)
else:
    print(f"Não foi encontrado um caminho de {inicio} até {meta}.")


#print("\nPosições no Plano Cartesiano:")
#for cidade, pos in coordenadas.items():
#    print(f"{cidade}: {pos}")

plt.figure(figsize=(8, 6))

for cidade, (x, y) in coordenadas.items():
    plt.plot(x, y, 'bo')  
    plt.text(x + 2, y + 2, cidade, fontsize=9)

# Plota as arestas. Para evitar desenhar a mesma aresta duas vezes, percorremos a lista de distancias_cidades.
desenhadas = set()
for origem, destino, custo in distancias_cidades:
    chave = tuple(sorted((origem, destino)))
    if chave in desenhadas:
        continue
    desenhadas.add(chave)
    x1, y1 = coordenadas[origem]
    x2, y2 = coordenadas[destino]
    plt.plot([x1, x2], [y1, y2], 'k-', lw=1)

plt.xlabel("X")
plt.ylabel("Y")
plt.title("Grafo no Plano Cartesiano")
plt.grid(False)
plt.show()
