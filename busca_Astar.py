import networkx as nx
import heapq

# Criar o grafo
G = nx.Graph()

edges = [
    ("SJ Preto", "Ribeirão Preto", 168),
    ("Ribeirão Preto", "São Paulo", 291),
    ("São Paulo", "SJ Preto", 416),
    ("São Paulo", "BarraMansa", 279),
    ("BarraMansa", "Rio de Janeiro", 79),
    ("Rio de Janeiro", "Vitória", 517)
]

G.add_weighted_edges_from(edges)

# Heurística (distância em linha reta até Vitória)
heuristica = {
    "SJ Preto": 990,
    "Ribeirão Preto": 822,
    "São Paulo": 730,
    "BarraMansa": 627,
    "Rio de Janeiro": 521,
    "Vitória": 0
}

def a_star_search(graph, start, goal, heuristic):
    # Fila de prioridade: (f(n), g(n), cidade atual, caminho)
    fila = [(heuristic[start], 0, start, [start])]
    visitados = set()

    while fila:
        f, g, atual, caminho = heapq.heappop(fila)

        if atual in visitados:
            continue
        visitados.add(atual)

        if atual == goal:
            return caminho, g

        for vizinho in graph.neighbors(atual):
            if vizinho not in visitados:
                custo_g = g + graph[atual][vizinho]['weight']
                custo_f = custo_g + heuristic[vizinho]
                heapq.heappush(fila, (custo_f, custo_g, vizinho, caminho + [vizinho]))

    return None, float("inf")

# Executar busca A*
caminho, distancia_total = a_star_search(G, "SJ Preto", "Vitória", heuristica)

# Exibir resultados
print("Caminho (A*):", " -> ".join(caminho))
print("Distância total (km):", distancia_total)
tempo_estimado = distancia_total / 90
print("Tempo estimado (horas):", tempo_estimado)
