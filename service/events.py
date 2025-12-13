
class DomainEvent:
    def __init__(self, nome, dados):
        self.nome = nome
        self.dados = dados

class EventLog:
    def __init__(self):
        self.eventos = []

    def registrar(self, evento: DomainEvent):
        self.eventos.append(evento)
        print(f"[EVENTO] {evento.nome}: {evento.dados}")
