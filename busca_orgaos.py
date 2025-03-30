from interface_hospitais import carregar_hospitais

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
                f"Hospitais: {self.hospital}")

# Função para criar os EstadosTransplante a partir dos Hospitais
def criar_estados_transplante(hospitais):
    estados_dict = {}

    for hospital in hospitais:
        estado = hospital.estado
        if estado not in estados_dict:
            estados_dict[estado] = EstadoTransplante(estado, hospital=[])
        estados_dict[estado].hospital.append(hospital)

    return list(estados_dict.values())

# Exemplo de uso
hospitais = carregar_hospitais("hospitais.txt")
estados_transplante = criar_estados_transplante(hospitais)

for estado in estados_transplante:
    print(estado)
