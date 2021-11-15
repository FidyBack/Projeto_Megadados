from fastapi import FastAPI, Query, Path, status, HTTPException
from fastapi.responses import PlainTextResponse
from fastapi.param_functions import Body

from starlette.exceptions import HTTPException as StarletteHTTPException
from pydantic import BaseModel, Field
from typing import Dict, Optional
from uuid import UUID, uuid4

app = FastAPI()


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


fake_db = {
    "matematica": {"nome": "Matemática", "professor": "Angélica", "anotacoes": 
        {uuid4(): "Muito Legal!", uuid4(): "Gosto Muito", uuid4(): "Trabalhar Nisso"}
    },
    "quimica": {"nome": "Química", "professor": "Fê", "anotacoes": {uuid4(): "Meh"}},
    "portugues": {"nome": "Português", "professor": "Arnaldo"},
    "ingles": {"nome": "Ingles"} 
}


#===================================#
#               ERROS               #
#===================================#

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    return PlainTextResponse(str(exc.detail), status_code=exc.status_code)


#===================================#
#               GETS                #
#===================================#

# Lista tudo de todas as disciplinas
@app.get(
    "/disciplinas/", 
    status_code=status.HTTP_202_ACCEPTED, 
    tags=["Disciplinas"],
    summary="Devolve as Disciplinas",
    description="Retorna um dicionário com todas as disciplimas disponíveis e todas as informações presentes nelas",
)
def ler_tudo():
    return fake_db

# Lista tudo de uma disciplina
@app.get(
    "/disciplinas/{nome_disciplina}", 
    response_model=Disciplina, 
    response_model_exclude_unset=True, 
    status_code=status.HTTP_202_ACCEPTED, 
    tags=["Disciplinas"],
    summary="Devolve uma Disciplina",
    description="Retorna todas as informações de uma disciplina em específico",
)
def ler_disciplinas(
    nome_disciplina: str = Path(..., description="O nome da disciplina desejada", example="Foo")
):
    nome = nome_disciplina.casefold()
    if nome not in fake_db:
        raise HTTPException(status_code=404, detail="Disciplina Inexistente")
    return fake_db[nome]

# Lista o nome das disciplinas
@app.get(
    "/disciplinas/nomes/", 
    status_code=status.HTTP_202_ACCEPTED, 
    tags=["Disciplinas"],
    summary="Devolve o nome das Disciplinas",
    description="Retorna uma lista com o nome de todas as disciplinas",
)
def ler_nomes():
    todos_nomes = []
    for i in fake_db.values():
        todos_nomes.append(i["nome"])
    return todos_nomes

# Lista as anotações de uma disciplina
@app.get(
    "/disciplinas/{anotacao_disciplina}/notas/", 
    status_code=status.HTTP_202_ACCEPTED, 
    tags=["Anotações"],
    summary="Devolve as Anotações",
    description="Retorna uma lista com o as anotações de uma disciplina",
)
def ler_anotacao(
    anotacao_disciplina: str = Path(..., description="Nome da disciplina contendo as anotações desejadas", example="Foo")
):
    nome = anotacao_disciplina.casefold()
    if nome not in fake_db:
        raise HTTPException(status_code=404, detail="Disciplina Inexistente")

    if "anotacoes" not in fake_db[nome]:
        return "Não há anotações nesta disciplina."
    
    notas = fake_db[nome]["anotacoes"]
    return list(notas.values())


#=======================================#
#           POSTS/PUTS/PATCHS           #
#=======================================#

# Cria disciplina
@app.post(
    "/disciplinas/", 
    response_model=Disciplina, 
    response_model_exclude_unset=True, 
    status_code=status.HTTP_201_CREATED, 
    tags=["Disciplinas"],
    summary="Cria uma Disciplina",
)
def cria_disciplina(
    disciplina: Disciplina = Body(
        ..., 
        description="Corpo da criação da disciplina",
        examples={
            "completo": {
                "summary": "Exemplo completo",
                "description": "Um exemplo com todos os elementos.",
                "value": {
                    "nome": "Foo",
                    "professor": "Bar",
                    "anotacoes": {uuid4(): "Uma bela anotação", uuid4(): "Pode ter mais de uma"}
                }
            },
            "incompleto": {
                "summary": "Exemplo incompleto",
                "description": "Um exemplo com elementos faltantes.",
                "value": {
                    "nome": "Baz",
                    "anotacoes": {"uuid_1": "Uma bela anotação", uuid4(): "Pode ter mais de uma"}
                }
            },
            "minimo": {
                "summary": "Exemplo mínimo",
                "description": "Um exemplo com apenas os elementos obrigatórios.",
                "value": {
                    "nome": "Qux"
                }
            }
        }
    )
):
    """
    Cria uma disciplina com todas as informações necessárias, tais como:

    - **Nome**: Nome da disciplina que será criada
    - **Professor** (*Opcional*): Nome do professor que leciona a disciplina
    - **Anotações** (*Opcional*): Um dicionário com as anotações da matéria (O dicionário está construido com o conjunto *ID:Anotação*, onde o ID é constuido usando uuid)
    """
    nome_disciplina = disciplina.nome.casefold()
    if nome_disciplina in fake_db:
        raise HTTPException(status_code=418, detail="Disciplina já existe")
    
    fake_db.update({nome_disciplina: disciplina})
    return disciplina

# Adiciona nota em uma disciplina
@app.put(
    "/disciplinas/{nome_disciplina}/{id_nota}", 
    response_model=Disciplina, 
    response_model_exclude_unset=True, 
    status_code=status.HTTP_200_OK, 
    tags=["Anotações"],
    summary="Adiciona uma Nota",
    description="Cria uma nova nota dentro da disciplina",
) 
def adiciona_nota(
    nome_disciplina: str = Path(..., description="O nome da disciplina que terá uma nota nova", example="Foo"),
    id_nota: UUID = Path(..., description="Id da nota a ser adicionada", example="Bar"),
    nota: str = Query(...,  description="Nota a ser adicionada")
):
    nome = nome_disciplina.casefold()
    if nome not in fake_db:
        raise HTTPException(status_code=404, detail="Disciplina Inexistente")

    if "anotacoes" not in fake_db[nome]:
        fake_db[nome].update({"anotacoes": {}})

    fake_db[nome]["anotacoes"].update({id_nota: nota})

    return fake_db[nome]

# Modifica nota em uma disciplina
@app.patch(
    "/disciplinas/{nome_disciplina}/modifica/{id_nota}", 
    response_model=Disciplina, 
    response_model_exclude_unset=True, 
    status_code=status.HTTP_200_OK, 
    tags=["Anotações"],
    summary="Modifica uma Nota",
    description="Modifica uma nota existente dentro da disciplina",
) 
def modifica_nota(
    nome_disciplina: str = Path(..., description="O nome da disciplina que terá uma nota modificada", example="Foo"),
    id_nota: UUID = Path(..., description="Id da nota a ser modificada", example="Bar"),
    nova_nota: str = Query(...,  description="Nova nota a ser adicionada")
):
    nome = nome_disciplina.casefold()
    if nome not in fake_db:
        raise HTTPException(status_code=404, detail="Disciplina Inexistente")

    if "anotacoes" not in fake_db[nome]:
        raise HTTPException(status_code=404, detail="Não há anotações para essa disciplina")

    if id_nota not in fake_db[nome]["anotacoes"]:
        raise HTTPException(status_code=404, detail="Anotação Inexistente")

    fake_db[nome]["anotacoes"].update({id_nota: nova_nota})

    return fake_db[nome]

# Modifica tudo em uma disciplina
@app.patch(
    "/disciplinas/{nome_disciplina}", 
    response_model=Disciplina, 
    response_model_exclude_unset=True, 
    status_code=status.HTTP_200_OK, 
    tags=["Disciplinas"],
    summary="Modifica uma Disciplona",
    description="Modifica todos os itens de uma disciplina, incluindo nome e professor, se o mesmo existir. (A modificação das anotações é feita por outra chamada)",
)
def modifica_tudo(
    nome_disciplina: str = Path(..., description="O nome da disciplina que terá tudo modificado", example="Foo"),
    disciplina: Disciplina = Body(
        ...,
        example={
            "nome": "Foo",
            "professor": "Bar"
        }
    ),
):
    nomeD = nome_disciplina.casefold()
    if nomeD not in fake_db:
        raise HTTPException(status_code=404, detail="Disciplina Inexistente")

    if disciplina.nome:
        new_nome = disciplina.nome.casefold()
        fake_db[new_nome] = fake_db.pop(nomeD)
        fake_db[new_nome]["nome"] = disciplina.nome

    if disciplina.professor:
        fake_db[new_nome]["professor"] = disciplina.professor

    return fake_db[new_nome]


#===================================#
#               DELETES             #
#===================================#

# Deleta disciplina
@app.delete(
    "/disciplinas/{nome_disciplina}", 
    status_code=status.HTTP_200_OK, 
    tags=["Disciplinas"],
    summary="Deleta uma Disciplina",
)
def deleta_disciplina(
    nome_disciplina: str = Path(..., description="O nome da disciplina a ser deletada", example="Foo")
):
    nome = nome_disciplina.casefold()
    if nome not in fake_db:
        raise HTTPException(status_code=404, detail="Disciplina Inexistente")

    fake_db.pop(nome)

# Deleta nota de uma disciplina
@app.delete(
    "/disciplinas/{nome_disciplina}/{id_nota}", 
    response_model=Disciplina, 
    response_model_exclude_unset=True, 
    status_code=status.HTTP_200_OK, 
    tags=["Anotações"],
    summary="Deleta uma Anotação",
    description="Deleta uma anotação de uma disciplina selecionada",
)
def deleta_nota(
    nome_disciplina: str = Path(..., description="O nome da disciplina a ser deletada", example="Foo"),
    id_nota: UUID = Path(..., description="Id da nota a ser deletada", example="Bar"),
):
    nome = nome_disciplina.casefold()
    if nome not in fake_db:
        raise HTTPException(status_code=404, detail="Disciplina Inexistente")

    if "anotacoes" not in fake_db[nome]:
        raise HTTPException(status_code=404, detail="Não há anotações para essa disciplina")

    if id_nota not in list(fake_db[nome]["anotacoes"].keys()):
        raise HTTPException(status_code=404, detail="Anotação Inexistente")

    fake_db[nome]["anotacoes"].pop(id_nota)
    return fake_db[nome]