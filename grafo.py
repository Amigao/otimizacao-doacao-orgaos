from interface_hospitais import *
from interface_orgaos import *
from calc_distancia_entre_2_coord import *
from cep2coord import *
from plan_to_matrix import *
import numpy as np
import heapq
from collections import defaultdict, deque
import networkx as nx
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap



class GrafoGeografico:
    def __init__(self):
        self.vertices = {}
        self.arestas = []
        self.grafo_nx = nx.Graph()

    def adicionar_vertice(self, nome, lat, lon):
        self.vertices[nome] = (lat, lon)
        self.grafo_nx.add_node(nome, pos=(lon, lat))  # OBS: (lon, lat) para mapas

    def adicionar_aresta(self, v1, v2, peso):
        if v1 not in self.vertices or v2 not in self.vertices:
            raise ValueError("Todos os vértices devem ter coordenadas definidas.")
        self.arestas.append((v1, v2, peso))
        self.grafo_nx.add_edge(v1, v2, weight=peso)

    def desenhar_mapa(self, caminho_destacado=None):
        plt.figure(figsize=(12, 10))

        # Criar o mapa com uma projeção geográfica
        mapa = Basemap(projection='merc',
                       llcrnrlat=-25.5, urcrnrlat=-19.5,
                       llcrnrlon=-53.5, urcrnrlon=-44,
                       resolution='i')

        mapa.drawcoastlines()
        mapa.drawcountries()
        mapa.drawstates()
        mapa.drawmapboundary()
        mapa.drawparallels(range(-25, -23, 1), labels=[1,0,0,0])
        mapa.drawmeridians(range(-48, -46, 1), labels=[0,0,0,1])

        # Converter as coordenadas e desenhar vértices
        posicoes_proj = {}
        id_vertices = 0
        for cidade, (lat, lon) in self.vertices.items():
            x, y = mapa(lon, lat)
            posicoes_proj[cidade] = (x, y)
            plt.plot(x, y, 'bo', markersize=7)
            plt.text(x + 10000, y + 10000, id_vertices, fontsize=7, weight='normal')
            id_vertices = id_vertices + 1

        # Desenhar as arestas
        for v1, v2, _ in self.arestas:
            x1, y1 = posicoes_proj[v1]
            x2, y2 = posicoes_proj[v2]
            plt.plot([x1, x2], [y1, y2], 'black', linewidth=1)

        # Destacar caminho mínimo, se houver
        if caminho_destacado:
            for i in range(len(caminho_destacado) - 1):
                v1 = caminho_destacado[i]
                v2 = caminho_destacado[i+1]
                x1, y1 = posicoes_proj[v1]
                x2, y2 = posicoes_proj[v2]
                plt.plot([x1, x2], [y1, y2], 'r-', linewidth=3)

        plt.title('Rede de Cidades')
        plt.show()


# Exemplo de uso
grafo = GrafoGeografico()

coords = carregar_coordenadas("coordenadas.txt")
hospitais = carregar_hospitais("hospitais.txt")

matriz_adjacencias = ler_matriz_adjacencias("matriz_adj.xlsx", "Plan1")

hospitais = carregar_hospitais("hospitais.txt")

orgaos = carregar_orgaos("orgaos.txt")
print("Órgão adicionado ao sistema!")
print(orgaos[0])
print("")

# ADICIONANDO VERTICES
i = 0
for coord in coords:
    grafo.adicionar_vertice(hospitais[i].nome, float(coords[i][0]), float(coords[i][1]))
    i = i+1

print("<< Vértices do Grafo >>")

#ADICIONANDO AS ARESTAS E PRINTANDO VERTICES
vertices = list(grafo.vertices.items())
i = 0
for v1 in vertices:
    print(i, ":", v1[0]) # print dos hospitais (vertices)
    print("Coordenadas: ", v1[1], v1[1][0], v1[1][1], "\n")
    j = 0
    for v2 in vertices:
        if matriz_adjacencias[i][j] == 1 or matriz_adjacencias[j][i] == 1:
            distancia = calcular_distancia(float(v1[1][0]), float(v1[1][1]), float(v2[1][0]), float(v2[1][1]))
            grafo.adicionar_aresta(str(v1[0]), str(v2[0]), distancia)
        j = j+1
    i = i+1



grafo.desenhar_mapa()
