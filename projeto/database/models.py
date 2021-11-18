from sqlalchemy import Column, String, ForeignKey, Integer, Text
from sqlalchemy.orm import relationship

from .database import Base

class Disciplina(Base):
    __tablename__ = "disciplinas"

    nome = Column(String(40), primary_key=True, unique=True, index=True)
    professor = Column(String(40))

    notas = relationship("Anotacao", back_populates="dosciplina_dona")

class Anotacao(Base):
    __tablename__ = "notas"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    nota = Column(Text, nullable=False)

    nome_disciplina = Column(String(40), ForeignKey("disciplinas.nome"), nullable=False)

    dosciplina_dona = relationship("Disciplina", back_populates="notas")
