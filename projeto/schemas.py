from pydantic import BaseModel, Field
from typing import Optional, Dict
from uuid import UUID


class DisciplinaBase(BaseModel):
    nome: str = Field(
        ..., 
        title="Nome da Disciplina", 
        description="Nome único que identifica cada matéria",
    )
    professor: Optional[str] = Field(
        None,
        title="Nome do Professor", 
        description="Nome opcional do professor da disciplina",
    )

class DisciplinaCreate(DisciplinaBase):
    pass

class Disciplina(DisciplinaBase):
    class Config:
        orm_mode = True


class AnotacaoBase(BaseModel):
    nota: str = Field(
        ...,
        title="Nota a ser Adicionada"
    )

class AnotacaoCreate(AnotacaoBase):
    pass

class Anotacao(AnotacaoBase):
    id: int
    nome_disciplina: str

    class Config:
        orm_mode = True