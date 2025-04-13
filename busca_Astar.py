import heapq
import math

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
# Cada cidade de origem aponta para uma lista de (cidade vizinha, custo)
grafo = {}
for origem, destino, custo in distancias_cidades:
    if origem not in grafo:
        grafo[origem] = []
    grafo[origem].append((destino, custo))

def calc_heuristica(cidade, meta, coords):
    """
    Calcula a heurística como a distância euclidiana entre 'cidade' e 'meta'
    utilizando as coordenadas fornecidas.
    """
    x1, y1 = coords[cidade]
    x2, y2 = coords[meta]
    return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)

def astar(grafo, inicio, meta, coords):

    # A fila de prioridade guarda tuplas (f, cidade, g), onde f = g + h.
    open_set = []
    h_inicial = calc_heuristica(inicio, meta, coords)
    heapq.heappush(open_set, (h_inicial, inicio, 0))
    
    # Dicionário que guarda de onde viemos para reconstruir o caminho.
    came_from = {}
    
    g_score = {inicio: 0}
    
    while open_set:
        f_val, atual, g_val = heapq.heappop(open_set)
        
        if atual == meta:
            # Reconstrução do caminho percorrido.
            caminho = []
            while atual in came_from:
                caminho.append(atual)
                atual = came_from[atual]
            caminho.append(inicio)
            caminho.reverse()
            return caminho, g_score[meta]
        
        for vizinho, custo in grafo.get(atual, []):
            novo_g = g_val + custo
            if vizinho not in g_score or novo_g < g_score[vizinho]:
                g_score[vizinho] = novo_g
                # Calcula o valor f usando a heurística dinâmica em relação à meta atual.
                f_valor = novo_g + calc_heuristica(vizinho, meta, coords)
                heapq.heappush(open_set, (f_valor, vizinho, novo_g))
                came_from[vizinho] = atual

    return None, float('inf')

inicio = "SJ Preto"
meta = "BarraMansa"  # Altere para outra cidade se necessário

caminho, custo_total = astar(grafo, inicio, meta, coordenadas)

if caminho:
    print("Caminho escolhido:", " -> ".join(caminho))
    print("Custo total:", custo_total)
else:
    print("Não foi encontrado um caminho de", inicio, "até", meta)
