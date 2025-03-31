from interface_hospitais import carregar_hospitais
from interface_orgaos import Orgao
import requests
from collections import deque
from math import radians, sin, cos, sqrt, atan2

#Funções novas adicionadas e ainda verificaar:
# obter_coordenadas(), calcular_distancia(), encontrar_hospital_mais_proximo()
# O resto ta igual, apenas criei essas para realizar a busca, basicamente a minha ideia
# é que o paciente informe o cep dele e a partir disso eu busco o hospital mais próximo, tambem
#se baseando no CEP. Ainda precisa ponderar outras coisas como a quantidade de órgãos disponíveis
#
#

class EstadoTransplante:
    def __init__(self, estado, pacientes_aguardando=None, pacientes_alocados=None, hospital=None):
        self.estado = estado
        self.pacientes_aguardando = pacientes_aguardando or []
        self.pacientes_alocados = pacientes_alocados or []
        self.hospital = hospital or []

    def __repr__(self):
        return (f"EstadoTransplante(Estado: {self.estado}, "
                f"Pacientes aguardando: {self.pacientes_aguardando}, "
                f"Pacientes alocados: {self.pacientes_alocados}, "
                f"Hospitais: {self.hospital})")

# Função para obter as coordenadas geográficas (latitude e longitude) de um CEP usando ViaCEP
def obter_coordenadas(cep):
    url = f"https://viacep.com.br/ws/{cep}/json/"
    response = requests.get(url)
    dados = response.json()
    
    if 'erro' in dados:
        print(f"Erro ao consultar o CEP {cep}.")
        return None, None  # Retorna None se o CEP for inválido
    
    # Exemplo de coordenadas fictícias para o CEP, ainda 
    return -23.5505, -46.6333  

# Função para calcular a distância entre duas coordenadas geográficas usando a fórmula de Haversine
def calcular_distancia(lat1, lon1, lat2, lon2):
    # Converter de graus para radianos
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    
    # Fórmula de Haversine
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    
    # Raio da Terra em km
    R = 6371.0
    
    return R * c

# Função para criar os EstadosTransplante a partir dos Hospitais
def criar_estados_transplante(hospitais):
    estados_dict = {}

    for hospital in hospitais:
        estado = hospital.estado
        if estado not in estados_dict:
            estados_dict[estado] = EstadoTransplante(estado, hospital=[])  # Criando EstadoTransplante
        estados_dict[estado].hospital.append(hospital)  # Adicionando hospitais ao estado

    return list(estados_dict.values())

# Função para carregar órgãos aos hospitais e associar os órgãos aos hospitais pelo CEP
def carregar_orgaos(nome_arquivo, estados_transplante):
    for estado in estados_transplante:
        hospitais_dict = {hospital.cep: hospital for hospital in estado.hospital}

        with open(nome_arquivo, "r", encoding="utf-8") as arquivo:
            for linha in arquivo:
                if linha.strip():  # Ignora linhas vazias
                    dados = linha.strip().split(',')
                    if len(dados) == 3:
                        nome, data_captação, hospital_cep = dados
                        orgao = Orgao(nome=nome, data_captação=data_captação)

                        if hospital_cep in hospitais_dict:
                            hospitais_dict[hospital_cep].orgaos_disponiveis.append(orgao)
                            print(f"Órgão {orgao.nome} adicionado ao hospital {hospitais_dict[hospital_cep].nome} ({hospital_cep}).")



# Função para encontrar o hospital mais próximo com base no CEP do paciente
def encontrar_hospital_mais_proximo(cep_paciente, hospitais):
    paciente_lat, paciente_lon = obter_coordenadas(cep_paciente)
    
    if paciente_lat is None or paciente_lon is None:
        print("CEP do paciente inválido.")
        return None
    
    hospital_mais_proximo = None
    menor_distancia = float('inf')

    for hospital in hospitais:
        hospital_lat, hospital_lon = obter_coordenadas(hospital.cep)
        
        if hospital_lat is not None and hospital_lon is not None:
            distancia = calcular_distancia(paciente_lat, paciente_lon, hospital_lat, hospital_lon)
            print(f"Distância do paciente para o hospital {hospital.nome}: {distancia} km.")  # Debug: Exibe a distância
            
            if distancia < menor_distancia:
                menor_distancia = distancia
                hospital_mais_proximo = hospital

    return hospital_mais_proximo



# Exemplo de uso
hospitais = carregar_hospitais("hospitais.txt")  # Função fictícia, deve carregar hospitais com seus dados
estados_transplante = criar_estados_transplante(hospitais)

# Carregar órgãos para os hospitais de cada estado
carregar_orgaos("mock_orgaos.txt", estados_transplante)

# Exemplo de paciente com CEP
cep_paciente = "57010001"  # CEP do paciente (exemplo do hospital)
hospital_mais_proximo = encontrar_hospital_mais_proximo(cep_paciente, hospitais)

if hospital_mais_proximo:
    print(f"O hospital mais próximo do paciente é {hospital_mais_proximo.nome}.")
else:
    print("Não foi possível encontrar um hospital próximo.")
