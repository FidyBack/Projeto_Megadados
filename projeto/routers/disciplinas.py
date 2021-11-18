from fastapi import APIRouter, status, Depends
from fastapi.param_functions import Body
from sqlalchemy.orm import Session
from typing import List

# from ..dependencies import , , , 
from ..dependencies import get_db, nome_disc, verifica_nome, verifica_diciplina, disc
from ..schemas import Disciplina
from ..database import crud, models

router = APIRouter(
    prefix="/disciplinas",
    tags=["Disciplinas"]
)


# Lista todas as disciplinas
@router.get(
    "/",
    response_model=List[Disciplina],
    status_code=status.HTTP_202_ACCEPTED,
    summary="Lista todas as disciplinas",
    description="Retorna um dicionário com todas as disciplimas disponíveis e todas as informações presentes nelas",
    deprecated=True,
)
def ler_tudo(db: Session = Depends(get_db)):
    return crud.get_all_discipline(db)

# Lista tudo de uma disciplina
@router.get(
    "/{nome_disciplina}", 
    response_model=Disciplina,
    status_code=status.HTTP_202_ACCEPTED,
    summary="Lista tudo de uma disciplina",
    dependencies=[Depends(verifica_nome)],
)
def ler_disciplinas(db: Session = Depends(get_db), nome: str = Depends(nome_disc)):
    return crud.get_discipline(db, nome = nome)

# Lista o nome das disciplinas
@router.get(
    "/nomes/", 
    status_code=status.HTTP_202_ACCEPTED, 
    summary="Lista o nome das disciplinas",
)
def ler_nomes(db: Session = Depends(get_db)):
    return crud.get_all_discipline_names(db)

# Cria uma Disciplina
@router.post(
    "/",
    response_model=Disciplina, 
    status_code=status.HTTP_201_CREATED,
    summary="Cria uma disciplina",
    dependencies=[Depends(verifica_diciplina)]
)
def cria_disciplina(db: Session = Depends(get_db), disciplina: Disciplina = Depends(disc)):
    """
    Cria uma disciplina com todas as informações necessárias, tais como:

    - **Nome**: Nome da disciplina que será criada
    - **Professor** (*Opcional*): Nome do professor que leciona a disciplina
    """
    return crud.create_discipline(db, disciplina=disciplina)

# Modifica uma Disciplina
@router.patch(
    "/{nome_disciplina}", 
    # response_model=Disciplina,
    status_code=status.HTTP_200_OK,
    summary="Modifica uma disciplina",
    description="Modifica todos os itens de uma disciplina, incluindo nome e professor, se o mesmo existir. (A modificação das anotações é feita por outra chamada)",
    dependencies= [Depends(verifica_nome), Depends(verifica_diciplina)],

)
def modifica_tudo(db: Session = Depends(get_db), nome: str = Depends(nome_disc), disciplina: Disciplina = Depends(disc)):
    return crud.modify_discipline(db, nome, disciplina=disciplina)

# Deleta uma Disciplina
@router.delete(
    "/{nome_disciplina}",
    summary="Deleta uma disciplina",
    dependencies= [Depends(verifica_nome)],
)
def deleta_disciplina(db: Session = Depends(get_db), nome: str = Depends(nome_disc)):
    crud.delete_discipline(db, nome)