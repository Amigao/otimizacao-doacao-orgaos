from interface_hospitais import carregar_hospitais
from interface_orgaos import *
import requests
from collections import deque
from math import radians, sin, cos, sqrt, atan2
from cep2coord import *

#Funções novas adicionadas e ainda verificaar:
# obter_coordenadas(), calcular_distancia(), encontrar_hospital_mais_proximo()
# O resto ta igual, apenas criei essas para realizar a busca, basicamente a minha ideia
# é que o paciente informe o cep dele e a partir disso eu busco o hospital mais próximo, tambem
#se baseando no CEP. Ainda precisa ponderar outras coisas como a quantidade de órgãos disponíveis
#
#

class Demanda:
    def __init__(self, pacientes_aguardando=None, fila_prioridade=None):
        self.pacientes_aguardando = pacientes_aguardando or []
        self.fila_prioridade = fila_prioridade or []

    def __repr__(self):
        return (f"Pacientes aguardando: {self.pacientes_aguardando}")

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


# Função para encontrar o hospital mais próximo ao órgão ofertado
def encontrar_hospital_mais_proximo(cep_paciente, hospitais):
    paciente_lat, paciente_lon = get_coordinates_from_cep(cep_paciente)
    
    if paciente_lat is None or paciente_lon is None:
        print("CEP do órgão inválido.")
        return None
    
    hospital_mais_proximo = None
    menor_distancia = float('inf')

    for hospital in hospitais:
        print(hospital)
        hospital_lat, hospital_lon = get_coordinates_from_cep(hospital.cep)
        
        if hospital_lat is not None and hospital_lon is not None:
            distancia = calcular_distancia(paciente_lat, paciente_lon, hospital_lat, hospital_lon)
            print(f"Distância: {distancia} km.")  # Debug: Exibe a distância
            print("")
            
            if distancia < menor_distancia:
                menor_distancia = distancia
                hospital_mais_proximo = hospital

    return hospital_mais_proximo



# --------- E X E M P L O   D E   U S O --------------

hospitais = carregar_hospitais("hospitais.txt")

orgaos = carregar_orgaos("mock_orgaos.txt")
print("Órgão adicionado ao sistema!")
print(orgaos[0])
print("")

hospital_mais_proximo = encontrar_hospital_mais_proximo(orgaos[0].cep, hospitais)

if hospital_mais_proximo:
    print(f"O hospital mais próximo do órgão é {hospital_mais_proximo.nome}.")
else:
    print("Não foi possível encontrar um hospital próximo.")
