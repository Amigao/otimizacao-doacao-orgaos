from datetime import datetime

class Orgao:
    def __init__(self, nome, data_captação):
        self.nome = nome
        # Garantir que a data seja convertida para um objeto datetime
        self.data_captação = datetime.strptime(data_captação, "%Y-%m-%d") if isinstance(data_captação, str) else data_captação

    def __repr__(self):
        return f"Órgão(nome: {self.nome}, Data de captação: {self.data_captação.strftime('%d/%m/%Y')})"
    
    def tempo_captação(self):
        # Calcula o tempo decorrido desde a captação até o momento atual
        return (datetime.now() - self.data_captação).days

