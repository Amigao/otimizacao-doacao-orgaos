def busca_em_largura(grafo, cidade_inicial, cidade_meta):
    from collections import deque

    fila = deque([(cidade_inicial, [cidade_inicial], 0)])
    visitados = set()

    while fila:
        vertice, caminho, custo = fila.popleft()

        if vertice == cidade_meta:
            return caminho, custo

        if vertice not in visitados:
            visitados.add(vertice)
            for vizinho, custo_aresta in grafo.get(vertice, []):
                if vizinho not in visitados:
                    fila.append((vizinho, caminho + [vizinho], custo + custo_aresta))

    return None, float('inf')
