from fastapi import APIRouter, status, Depends

from ..dependencies import *
from ..schemas import Disciplina
from ..database import database


router = APIRouter(
    prefix="/notas",
    tags=["Anotações"],
    # dependencies=[Depends(verifica_nome)]
)


# # Lista as anotações de uma disciplina
# @router.get(
#     "/{nome_disciplina}", 
#     status_code=status.HTTP_202_ACCEPTED,
#     summary="Lista as anotações de uma disciplina",
#     description="Retorna uma lista com o as anotações de uma disciplina",
#     dependencies= [Depends(verifica_campo_nota)],
# )
# def ler_anotacao(nome: str = Depends(nome_disc)):
#     notas = fake_db[nome]["anotacoes"]
#     return list(notas.values())

# # Adiciona uma Nota
# @router.put(
#     "/{nome_disciplina}", 
#     response_model=Disciplina,
#     response_model_exclude_unset=True,
#     status_code=status.HTTP_200_OK,
#     summary="Adiciona uma Nota",
#     description="Cria uma nova nota dentro da disciplina",
# ) 
# def adiciona_nota(commons: CommonInfoQ = Depends()):
#     nome = commons.nome_disciplina

#     if "anotacoes" not in fake_db[nome]:
#         fake_db[nome].update({"anotacoes": {}})

#     fake_db[nome]["anotacoes"].update({commons.id_nota: commons.nota})
#     return fake_db[nome]

# # Modifica uma Nota
# @router.patch(
#     "/{nome_disciplina}/{id_nota}", 
#     response_model=Disciplina, 
#     response_model_exclude_unset=True, 
#     status_code=status.HTTP_200_OK,
#     summary="Modifica uma Nota",
#     description="Modifica uma nota existente dentro da disciplina",
#     dependencies= [Depends(verifica_campo_nota), Depends(verifica_nota_especifica)],
# ) 
# def modifica_nota(commons: CommonInfoP = Depends()):
#     nome = commons.nome_disciplina
#     id_nota = commons.id_nota
#     fake_db[nome]["anotacoes"].update({id_nota: commons.nota})

#     return fake_db[nome]

# # Deleta uma Anotação
# @router.delete(
#     "/{nome_disciplina}/{id_nota}", 
#     response_model=Disciplina,
#     summary="Deleta uma Anotação",
#     dependencies= [Depends(verifica_campo_nota), Depends(verifica_nota_especifica)],
# )
# def deleta_nota(commons: NotaDisciplinaQuery = Depends()):
#     nome = commons.nome_disciplina
#     id_nota = commons.id_nota

#     fake_db[nome]["anotacoes"].pop(id_nota)
#     return fake_db[nome]