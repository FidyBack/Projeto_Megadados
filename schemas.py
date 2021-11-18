from pydantic import BaseModel, Field
from typing import Optional, Dict
from uuid import UUID

class Disciplina(BaseModel):
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
    anotacoes: Optional[Dict[UUID, str]] = Field(
        None,
        title="Lista de Anotações", 
        description="Lista com todas as notas criadas, em formato de dicionário com UUID: Nota. É opcional",
    )