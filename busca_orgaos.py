from interface_hospitais import carregar_hospitais

class EstadoTransplante:
    def __init__(self, estado, orgaos_disponiveis=None, pacientes_aguardando=None, pacientes_alocados=None, localizacoes_equipes=None, tempo_decorrido=0):
        self.estado = estado
        self.orgaos_disponiveis = orgaos_disponiveis or []
        self.pacientes_aguardando = pacientes_aguardando or []
        self.pacientes_alocados = pacientes_alocados or []
        self.localizacoes_equipes = localizacoes_equipes or []
        self.tempo_decorrido = tempo_decorrido

    def __repr__(self):
        return (f"EstadoTransplante(Estado: {self.estado}, "
                f"Órgãos: {self.orgaos_disponiveis}, "
                f"Pacientes aguardando: {self.pacientes_aguardando}, "
                f"Pacientes alocados: {self.pacientes_alocados}, "
                f"Localizações equipes: {self.localizacoes_equipes}, "
                f"Tempo: {self.tempo_decorrido}s)")

# Função para criar os EstadosTransplante a partir das localizações das equipes
def criar_estados_transplante(hospitais):
    estados_dict = {}

    for hospital in hospitais:
        estado = hospital.estado
        if estado not in estados_dict:
            estados_dict[estado] = EstadoTransplante(estado, localizacoes_equipes=[])
        estados_dict[estado].localizacoes_equipes.append(hospital)

    return list(estados_dict.values())

# Exemplo de uso
hospitais = carregar_hospitais("hospitais.txt")
estados_transplante = criar_estados_transplante(hospitais)

for estado in estados_transplante:
    print(estado)
