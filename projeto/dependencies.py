from fastapi import HTTPException, Path, Query, Depends
from fastapi.param_functions import Body
from sqlalchemy.orm import Session

from .database import database, crud, models
from .schemas import Disciplina, DisciplinaCreate

models.Base.metadata.create_all(bind= database.engine)

# Database
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Dependências Básicas
def nome_disc(nome_disciplina: str = Path(..., description="O nome da disciplina desejada", example="Foo")):
    return nome_disciplina

def id_anotacao(id_nota: int = Path(..., description="Id da anotação", example="1")):
    return id_nota

def disc_norm(
    disciplina: Disciplina = Body(
        ..., 
        description="Corpo da criação da disciplina",
        examples={
            "completo": {
                "summary": "Exemplo Completo",
                "description": "Um exemplo com todos os elementos.",
                "value": {
                    "nome": "Foo",
                    "professor": "Bar",
                }
            },
            "minimo": {
                "summary": "Exemplo Mínimo",
                "description": "Um exemplo com apenas os elementos obrigatórios.",
                "value": {
                    "nome": "Foo"
                }
            },
        }
    )
):
    return disciplina

def create_disc(
    disciplina: DisciplinaCreate = Body(
        ..., 
        description="Corpo da criação da disciplina",
        examples={
            "completo": {
                "summary": "Exemplo Completo",
                "description": "Um exemplo com todos os elementos.",
                "value": {
                    "nome": "Foo",
                    "professor": "Bar",
                }
            },
            "minimo": {
                "summary": "Exemplo Mínimo",
                "description": "Um exemplo com apenas os elementos obrigatórios.",
                "value": {
                    "nome": "Foo"
                }
            },
        }
    )
):
    return disciplina


# Dependências de Erros
def verifica_nome(nome_disciplina: str, db: Session = Depends(get_db)):
    if (crud.get_discipline(db, nome_disciplina) == None):
        raise HTTPException(status_code=404, detail=f"Disciplina {nome_disciplina} Inexistente")

def verifica_diciplina(db: Session = Depends(get_db), disciplina: Disciplina = Depends(disc_norm)):
    if (crud.get_discipline(db, disciplina.nome) != None):
        raise HTTPException(status_code=418, detail=f"Disciplina {disciplina.nome} já existe")

def verifica_campo_nota(nome_disciplina: str, db: Session = Depends(get_db)):
    if (crud.get_discipline_notes(db, nome_disciplina) == []):
        raise HTTPException(status_code=404, detail= "Não há anotações nesta disciplina")

async def verifica_nota_especifica(nome_disciplina: str,  id_nota: int, db: Session = Depends(get_db)):
    if (crud.get_one_note(db, nome_disciplina, id_nota) == None):
        raise HTTPException(status_code=404, detail="Anotação Inexistente")