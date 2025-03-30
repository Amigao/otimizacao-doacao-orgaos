import re

class LocalizacaoEquipe:
    def __init__(self, estado, cidade, hospitais):
        self.estado = estado
        self.cidade = cidade
        self.hospitais = hospitais  # Lista de tuplas (nome_hospital, cep)

    def __repr__(self):
        hospitais_info = ", ".join([f"{nome} (CEP: {cep})" for nome, cep in self.hospitais])
        return f"LocalizacaoEquipe(Estado: {self.estado}, Cidade: {self.cidade}, Hospitais: {hospitais_info})"


def carregar_hospitais(nome_arquivo):
    localizacoes = {}

    with open(nome_arquivo, "r", encoding="utf-8") as arquivo:
        for linha in arquivo:
            if linha.strip():  # Ignora linhas vazias
                # Usa regex para capturar os dados corretamente
                match = re.match(r"([A-Z]{2}) - (.*?):\s*“(.*?)”\s*- CEP:\s*([\d.-]+)", linha.strip())
                if match:
                    estado, cidade, nome_hospital, cep = match.groups()
                    chave = (estado, cidade)

                    if chave not in localizacoes:
                        localizacoes[chave] = LocalizacaoEquipe(estado, cidade, [])

                    localizacoes[chave].hospitais.append((nome_hospital, cep))

    return list(localizacoes.values())


# Exemplo de uso
hospitais = carregar_hospitais("hospitais.txt")
for hospital in hospitais:
    print(hospital)
