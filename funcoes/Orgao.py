VELOCIDADE_MEDIA = 80  # Velocidade média de transporte (km/h)

class Orgao:
    def __init__(self, nome, tempo_isquemia, tipo_sanguineo=None, cep=None):
        self.nome = nome

        self.cep = cep

        self.tempo_isquemia = tempo_isquemia
        
        self.tipo_sanguineo = tipo_sanguineo

    def __repr__(self):
        return f"Órgão: {self.nome} \nTempo de isquemia: {self.tempo_isquemia} horas \n"

def calcular_tempo_compatibilidade(orgao, distancia):
    print(f"Tempo: {distancia/VELOCIDADE_MEDIA} horas. Tempo de isquemia: {orgao.tempo_isquemia} horas")
    return (float(distancia) / VELOCIDADE_MEDIA) <= float(orgao.tempo_isquemia)

def carregar_orgaos(nome_arquivo):

    orgaos = []

    with open(nome_arquivo, "r", encoding="utf-8") as arquivo:
        for linha in arquivo:
            if linha.strip():  # Ignora linhas vazias
                dados = linha.strip().split(',')
                if len(dados) == 4:
                    nome, cep, tempo_isquemia, tipo_sanguineo = dados
                    orgao = Orgao(nome=nome, cep=cep, tempo_isquemia=tempo_isquemia, tipo_sanguineo=tipo_sanguineo)
                    orgaos.append(orgao)

    return orgaos

# Exemplo de uso - rodável usando [python funcoes/Orgao.py]
if __name__ == "__main__":
    orgaos = carregar_orgaos("dados/orgaos.txt")

    for orgao in orgaos:
        print(orgao)