from sqlalchemy import column, Integer, String, DateTime, ForeignKey, Column
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class Cliente(Base):
    __tablename__ = 'clientes'
    id = Column(Integer, primary_key=True)
    nome = Column(String(100), nullable=False)
    telefone = Column(String(20), nullable=False)
    email = Column(String(100), nullable=False)

class Atendimento(Base):
    __tablename__ = 'atendimentos'
    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, ForeignKey('clientes.id'))
    equipamento_id = Column(String(100), nullable=False)
    problema = Column(String(1000), nullable=False)
    status = Column(String(100), nullable=False)
    criado_em = Column(DateTime, default=datetime.now)
    cliente = relationship("Cliente")