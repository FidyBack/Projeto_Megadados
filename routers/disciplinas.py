from fastapi import APIRouter, status, Depends
from fastapi.param_functions import Body

from ..dependencies import verifica_nome, verifica_diciplina, nome_disc, disc
from ..schemas import Disciplina
from ..database import fake_db


router = APIRouter(
    prefix="/disciplinas",
    tags=["Disciplinas"]
)


# Lista tudo de todas as disciplinas
@router.get(
    "/", 
    status_code=status.HTTP_202_ACCEPTED,
    summary="Lista tudo de todas as disciplinas",
    description="Retorna um dicionário com todas as disciplimas disponíveis e todas as informações presentes nelas",
    deprecated=True,
)
def ler_tudo():
    return fake_db

# Lista tudo de uma disciplina
@router.get(
    "/{nome_disciplina}", 
    response_model=Disciplina, 
    response_model_exclude_unset=True, 
    status_code=status.HTTP_202_ACCEPTED, 
    tags=["Disciplinas"],
    summary="Lista tudo de uma disciplina",
    dependencies= [Depends(verifica_nome)],
)
def ler_disciplinas(nome: str = Depends(nome_disc)):
    return fake_db[nome]

# Lista o nome das disciplinas
@router.get(
    "/nomes/", 
    status_code=status.HTTP_202_ACCEPTED, 
    summary="Lista o nome das disciplinas",
)
def ler_nomes():
    todos_nomes = []
    for i in fake_db.values():
        todos_nomes.append(i["nome"])
    return todos_nomes

# Cria uma Disciplina
@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    summary="Cria uma disciplina",
    dependencies=[Depends(verifica_diciplina)]
)
def cria_disciplina(disciplina: Disciplina = Depends(disc)):
    """
    Cria uma disciplina com todas as informações necessárias, tais como:

    - **Nome**: Nome da disciplina que será criada
    - **Professor** (*Opcional*): Nome do professor que leciona a disciplina
    - **Anotações** (*Opcional*): Um dicionário com as anotações da matéria (O dicionário está construido com o conjunto *ID:Anotação*, onde o ID é constuido usando uuid)
    """
    nome = disciplina.nome.casefold()
    new_data = disciplina.dict(exclude_unset=True)
    new_dict = {nome: new_data}
    fake_db.update(new_dict)
    return new_dict

# Modifica uma Disciplona
@router.patch(
    "/{nome_disciplina}", 
    response_model=Disciplina,
    response_model_exclude_unset=True,
    status_code=status.HTTP_200_OK,
    summary="Modifica uma disciplona",
    description="Modifica todos os itens de uma disciplina, incluindo nome e professor, se o mesmo existir. (A modificação das anotações é feita por outra chamada)",
    dependencies= [Depends(verifica_nome)],

)
def modifica_tudo(nomeD: str = Depends(nome_disc), disciplina: Disciplina = Body(..., example={ "nome": "Foo", "professor": "Bar"})):

    if disciplina.nome:
        new_nome = disciplina.nome.casefold()
        fake_db[new_nome] = fake_db.pop(nomeD)
        fake_db[new_nome]["nome"] = disciplina.nome

    if disciplina.professor:
        fake_db[new_nome]["professor"] = disciplina.professor

    return fake_db[new_nome]

# Deleta uma Disciplina
@router.delete(
    "/{nome_disciplina}",
    summary="Deleta uma disciplina",
    dependencies= [Depends(verifica_nome)],
)
def deleta_disciplina(nome: str = Depends(nome_disc)):
    fake_db.pop(nome)