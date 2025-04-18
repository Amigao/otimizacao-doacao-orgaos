def busca_em_largura(grafo, cidade_atual, cidade_meta):
    visitados = set()
    fila = [(cidade_atual, [cidade_atual])]  # (nó atual, caminho percorrido)

    while fila:
        vertice, caminho = fila.pop(0)  # remove o primeiro elemento da lista

        if vertice == cidade_meta:
            print(f"Encontrado: {cidade_meta}")
            print(f"Caminho: {' -> '.join(caminho)}")
            return caminho

        if vertice not in visitados:
            visitados.add(vertice)
            for vizinho in grafo[vertice]:
                if vizinho not in visitados:
                    fila.append((vizinho, caminho + [vizinho]))

    print(f"Nó '{cidade_meta}' não encontrado.")
    return None
