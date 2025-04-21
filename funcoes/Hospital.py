class Hospital:
    def __init__(self, estado, cidade, nome, cep):
        self.estado = estado
        self.cidade = cidade
        self.nome = nome
        self.cep = cep  

    def __repr__(self):
        return f"{self.nome}, ({self.cidade}-{self.estado})" 
        # Orgaos: {self.orgaos_disponiveis})"

def carregar_hospitais(nome_arquivo):
    localizacoes = []

    with open(nome_arquivo, "r", encoding="utf-8") as arquivo:
        for linha in arquivo:
            if linha.strip():  # Ignora linhas vazias
                # Usa regex para capturar os dados corretamente
                estado, cidade, nome_hospital, cep = linha.strip().split(",")

                # Cria o objeto Hospital com as informações
                hospital = Hospital(estado, cidade, nome_hospital, cep)

                # Adiciona o hospital à lista de localizações
                localizacoes.append(hospital)

    return localizacoes

def cidade_via_cep(hospitais, cep):
    for hospital in hospitais:
        if hospital.cep == cep:
            return hospital.cidade

def cep_via_cidade(hospitais, cidade):
    for hospital in hospitais:
        if hospital.cidade == cidade:
            return hospital.cep

# Exemplo de uso - rodável usando [python funcoes/Hospital.py]
if __name__ == "__main__":
    hospitais = carregar_hospitais("dados/hospitais.txt")

    for hospital in hospitais:
        print(hospital)
