from datetime import datetime
from algoritmos.A_estrela import heuristica_A_estrela
from funcoes.Hospital import cidade_via_cep

import unicodedata
def normalizar(texto):
    return unicodedata.normalize('NFKD', texto).encode('ASCII', 'ignore').decode('ASCII').lower()


class Paciente:
    def __init__(self, nome, data_entrada, idade, cep, orgao_solicitado, tipo_sanguineo, estado_gravidade):
        self.nome = nome

        # Garantir que a data seja convertida para um objeto datetime
        self.data_entrada = datetime.strptime(data_entrada, "%Y-%m-%d") if isinstance(data_entrada, str) else data_entrada

        self.cep = cep
        self.idade = idade
        self.orgao_solicitado = orgao_solicitado
        self.tipo_sanguineo = tipo_sanguineo
        self.estado_gravidade = estado_gravidade

    def __repr__(self):
        return f"Paciente: {self.nome} \nData de entrada: {self.data_entrada.strftime('%d/%m/%Y')} \nIdade: {self.idade} \n"

    def tempo_entrada(self):
        # Calcula o tempo decorrido desde a entrada até o momento atual
        return (datetime.now() - self.data_entrada).days
    
def ordenar_pacientes(pacientes, hospitais, orgao_cidade):
    prioridade_gravidade = {
        "critico": 0,
        "urgente": 1,
        "moderado": 2,
        "estavel": 3
    }

    return sorted(pacientes, key=lambda paciente: (
        prioridade_gravidade.get(normalizar(paciente.estado_gravidade), 4),
        paciente.data_entrada,
        -int(paciente.idade),
        heuristica_A_estrela(cidade_via_cep(hospitais, paciente.cep), orgao_cidade)
    ))

def carregar_pacientes(nome_arquivo):
    pacientes = []

    with open(nome_arquivo, "r", encoding="utf-8") as arquivo:
        for linha in arquivo:
            if linha.strip():  # Ignora linhas vazias
                dados = linha.strip().split(',')
                if len(dados) == 7:  # Corrigido para 7 campos
                    nome, data_entrada, cep, idade, orgao_solicitado, tipo_sanguineo, estado_gravidade = dados
                    paciente_obj = Paciente(
                        nome=nome,
                        data_entrada=data_entrada,
                        idade=int(idade),
                        cep=cep,
                        orgao_solicitado=orgao_solicitado,
                        tipo_sanguineo=tipo_sanguineo,
                        estado_gravidade=estado_gravidade
                    )
                    pacientes.append(paciente_obj)

    return pacientes

# Exemplo de uso - rodável usando [python funcoes/mock_pacientes.py]
if __name__ == "__main__":
    pacientes = carregar_pacientes("dados/mock_pacientes.txt")

    for paciente in pacientes:
        print(paciente)
