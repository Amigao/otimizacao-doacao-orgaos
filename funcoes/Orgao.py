from datetime import datetime

VELOCIDADE_MEDIA = 80  # Velocidade média de transporte (km/h)

class Orgao:
    def __init__(self, nome, cep, tempo_isquemia):
        self.nome = nome

        self.cep = cep

        self.tempo_isquemia = tempo_isquemia

    def __repr__(self):
        return f"Órgão: {self.nome} \nTempo de isquemia: {self.tempo_isquemia} horas \n"

def calcular_tempo_compatibilidade(orgao, distancia):
    return (float(distancia) / VELOCIDADE_MEDIA) <= float(orgao.tempo_isquemia)

def carregar_orgaos(nome_arquivo):

    orgaos = []

    with open(nome_arquivo, "r", encoding="utf-8") as arquivo:
        for linha in arquivo:
            if linha.strip():  # Ignora linhas vazias
                dados = linha.strip().split(',')
                if len(dados) == 3:
                    nome, cep, tempo_isquemia = dados
                    orgao = Orgao(nome=nome, cep=cep, tempo_isquemia=tempo_isquemia)
                    orgaos.append(orgao)

    return orgaos

# Exemplo de uso - rodável usando [python funcoes/Orgao.py]
if __name__ == "__main__":
    orgaos = carregar_orgaos("dados/orgaos.txt")

    for orgao in orgaos:
        print(orgao)