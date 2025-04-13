import requests
import time
from interface_hospitais import *

API_KEY = '38b6c76dc3d046038db52fdbd9e18f95'  # OpenCage

def limpar_cep(cep):
    return ''.join(filter(str.isdigit, cep))

def get_coordinates_from_cep(cep):
    time.sleep(0.8)  # Para não estourar o limite da API
    
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

# Lista de CEPs
"""
ceps = []
hospitais = carregar_hospitais("hospitais.txt")
for hospital in hospitais:
    ceps.append(hospital.cep)



# Coletar todas as coordenadas
coordenadas = []
for idx, cep in enumerate(ceps):
    lat, lon = get_coordinates_from_cep(cep)
    if lat and lon:
        print(f"{lat}, {lon}")
        coordenadas.append((lat, lon))
    else:
        print(f"[{idx}] Não foi possível obter coordenadas para o CEP {cep}")
        
"""
