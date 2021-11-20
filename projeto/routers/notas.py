from fastapi import APIRouter, status, Depends

from ..schemas import Anotacao, AnotacaoCreate
from ..dependencies import *

router = APIRouter(
    prefix="/notas",
    tags=["Anotações"],
    dependencies=[Depends(verifica_nome)]
)


# Lista as anotações de uma disciplina
@router.get(
    "/{nome_disciplina}",
    status_code=status.HTTP_202_ACCEPTED,
    summary="Lista as anotações de uma disciplina",
    description="Retorna uma lista com o as anotações de uma disciplina",
    dependencies= [Depends(verifica_campo_nota)],
)
def ler_anotacao(db: Session = Depends(get_db), nome: str = Depends(nome_disc)):
    return crud.get_discipline_notes(db, nome)

# Adiciona uma Nota
@router.put(
    "/{nome_disciplina}",
    response_model=Anotacao,
    status_code=status.HTTP_200_OK,
    summary="Adiciona uma Nota",
    description="Cria uma nova nota dentro da disciplina",
) 
def adiciona_nota(db: Session = Depends(get_db), nome: str = Depends(nome_disc), nota: AnotacaoCreate = Depends()):
    return crud.add_discipline_note(db, nota, nome)

# Modifica uma Nota
@router.patch(
    "/{nome_disciplina}/{id_nota}",
    status_code=status.HTTP_200_OK,
    summary="Modifica uma Nota",
    description="Modifica uma nota existente dentro da disciplina",
    dependencies= [Depends(verifica_campo_nota), Depends(verifica_nota_especifica)],
) 
def modifica_nota(db: Session = Depends(get_db), id: int = Depends(id_anotacao), nota: Anotacao = Depends()):
    return crud.modify_note(db, id, nota)

# Deleta uma Anotação
@router.delete(
    "/{nome_disciplina}/{id_nota}",
    summary="Deleta uma Anotação",
    dependencies= [Depends(verifica_campo_nota), Depends(verifica_nota_especifica)],
)
def deleta_nota(db: Session = Depends(get_db), nome: str = Depends(nome_disc), id: int = Depends(id_anotacao)):
    crud.delete_discipline_note(db, nome, id)