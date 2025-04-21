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
    ("São Paulo", "Campinas", 99),
    ("Campinas", "Ribeirão Preto", 210),
    ("São Paulo", "Sorocaba", 102),
    ("Presidente Prudente", "São José do Rio Preto", 263),
    ("Presidente Prudente", "Ribeirão Preto", 325),
    ("Presidente Prudente", "Uberlândia", 368),
    ("Campinas", "Sorocaba", 96),
    ("Sorocaba", "Barra Mansa", 256),
    ("Campinas", "Barra Mansa", 275),
    ("Belo Horizonte", "Vitória", 524),
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
    "São José do Rio Preto": (64, 95),
    "Ribeirão Preto": (150, 80),
    "São Paulo": (200, 50),
    "Campinas": (180, 60),
    "Sorocaba": (180, 40),
    "Presidente Prudente": (10, 75),
    "Barra Mansa": (300, 20),
    "Rio de Janeiro": (400, 100),
    "Vitória": (500, 150),
    "Uberlândia": (179, 130),
    "Belo Horizonte": (300, 120),
}


