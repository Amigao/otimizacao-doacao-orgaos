import heapq
import math
import grafo
import matplotlib.pyplot as plt


# Dados das arestas entre cidades (g(n))
distancias_cidades = [
    ("SJ Preto", "Ribeirão Preto", 168),
    ("Ribeirão Preto", "São Paulo", 291),
    ("São Paulo", "SJ Preto", 416),
    ("São Paulo", "BarraMansa", 279),
    ("BarraMansa", "Rio de Janeiro", 79),
    ("Rio de Janeiro", "Vitória", 517)
]

# Exemplo de coordenadas para cada cidade (valores fictícios para demonstração)
coordenadas = {
    "SJ Preto": (0, 0),
    "Ribeirão Preto": (100, 30),
    "São Paulo": (200, 50),
    "BarraMansa": (300, 20),
    "Rio de Janeiro": (400, 100),
    "Vitória": (500, 150)
}

# Construindo o grafo a partir da lista de arestas.
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
## Basicamente AQUI ESTÁ A IMPLEMENTAÇÃO DO ALGORITMO A*
#A* é um algoritmo de busca que utiliza uma heurística para guiar a busca
# O algoritmo A* combina a busca de custo uniforme com a busca informada
def astar(grafo, inicio, meta, coords):

    open_set = []
    h_inicial = calc_heuristica(inicio, meta, coords)
    heapq.heappush(open_set, (h_inicial, inicio, 0))
    
    came_from = {}  # Para reconstrução do caminho
    g_score = {inicio: 0}  # Custo conhecido para cada cidade

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
        
        # Explora os vizinhos do nó atual
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

inicio = "Vitória"
meta = "SJ Preto"  # Altere a cidade meta conforme necessário

caminho, custo_total = astar(grafo, inicio, meta, coordenadas)

if caminho:
    print("Caminho escolhido:", " -> ".join(caminho))
    print("Custo Final:", custo_total)
else:
    print(f"Não foi encontrado um caminho de {inicio} até {meta}.")
