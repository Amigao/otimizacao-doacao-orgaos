# Dados das arestas entre cidades (g(n))
distancias_cidades = [
    ("São José do Rio Preto", "Ribeirão Preto", 168),
    ("Ribeirão Preto", "São Paulo", 291),
    ("São Paulo", "São José do Rio Preto", 416),
    ("São Paulo", "Barra Mansa", 279),
    ("Barra Mansa", "Rio de Janeiro", 79),
    ("Rio de Janeiro", "Vitória", 517),
    ("São José do Rio Preto", "Uberlândia", 318),
    ("Uberlândia", "Belo Horizonte", 240),
]

# Construindo o grafo (dicionário de vizinhança) a partir da lista de arestas.
grafo_distancias = {}
for origem, destino, custo in distancias_cidades:
    if origem not in grafo_distancias:
        grafo_distancias[origem] = []
    grafo_distancias[origem].append((destino, custo))
    if destino not in grafo_distancias:
         grafo_distancias[destino] = []
    grafo_distancias[destino].append((origem, custo))

# Coordenadas de cada cidade
coordenadas = {
    "São José do Rio Preto": (64,95),
    "Ribeirão Preto": (150, 80),
    "São Paulo": (200, 50),
    "Barra Mansa": (300, 20),
    "Rio de Janeiro": (400, 100),
    "Vitória": (500, 150),
    "Uberlândia": (179, 130),      
    "Belo Horizonte": (300, 120)     
}