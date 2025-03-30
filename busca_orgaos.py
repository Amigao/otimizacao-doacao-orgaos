from interface_hospitais import carregar_hospitais
from interface_orgaos import Orgao

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

# Função para criar os EstadosTransplante a partir dos Hospitais
def criar_estados_transplante(hospitais):
    estados_dict = {}

    for hospital in hospitais:
        estado = hospital.estado
        if estado not in estados_dict:
            estados_dict[estado] = EstadoTransplante(estado, hospital=[])  # corrigido aqui
        estados_dict[estado].hospital.append(hospital)  # corrigido aqui

    return list(estados_dict.values())

def carregar_orgaos(nome_arquivo, estados_transplante):

    # Cria um dicionário de hospitais com cep como chave para facilitar a busca
    for estado in estados_transplante:
        hospitais_dict = {hospital.cep: hospital for hospital in estado.hospital}

        with open(nome_arquivo, "r", encoding="utf-8") as arquivo:
            for linha in arquivo:
                if linha.strip():  # Ignora linhas vazias
                    # Divide a linha para obter as informações do órgão
                    dados = linha.strip().split(',')
                    if len(dados) == 3:
                        nome, data_captação, hospital_cep = dados
                        # Cria o objeto Orgao
                        orgao = Orgao(nome=nome, data_captação=data_captação)

                        # Verifica se o hospital com o cep existe no dicionário
                        if hospital_cep in hospitais_dict:
                            # Adiciona o órgão ao hospital correspondente
                            hospitais_dict[hospital_cep].orgaos_disponiveis.append(orgao)
                            print(f"Órgão {orgao.nome} adicionado ao hospital {hospitais_dict[hospital_cep].nome} ({hospital_cep}).")

# Exemplo de uso
hospitais = carregar_hospitais("hospitais.txt")
estados_transplante = criar_estados_transplante(hospitais)

# Carregar órgãos para os hospitais de cada estado
carregar_orgaos("mock_orgaos.txt", estados_transplante)

# Exibe os hospitais com seus órgãos disponíveis
for estado in estados_transplante:
    print(estado)
