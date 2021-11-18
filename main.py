from fastapi import FastAPI,  status, HTTPException, Query, Path, Depends
from fastapi.responses import PlainTextResponse
from fastapi.param_functions import Body

from starlette.exceptions import HTTPException as StarletteHTTPException
from pydantic import BaseModel, Field
from typing import Dict, Optional
from uuid import UUID, uuid4

app = FastAPI()


fake_db = {
    "matematica": {
        "nome": "Matematica", 
        "professor": "Angélica", 
        "anotacoes": {
            "9470e1d7-bbbe-4037-9032-4b5e1c0ffddf": "Muito Legal!", 
            "f77fc0df-d9ac-4e70-a7c6-96d4bcf39484": "Gosto Muito", 
            "227ed50c-9cd9-4762-af8f-bc74954bdd9b": "Trabalhar Nisso"
        }
    },
    "quimica": {
        "nome": "Quimica",
        "anotacoes": {
            "9d752a00-2185-43c6-b6db-269f11b16029": "Meh"
        }
    },
    "portugues": {
        "nome": "Portugues", 
        "professor": "Arnaldo"
    },
    "ingles": {
        "nome": "Ingles"
    } 
}


#===================================#
#               Models              #
#===================================#

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


#=======================================#
#               Dependences             #
#=======================================#

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
            },
        }
    )
):
    return disciplina

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

async def verifica_diciplina(disciplina: Disciplina = Depends(disc)):
    if disciplina.nome.casefold() in fake_db:
        raise HTTPException(status_code=418, detail="Disciplina já existe")


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
    deprecated=True,
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
    dependencies= [Depends(verifica_nome)],
)
def ler_disciplinas(nome: str = Depends(nome_disc)):
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
    "/disciplinas/notas/{nome_disciplina}", 
    status_code=status.HTTP_202_ACCEPTED, 
    tags=["Anotações"],
    summary="Devolve as Anotações",
    description="Retorna uma lista com o as anotações de uma disciplina",
    dependencies= [Depends(verifica_nome), Depends(verifica_campo_nota)],
)
def ler_anotacao(nome: str = Depends(nome_disc)):
    notas = fake_db[nome]["anotacoes"]
    return list(notas.values())


#=======================================#
#           POSTS/PUTS/PATCHS           #
#=======================================#

# Cria disciplina
@app.post(
    "/disciplinas/",
    status_code=status.HTTP_201_CREATED, 
    tags=["Disciplinas"],
    summary="Cria uma Disciplina",
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

# Adiciona nota em uma disciplina
@app.put(
    "/disciplinas/{nome_disciplina}", 
    response_model=Disciplina,
    response_model_exclude_unset=True,
    status_code=status.HTTP_200_OK, 
    tags=["Anotações"],
    summary="Adiciona uma Nota",
    description="Cria uma nova nota dentro da disciplina",
    dependencies= [Depends(verifica_nome)],
) 
def adiciona_nota(commons: CommonInfoQ = Depends()):
    nome = commons.nome_disciplina

    if "anotacoes" not in fake_db[nome]:
        fake_db[nome].update({"anotacoes": {}})

    fake_db[nome]["anotacoes"].update({commons.id_nota: commons.nota})
    return fake_db[nome]

# Modifica nota em uma disciplina
@app.patch(
    "/disciplinas/{nome_disciplina}/{id_nota}", 
    response_model=Disciplina, 
    response_model_exclude_unset=True, 
    status_code=status.HTTP_200_OK, 
    tags=["Anotações"],
    summary="Modifica uma Nota",
    description="Modifica uma nota existente dentro da disciplina",
    dependencies= [Depends(verifica_nome), Depends(verifica_campo_nota), Depends(verifica_nota_especifica)],
) 
def modifica_nota(commons: CommonInfoP = Depends()):
    nome = commons.nome_disciplina
    id_nota = commons.id_nota
    fake_db[nome]["anotacoes"].update({id_nota: commons.nota})

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
    dependencies= [Depends(verifica_nome)],

)
def modifica_tudo(nomeD: str = Depends(nome_disc), disciplina: Disciplina = Depends(disc)):

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
@app.delete( "/disciplinas/{nome_disciplina}", tags=["Disciplinas"], summary="Deleta uma Disciplina", dependencies= [Depends(verifica_nome)],)
def deleta_disciplina(nome: str = Depends(nome_disc)):
    fake_db.pop(nome)

# Deleta nota de uma disciplina
@app.delete(
    "/disciplinas/{nome_disciplina}/{id_nota}", 
    response_model=Disciplina, 
    tags=["Anotações"],
    summary="Deleta uma Anotação",
    dependencies= [Depends(verifica_nome), Depends(verifica_campo_nota), Depends(verifica_nota_especifica)],
)
def deleta_nota(commons: NotaDisciplinaQuery = Depends()):
    nome = commons.nome_disciplina
    id_nota = commons.id_nota

    fake_db[nome]["anotacoes"].pop(id_nota)
    return fake_db[nome]
