import re

class Hospital:
    def __init__(self, estado, cidade, nome, cep, orgaos_disponiveis=None):
        self.estado = estado
        self.cidade = cidade
        self.nome = nome
        self.cep = cep  
        self.orgaos_disponiveis = orgaos_disponiveis or []


    def __repr__(self):
        return f"{self.nome}, ({self.cidade}-{self.estado}, {self.cep})" 
        # Orgaos: {self.orgaos_disponiveis})"

def carregar_hospitais(nome_arquivo):
    localizacoes = []

    with open(nome_arquivo, "r", encoding="utf-8") as arquivo:
        for linha in arquivo:
            if linha.strip():  # Ignora linhas vazias
                # Usa regex para capturar os dados corretamente
                match = re.match(r"([A-Z]{2}) - (.*?):\s*“(.*?)”\s*- CEP:\s*([\d.-]+)", linha.strip())
                if match:
                    estado, cidade, nome_hospital, cep = match.groups()

                    # Cria o objeto Hospital com as informações
                    hospital = Hospital(estado, cidade, nome_hospital, cep)

                    # Adiciona o hospital à lista de localizações
                    localizacoes.append(hospital)

    return localizacoes

def carregar_coordenadas(arq):

    coords = []

    with open(arq, "r", encoding="utf-8") as arquivo:
        for linha in arquivo:
            if linha.strip():  # Ignora linhas vazias
                dados = linha.strip().split(',')
                if len(dados) == 2:
                    lat, lon = dados
                    coords.append((lat, lon))

    return coords

# Exemplo de uso
#hospitais = carregar_hospitais("hospitais.txt")
#for hospital in hospitais:
  #  print(hospital)
