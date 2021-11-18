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


# Lista tudo de todas as disciplinas
@router.get(
    "/",
    response_model=List[Disciplina],
    status_code=status.HTTP_202_ACCEPTED,
    summary="Lista tudo de todas as disciplinas",
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
    - **Anotações** (*Opcional*): Um dicionário com as anotações da matéria (O dicionário está construido com o conjunto *ID:Anotação*, onde o ID é constuido usando uuid)
    """
    return crud.create_discipline(db, disciplina=disciplina)

# # Modifica uma Disciplona
# @router.patch(
#     "/{nome_disciplina}", 
#     response_model=Disciplina,
#     response_model_exclude_unset=True,
#     status_code=status.HTTP_200_OK,
#     summary="Modifica uma disciplona",
#     description="Modifica todos os itens de uma disciplina, incluindo nome e professor, se o mesmo existir. (A modificação das anotações é feita por outra chamada)",
#     dependencies= [Depends(verifica_nome)],

# )
# def modifica_tudo(nomeD: str = Depends(nome_disc), disciplina: Disciplina = Depends(disc)):

#     if disciplina.nome:
#         new_nome = disciplina.nome.casefold()
#         fake_db[new_nome] = fake_db.pop(nomeD)
#         fake_db[new_nome]["nome"] = disciplina.nome

#     if disciplina.professor:
#         fake_db[new_nome]["professor"] = disciplina.professor

#     return fake_db[new_nome]

# Deleta uma Disciplina
@router.delete(
    "/{nome_disciplina}",
    summary="Deleta uma disciplina",
    dependencies= [Depends(verifica_nome)],
)
def deleta_disciplina(db: Session = Depends(get_db), nome: str = Depends(nome_disc)):
    crud.delete_discipline(db, nome)