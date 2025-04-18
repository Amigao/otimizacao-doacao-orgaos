import networkx as nx
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature

try:
    from Hospital import carregar_hospitais
    #from Orgao import carregar_orgaos
    from coord import carregar_coordenadas
except ModuleNotFoundError:
    from funcoes.Hospital import carregar_hospitais
    #from funcoes.Orgao import carregar_orgaos
    from funcoes.coord import carregar_coordenadas

class GrafoGeografico:
    def __init__(self):
        self.vertices = {}     # Armazena: nome -> (lat, lon)
        self.arestas = []      # Lista de arestas: (v1, v2, peso)
        self.grafo_nx = nx.Graph()
    
    def adicionar_vertice(self, nome, lat, lon):
        self.vertices[nome] = (lat, lon)
        # Armazena no grafo do networkx usando (lon, lat) para compatibilidade com as projeções
        self.grafo_nx.add_node(nome, pos=(lon, lat))
    
    def adicionar_aresta(self, v1, v2, peso):
        if v1 not in self.vertices or v2 not in self.vertices:
            raise ValueError("Todos os vértices devem ter coordenadas definidas.")
        self.arestas.append((v1, v2, peso))
        self.grafo_nx.add_edge(v1, v2, weight=peso)
    
    def desenhar_mapa(self, caminho_destacado=None):
        # Cria a figura com projeção Mercator usando Cartopy
        fig, ax = plt.subplots(figsize=(12, 10), subplot_kw={'projection': ccrs.Mercator()})
        
        # Define o extent: [lon_min, lon_max, lat_min, lat_max] em crs PlateCarree (lat/lon)
        ax.set_extent([-75, -30, -35, 5], crs=ccrs.PlateCarree())
        
        # Adiciona características do mapa
        ax.add_feature(cfeature.COASTLINE)
        ax.add_feature(cfeature.BORDERS, linestyle=':')
        ax.add_feature(cfeature.STATES, linestyle=':')
        ax.add_feature(cfeature.LAND, edgecolor='black')
        ax.add_feature(cfeature.OCEAN)
        ax.gridlines(draw_labels=True, linestyle='--')
        
        # Converter as coordenadas dos vértices e desenhá-los
        # Como usamos Cartopy com crs=PlateCarree(), as coordenadas (lon, lat) são usadas diretamente
        posicoes_proj = {}
        for cidade, (lat, lon) in self.vertices.items():
            posicoes_proj[cidade] = (lon, lat)  # Armazena os valores originais
            ax.plot(lon, lat, 'bo', markersize=7, transform=ccrs.PlateCarree())
            ax.text(lon + 0.1, lat + 0.1, cidade, fontsize=10, weight='bold', transform=ccrs.PlateCarree())
        
        # Desenhar as arestas entre os vértices
        for v1, v2, _ in self.arestas:
            lon1, lat1 = posicoes_proj[v1]
            lon2, lat2 = posicoes_proj[v2]
            ax.plot([lon1, lon2], [lat1, lat2], color='gray', linewidth=1, transform=ccrs.PlateCarree())
        
        # Destacar um caminho (se fornecido)
        if caminho_destacado:
            for i in range(len(caminho_destacado) - 1):
                v1 = caminho_destacado[i]
                v2 = caminho_destacado[i + 1]
                lon1, lat1 = posicoes_proj[v1]
                lon2, lat2 = posicoes_proj[v2]
                ax.plot([lon1, lon2], [lat1, lat2], color='red', linewidth=3, transform=ccrs.PlateCarree())
        
        ax.set_title('Rede de Cidades')
        plt.show()


# Exemplo de uso - rodável usando [python funcoes/Grafo.py]
if __name__ == "__main__":
    # Carrega os dados dos arquivos (certifique-se de que esses arquivos existam e estejam formatados corretamente)
    coords = carregar_coordenadas("dados/coordenadas.txt")
    hospitais = carregar_hospitais("dados/hospitais.txt")

    grafo = GrafoGeografico()

    # Adiciona os vértices ao grafo: cada hospital (ou cidade) recebe suas coordenadas
    for i, coord in enumerate(coords):
        grafo.adicionar_vertice(hospitais[i].nome, float(coord[0]), float(coord[1]))

    print("<< Vértices do Grafo >>")
    for v, coord in grafo.vertices.items():
        print(v)
        print("Coordenadas:", coord, "\n")

    # Adiciona uma aresta de exemplo
    #grafo.adicionar_aresta('CNCDOSC', 'OPO I ISCMPA', 430)

    # Se desejar, pode calcular e destacar um caminho mínimo (exemplo comentado)
    # caminho, custo = grafo.caminho_minimo('São Paulo', 'Brasília')
    # print("Caminho mínimo:", caminho)
    # print("Custo total:", custo)

    # Desenha o mapa com o grafo e, opcionalmente, um caminho destacado
    grafo.desenhar_mapa()
