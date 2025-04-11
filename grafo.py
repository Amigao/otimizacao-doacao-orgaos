import heapq
from collections import defaultdict, deque
import networkx as nx
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from interface_hospitais import *
from cep2coord import *
from interface_orgaos import *


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
                       llcrnrlat=-35, urcrnrlat=5,
                       llcrnrlon=-75, urcrnrlon=-30,
                       resolution='i')

        mapa.drawcoastlines()
        mapa.drawcountries()
        mapa.drawstates()
        mapa.drawmapboundary()
        mapa.drawparallels(range(-30, 5, 5), labels=[1,0,0,0])
        mapa.drawmeridians(range(-70, -30, 5), labels=[0,0,0,1])

        # Converter as coordenadas e desenhar vértices
        posicoes_proj = {}
        for cidade, (lat, lon) in self.vertices.items():
            x, y = mapa(lon, lat)
            posicoes_proj[cidade] = (x, y)
            plt.plot(x, y, 'bo', markersize=7)
            plt.text(x + 10000, y + 10000, cidade, fontsize=10, weight='bold')

        # Desenhar as arestas
        for v1, v2, _ in self.arestas:
            x1, y1 = posicoes_proj[v1]
            x2, y2 = posicoes_proj[v2]
            plt.plot([x1, x2], [y1, y2], 'gray', linewidth=1)

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

i = 0
for coord in coords:
    grafo.adicionar_vertice(hospitais[i].nome, float(coords[i][0]), float(coords[i][1]))
    i = i+1

print("<< Vértices do Grafo >>")
for v in grafo.vertices.items():
    print(v[0])
    print("Coordenadas: ", v[1], "\n")

grafo.adicionar_aresta('CNCDOSC', 'OPO I ISCMPA', 430)

#caminho, custo = grafo.caminho_minimo('São Paulo', 'Brasília')
#print("Caminho mínimo:", caminho)
#print("Custo total:", custo)

grafo.desenhar_mapa()
