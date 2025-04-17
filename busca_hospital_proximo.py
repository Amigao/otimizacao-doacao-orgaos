from funcoes.Hospital import carregar_hospitais
from funcoes.Orgao import carregar_orgaos

from funcoes.coord import distancia_coordenadas, get_coordinates_from_cep

# Não utilizada (por enquanto?)
'''
class Demanda:
    def __init__(self, pacientes_aguardando=None, fila_prioridade=None):
        self.pacientes_aguardando = pacientes_aguardando or []
        self.fila_prioridade = fila_prioridade or []

    def __repr__(self):
        return (f"Pacientes aguardando: {self.pacientes_aguardando}")
'''

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
            distancia = distancia_coordenadas(paciente_lat, paciente_lon, hospital_lat, hospital_lon)
            print(f"Distância: {distancia} km.")  # Debug: Exibe a distância
            print("")
            
            if distancia < menor_distancia:
                menor_distancia = distancia
                hospital_mais_proximo = hospital

    return hospital_mais_proximo

# Exemplo de uso - rodável usando [python busca_hospital.py]
# Encontra o hospital mais próximo do primeiro órgão da lista
if __name__ == "__main__":
    hospitais = carregar_hospitais("dados/hospitais.txt")
    orgaos = carregar_orgaos("dados/mock_orgaos.txt")

    print("Órgão adicionado ao sistema!")
    print(orgaos[0], "\n")

    hospital_mais_proximo = encontrar_hospital_mais_proximo(orgaos[0].cep, hospitais)

    if hospital_mais_proximo:
        print(f"O hospital mais próximo do órgão é {hospital_mais_proximo.nome}.")
    else:
        print("Não foi possível encontrar um hospital próximo.")
