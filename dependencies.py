from fastapi import HTTPException, Path, Query, Depends
from fastapi.param_functions import Body
from uuid import UUID, uuid4

from .database import fake_db
from .schemas import Disciplina


def nome_disc(nome_disciplina: str = Path(..., description="O nome da disciplina desejada", example="Foo")):
    return nome_disciplina.casefold()

class NotaDisciplinaQuery:
    def __init__(self, nome_disciplina: str = Depends(nome_disc), id_nota: UUID = Query(..., description="Id da anotação em formato UUID", example="Bar")):
        self.nome_disciplina = nome_disciplina
        self.id_nota = str(id_nota)

class NotaDisciplinaPath:
    def __init__(self, nome_disciplina: str = Depends(nome_disc), id_nota: UUID = Path(..., description="Id da anotação em formato UUID", example="Bar")):
        self.nome_disciplina = nome_disciplina
        self.id_nota = str(id_nota)

class CommonInfoQ:
    def __init__(self, nome_disc: NotaDisciplinaQuery = Depends(), nota: str = Query(...,  description="Anotação requerida", example="Baz")):
        self.nome_disciplina = nome_disc.nome_disciplina
        self.id_nota = nome_disc.id_nota
        self.nota = nota

class CommonInfoP:
    def __init__(self, disc: NotaDisciplinaPath = Depends(), nota: str = Query(...,  description="Anotação requerida", example="Baz")):
        self.nome_disciplina = disc.nome_disciplina
        self.id_nota = disc.id_nota
        self.nota = nota


async def verifica_nome(nome: str = Depends(nome_disc)):
    if nome not in fake_db:
        raise HTTPException(status_code=404, detail=f"Disciplina {nome} Inexistente")

async def verifica_campo_nota(nome: str = Depends(nome_disc)):
    if "anotacoes" not in fake_db[nome]:
        raise HTTPException(status_code=404, detail= "Não há anotações nesta disciplina")

async def verifica_nota_especifica(notaDisc: NotaDisciplinaPath = Depends()):
    if notaDisc.id_nota not in fake_db[notaDisc.nome_disciplina]["anotacoes"]:
        raise HTTPException(status_code=404, detail="Anotação Inexistente")

def disc(
    disciplina: Disciplina = Body(
        ..., 
        description="Corpo da criação da disciplina",
        examples={
            "criacao_completo": {
                "summary": "Criação - Exemplo Completo",
                "description": "Um exemplo com todos os elementos.",
                "value": {
                    "nome": "Foo",
                    "professor": "Bar",
                    "anotacoes": {uuid4(): "Uma bela anotação", uuid4(): "Pode ter mais de uma"}
                }
            },
            "criacao_parcial": {
                "summary": "Criação - Exemplo Parcial",
                "description": "Um exemplo com alguns elementos opcionais.",
                "value": {
                    "nome": "Foo",
                    "anotacoes": {"uuid_1": "Uma bela anotação", uuid4(): "Pode ter mais de uma"}
                }
            },
            "criacao_minimo": {
                "summary": "Criação - Exemplo Mínimo",
                "description": "Um exemplo com apenas os elementos obrigatórios.",
                "value": {
                    "nome": "Foo"
                }
            },
            "modificacao_minimo": {
                "summary": "Modificação - Exemplo Mínimo",
                "description": "Um exemplo com apenas os elementos obrigatórios.",
                "value": {
                    "nome": "Foo"
                }
            },
            "modificacao_completo": {
                "summary": "Modificação - Exemplo Completo",
                "description": "Um exemplo com todos os elementos.",
                "value": {
                    "nome": "Foo", 
                    "professor": "Bar"
                }
            }
        }
    )
):
    return disciplina

async def verifica_diciplina(disciplina: Disciplina = Depends(disc)):
    if disciplina.nome.casefold() in fake_db:
        raise HTTPException(status_code=418, detail="Disciplina já existe")