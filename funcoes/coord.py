# Funções pra lidar com coordenadas

import requests
import time
from math import radians, sin, cos, sqrt, atan2

try:
    from Hospital import carregar_hospitais
except ModuleNotFoundError:
    from funcoes.Hospital import carregar_hospitais

API_KEY = '38b6c76dc3d046038db52fdbd9e18f95'  # OpenCage

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

def distancia_coordenadas(lat1, lon1, lat2, lon2):
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

def limpar_cep(cep):
    return ''.join(filter(str.isdigit, cep))

def get_coordinates_from_cep(cep):
    # Usa a API da ViaCEP pra pegar as coordenadas

    time.sleep(0.6)  # Para não estourar o limite da API
    
    cep = limpar_cep(cep)

    # Requisição na API ViaCEP
    url = f"https://viacep.com.br/ws/{cep}/json/"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        if 'erro' in data:
            return None, None

        # Monta a string de localização com os dados disponíveis
        components = [data.get(k) for k in ['logradouro', 'bairro', 'localidade', 'uf'] if data.get(k)]
        localizacao = ', '.join(components)

        # Consulta a API de geocodificação
        geocode_url = f"https://api.opencagedata.com/geocode/v1/json?q={localizacao}&key={API_KEY}&language=pt&countrycode=br"
        geocode_response = requests.get(geocode_url)
        if geocode_response.status_code == 200:
            geocode_data = geocode_response.json()
            if geocode_data['results']:
                lat = geocode_data['results'][0]['geometry']['lat']
                lon = geocode_data['results'][0]['geometry']['lng']
                return lat, lon
    return None, None

# Exemplo de uso - rodável usando [python funcoes/coord.py]
# Retorna as coordenadas de cada hospital no arquivo de hospitais
if __name__ == "__main__":
    hospitais = carregar_hospitais("dados/hospitais.txt")

    # Coletar todas as coordenadas
    coordenadas = []
    for hospital in hospitais:
        cep_h = hospital.cep
        lat, lon = get_coordinates_from_cep(cep_h)

        if lat and lon:
            print(hospital)
            print(f"{lat}, {lon}\n")
            coordenadas.append((lat, lon))

        else:
            print(f"Não foi possível obter coordenadas para o CEP {hospital.cep}")