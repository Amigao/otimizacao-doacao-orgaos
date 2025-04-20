import heapq
import math

from dados.cidades import coordenadas

def heuristica_A_estrela(cidade_atual, cidade_meta):
    # h(n) do algoritmo: distância em linha reta entre a cidade atual e a meta

    x1, y1 = coordenadas[cidade_atual]
    x2, y2 = coordenadas[cidade_meta]
    return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)

def A_estrela(grafo, cidade_inicial, cidade_meta):
    # Base do algoritmo A*

    open_set = []
    h_inicial = heuristica_A_estrela(cidade_inicial, cidade_meta)
    heapq.heappush(open_set, (h_inicial, cidade_inicial, 0))
    
    came_from = {}   # Para reconstruir o caminho
    g_score = {cidade_inicial: 0}  # Custo real acumulado até cada cidade

    print(f"Inicializando A* com nó de partida: {cidade_inicial}")
    
    while open_set:
        f_atual, atual, g_atual = heapq.heappop(open_set)

        # Verifica se já chegou na meta
        if atual == cidade_meta:
            caminho = []
            while atual in came_from:
                caminho.append(atual)
                atual = came_from[atual]
            caminho.append(cidade_inicial)
            caminho.reverse()
            return caminho, g_score[cidade_meta]
        
        # Explora os vizinhos
        for vizinho, custo in grafo.get(atual, []):
            novo_g = g_atual + custo
            h_vizinho = heuristica_A_estrela(vizinho, cidade_meta)
            f_vizinho = novo_g + h_vizinho

            if vizinho not in g_score or novo_g < g_score[vizinho]:
                g_score[vizinho] = novo_g
                heapq.heappush(open_set, (f_vizinho, vizinho, novo_g))
                came_from[vizinho] = atual

    return None, float('inf')
#----------------------------------

