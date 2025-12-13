
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Enum
from sqlalchemy.orm import relationship, declarative_base
import enum

Base = declarative_base()

# Enum para controle de status (State Pattern)
class StatusOS(enum.Enum):
    ABERTA = "Aberta"
    EM_EXECUCAO = "Em Execução"
    FINALIZADA = "Finalizada"

class Cliente(Base):
    __tablename__ = "clientes"
    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    telefone = Column(String, nullable=False)
    veiculos = relationship("Veiculo", back_populates="cliente")

class Veiculo(Base):
    __tablename__ = "veiculos"
    id = Column(Integer, primary_key=True)
    modelo = Column(String, nullable=False)
    placa = Column(String, nullable=False)
    cliente_id = Column(Integer, ForeignKey("clientes.id"))
    cliente = relationship("Cliente", back_populates="veiculos")
    ordens = relationship("OrdemServico", back_populates="veiculo")

class OrdemServico(Base):
    __tablename__ = "ordens_servico"
    id = Column(Integer, primary_key=True)
    descricao = Column(String, nullable=False)
    valor_estimado = Column(Float, nullable=False)
    valor_final = Column(Float, nullable=True)
    status = Column(Enum(StatusOS), default=StatusOS.ABERTA)
    veiculo_id = Column(Integer, ForeignKey("veiculos.id"))
    veiculo = relationship("Veiculo", back_populates="ordens")
    historico = relationship("HistoricoStatus", back_populates="ordem")

class HistoricoStatus(Base):
    __tablename__ = "historico_status"
    id = Column(Integer, primary_key=True)
    ordem_id = Column(Integer, ForeignKey("ordens_servico.id"))
    mensagem = Column(String, nullable=False)
    ordem = relationship("OrdemServico", back_populates="historico")
