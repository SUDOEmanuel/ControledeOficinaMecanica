
from model.models import OrdemServico, HistoricoStatus, StatusOS
from service.events import DomainEvent

class UnitOfWork:
    def __init__(self, session, event_log):
        self.session = session
        self.event_log = event_log

    def alterar_status(self, ordem: OrdemServico, novo_status: StatusOS):
        # Regra: não permitir finalizar sem valor_final
        if novo_status == StatusOS.FINALIZADA and ordem.valor_final is None:
            raise ValueError("Não é possível finalizar sem valor final.")

        # Atualiza status
        ordem.status = novo_status

        # Registra histórico
        historico = HistoricoStatus(ordem=ordem, mensagem=f"Status alterado para {novo_status.value}")
        self.session.add(historico)

        # Dispara eventos de domínio
        evento = DomainEvent("StatusAlterado", {"ordem_id": ordem.id, "status": novo_status.value})
        self.event_log.registrar(evento)

        if novo_status == StatusOS.FINALIZADA:
            evento_finalizada = DomainEvent("OSFinalizada", {"ordem_id": ordem.id})
            self.event_log.registrar(evento_finalizada)

        # Commit transacional
        self.session.commit()
