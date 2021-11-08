from pydantic import BaseModel, Field
from uuid import UUID, uuid4
from typing import Dict, Optional


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

bd = {
    "matemática": {"nome": "Matemática", "professor": "Angélica", "anotacoes": 
        {uuid4(): "Muito Legal!", uuid4(): "Gosto Muito", uuid4(): "Trabalhar Nisso"}
    },
    "química": {"nome": "Química", "professor": "Fê", "anotacoes": {uuid4(): "Meh"}},
    "português": {"nome": "Português", "professor": "Arnaldo"},
    "ingles": {"nome": "Ingles"} 
}



notas = bd["matemática"]["anotacoes"].keys()
# todas_notas = []
# for i in notas:
#     todas_notas.append(list(i.values())[0])




print(notas)