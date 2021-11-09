from typing import Dict, Optional

from fastapi import FastAPI, Query, Path, HTTPException
from fastapi.param_functions import Body
from pydantic import BaseModel, Field
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
    "matemática": {"nome": "Matemática", "professor": "Angélica", "anotacoes": 
        {uuid4(): "Muito Legal!", uuid4(): "Gosto Muito", uuid4(): "Trabalhar Nisso"}
    },
    "química": {"nome": "Química", "professor": "Fê", "anotacoes": {uuid4(): "Meh"}},
    "português": {"nome": "Português", "professor": "Arnaldo"},
    "ingles": {"nome": "Ingles"} 
}


# Lista tudo de todas as disciplinas
@app.get("/disciplinas/")
def ler_tudo():
    return fake_db


# Lista tudo de uma disciplina
@app.get("/disciplinas/{nome_disciplina}", response_model=Disciplina, response_model_exclude_unset=True)
def ler_disciplinas(
    nome_disciplina: str = Path(..., description="O nome da disciplina desejada", example="Foo")
):
    nome = nome_disciplina.casefold()
    if nome not in fake_db:
        raise HTTPException(status_code=404, detail="Item not found")
    return fake_db[nome]


# Lista o nome das disciplinas
@app.get("/disciplinas/nomes/")
def ler_nomes():
    todos_nomes = []
    for i in fake_db.values():
        todos_nomes.append(i["nome"])
    return todos_nomes


# Lista as anotações de uma disciplina
@app.get("/disciplinas/{anotacao_disciplina}/notas/")
def ler_anotacao(
    anotacao_disciplina: str = Path(..., description="Nome da disciplina contendo as anotações desejadas", example="Bar")
):
    if anotacao_disciplina not in fake_db or "anotacoes" not in fake_db[anotacao_disciplina]:
        raise HTTPException(status_code=404, detail="Item not found")
    
    notas = fake_db[anotacao_disciplina]["anotacoes"]

    return list(notas.values())


# Cria disciplina
@app.post("/disciplinas/", response_model=Disciplina, response_model_exclude_unset=True)
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
                    "nome": "Bar",
                    "anotacoes": {"uuid_1": "Uma bela anotação", uuid4(): "Pode ter mais de uma"}
                }
            },
            "minimo": {
                "summary": "Exemplo mínimo",
                "description": "Um exemplo com apenas os elementos obrigatórios.",
                "value": {
                    "nome": "Bar"
                }
            }
        }
    )
):
    nome_disciplina = disciplina.nome.casefold()
    if nome_disciplina in fake_db:
        raise HTTPException(status_code=418, detail="Disciplina já existe")
    
    fake_db.update({nome_disciplina: disciplina})
    return disciplina


# Adiciona nota em uma disciplina
@app.put("/disciplinas/{nome_disciplina}/{id_nota}", response_model=Disciplina, response_model_exclude_unset=True) 
def adiciona_nota(
    nome_disciplina: str = Path(..., description="O nome da disciplina que terá uma nota nova", example="Baz"),
    id_nota: UUID = Path(..., description="Id da nota a ser adicionada", example="Quux"),
    nota: str = Query(...,  description="Nota a ser adicionada")
):
    if nome_disciplina not in fake_db:
        raise HTTPException(status_code=404, detail="Item not found")

    if "anotacoes" not in fake_db[nome_disciplina]:
        fake_db[nome_disciplina].update({"anotacoes": {}})

    fake_db[nome_disciplina]["anotacoes"].update({id_nota: nota})

    return fake_db[nome_disciplina]


# Modifica nota em uma disciplina
@app.put("/disciplinas/{nome_disciplina}/modifica/{id_nota}", response_model=Disciplina, response_model_exclude_unset=True) 
def modifica_nota(
    nome_disciplina: str = Path(..., description="O nome da disciplina que terá uma nota modificada", example="Baz"),
    id_nota: UUID = Path(..., description="Id da nota a ser modificada", example="Quux"),
    nova_nota: str = Query(...,  description="Nova nota a ser adicionada")
):

    if nome_disciplina not in fake_db or "anotacoes" not in fake_db[nome_disciplina] or id_nota not in fake_db[nome_disciplina]["anotacoes"]:
        raise HTTPException(status_code=404, detail="Item not found")

    fake_db[nome_disciplina]["anotacoes"].update({id_nota: nova_nota})

    return fake_db[nome_disciplina]

# Modifica tudo em uma disciplina
@app.patch("/disciplinas/{nome_disciplina}", response_model=Disciplina, response_model_exclude_unset=True)
def modifica_tudo(
    nome_disciplina: str = Path(..., description="O nome da disciplina que terá tudo modificado", example="Baz"),
    disciplina: Disciplina = Body(...),
):

    if nome_disciplina not in fake_db:
        raise HTTPException(status_code=404, detail="Item not found")

    if disciplina.nome:
        fake_db[nome_disciplina]["nome"] = disciplina.nome

    if disciplina.professor:
        fake_db[nome_disciplina]["professor"] = disciplina.professor



# Deleta disciplina
@app.delete("/disciplinas/{nome_disciplina}")
def deleta_disciplina(
    nome_disciplina: str = Path(..., description="O nome da disciplina a ser deletada", example="Baz")
):
    if nome_disciplina not in fake_db:
        raise HTTPException(status_code=404, detail="Item not found")

    fake_db.pop(nome_disciplina)


# Deleta nota de uma disciplina
@app.delete("/disciplinas/{nome_disciplina}/{id_nota}", response_model=Disciplina, response_model_exclude_unset=True)
def deleta_nota(
    nome_disciplina: str = Path(..., description="O nome da disciplina a ser deletada", example="Qux"),
    id_nota: UUID = Path(..., description="Id da nota a ser deletada", example="Quux"),
):
    if nome_disciplina not in fake_db or id_nota not in list(fake_db[nome_disciplina]["anotacoes"].keys()) :
        raise HTTPException(status_code=404, detail="Item not found")

    fake_db[nome_disciplina]["anotacoes"].pop(id_nota)

    return fake_db[nome_disciplina]