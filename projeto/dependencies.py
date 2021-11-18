from fastapi import HTTPException, Path, Query, Depends
from fastapi.param_functions import Body
from sqlalchemy.orm import Session

from .database import database, crud, models
from .schemas import Disciplina

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
    return nome_disciplina.casefold()

def disc(
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


# Dependências de Erros
def verifica_nome(db: Session = Depends(get_db), nome: str = Depends(nome_disc)):
    if (crud.get_discipline(db, nome) == None):
        raise HTTPException(status_code=404, detail=f"Disciplina {nome} Inexistente")

def verifica_diciplina(db: Session = Depends(get_db), disciplina: Disciplina = Depends(disc)):
    if (crud.get_discipline(db, disciplina.nome) != None):
        raise HTTPException(status_code=418, detail=f"Disciplina {disciplina.nome} já existe")

# class NotaDisciplinaQuery:
#     def __init__(self, nome_disciplina: str = Depends(nome_disc), id_nota: UUID = Query(..., description="Id da anotação em formato UUID", example="Bar")):
#         self.nome_disciplina = nome_disciplina
#         self.id_nota = str(id_nota)

# class NotaDisciplinaPath:
#     def __init__(self, nome_disciplina: str = Depends(nome_disc), id_nota: UUID = Path(..., description="Id da anotação em formato UUID", example="Bar")):
#         self.nome_disciplina = nome_disciplina
#         self.id_nota = str(id_nota)

# class CommonInfoQ:
#     def __init__(self, nome_disc: NotaDisciplinaQuery = Depends(), nota: str = Query(...,  description="Anotação requerida", example="Baz")):
#         self.nome_disciplina = nome_disc.nome_disciplina
#         self.id_nota = nome_disc.id_nota
#         self.nota = nota

# class CommonInfoP:
#     def __init__(self, disc: NotaDisciplinaPath = Depends(), nota: str = Query(...,  description="Anotação requerida", example="Baz")):
#         self.nome_disciplina = disc.nome_disciplina
#         self.id_nota = disc.id_nota
#         self.nota = nota

# async def verifica_campo_nota(nome: str = Depends(nome_disc)):
#     if "anotacoes" not in fake_db[nome]:
#         raise HTTPException(status_code=404, detail= "Não há anotações nesta disciplina")

# async def verifica_nota_especifica(notaDisc: NotaDisciplinaPath = Depends()):
#     if notaDisc.id_nota not in fake_db[notaDisc.nome_disciplina]["anotacoes"]:
#         raise HTTPException(status_code=404, detail="Anotação Inexistente")