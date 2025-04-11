from datetime import datetime

class Orgao:
    def __init__(self, nome, data_captação, cep, tempo_isquemia):
        self.nome = nome

        # Garantir que a data seja convertida para um objeto datetime
        self.data_captação = datetime.strptime(data_captação, "%Y-%m-%d") if isinstance(data_captação, str) else data_captação

        self.cep = cep

        self.tempo_isquemia = tempo_isquemia

    def __repr__(self):
        return f"Órgão: {self.nome} \nData de captação: {self.data_captação.strftime('%d/%m/%Y')}) \nTempo de isquemia: {self.tempo_isquemia} horas"
    
    def tempo_captação(self):
        # Calcula o tempo decorrido desde a captação até o momento atual
        return (datetime.now() - self.data_captação).days

def carregar_orgaos(nome_arquivo):

    orgaos = []

    with open(nome_arquivo, "r", encoding="utf-8") as arquivo:
        for linha in arquivo:
            if linha.strip():  # Ignora linhas vazias
                dados = linha.strip().split(',')
                if len(dados) == 4:
                    nome, data_captação, cep, tempo_isquemia = dados
                    orgao = Orgao(nome=nome, data_captação=data_captação, cep=cep, tempo_isquemia=tempo_isquemia)
                    orgaos.append(orgao)

    return orgaos
