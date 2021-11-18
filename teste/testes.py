from fastapi.testclient import TestClient
from ..main import app


client = TestClient(app)


def test_read_main():
    response = client.get("/disciplinas/")
    assert response.status_code == 202
    assert response.json() == {
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

def test_read_inexistent_discipline():
    response = client.get("/disciplinas/japones")
    assert response.status_code == 404
    assert response.text == "Disciplina japones Inexistente"

def test_read_complete_discipline():
    response = client.get("/disciplinas/matematica")
    assert response.status_code == 202
    assert response.json() == {
        "nome": "Matematica", 
        "professor": "Angélica", 
        "anotacoes": {
            "9470e1d7-bbbe-4037-9032-4b5e1c0ffddf": "Muito Legal!", 
            "f77fc0df-d9ac-4e70-a7c6-96d4bcf39484": "Gosto Muito", 
            "227ed50c-9cd9-4762-af8f-bc74954bdd9b": "Trabalhar Nisso"
        }
    }

def test_read_incomplete_discipline():
    response = client.get("/disciplinas/ingles")
    assert response.status_code == 202
    assert response.json() == {"nome": "Ingles", }

def test_read_all_disciplines_names():
    response = client.get("/disciplinas/nomes/")
    assert response.status_code == 202
    assert response.json() == ["Matematica", "Quimica", "Portugues", "Ingles"]

def test_read_anotations_from_inexistent_discipline():
    response = client.get("/notas/japones")
    assert response.status_code == 404
    assert response.text == "Disciplina japones Inexistente"

def test_read_anotations_from_discipline_without_anotations():
    response = client.get("/notas/ingles")
    assert response.status_code == 404
    assert response.text == "Não há anotações nesta disciplina"

def test_read_anotations_from_discipline_with_one_anotation():
    response = client.get("/notas/quimica")
    assert response.status_code == 202
    assert response.json() == ["Meh"]

def test_read_anotations_from_discipline_with_multiple_anotations():
    response = client.get("/notas/matematica")
    assert response.status_code == 202
    assert response.json() == ["Muito Legal!", "Gosto Muito", "Trabalhar Nisso"]


def test_create_discipline_that_already_exists():
    response = client.post(
        "/disciplinas/",
        json={
            "nome": "Matematica"
        }
    )
    assert response.status_code == 418
    assert response.text == "Disciplina já existe"

def test_create_discipline_with_just_name_and_delete():
    response = client.post(
        "/disciplinas/",
        json={
            "nome": "Historia"
        }
    )
    assert response.status_code == 201
    assert response.json() == {
        "historia": {
            "nome": "Historia"
        }
    }

    response = client.delete("/disciplinas/historia")
    assert response.status_code == 200

    test_read_main()


def test_create_discipline_with_name_and_professor_and_delete():
    response = client.post(
        "/disciplinas/",
        json={
            "nome": "Historia",
            "professor": "Arnaldo"
        }
    )
    assert response.status_code == 201
    assert response.json() == {
        "historia": {
            "nome": "Historia",
            "professor": "Arnaldo"
        }
    }

    response = client.delete("/disciplinas/historia")
    assert response.status_code == 200

    test_read_main()

def test_create_discipline_complete_and_delete():
    response = client.post(
        "/disciplinas/",
        json={
            "nome": "Historia",
            "professor": "Arnaldo",
            "anotacoes": {
                "74337955-23a3-46a8-9e6a-cdf06b00cb3f": "Uma bela anotação",
                "32b55134-38dd-4c3f-bfe2-a8847f9ec37f": "Pode ter mais de uma"
            }
        }
    )
    assert response.status_code == 201
    assert response.json() == {
        "historia": {
            "nome": "Historia",
            "professor": "Arnaldo",
            "anotacoes": {
                "74337955-23a3-46a8-9e6a-cdf06b00cb3f": "Uma bela anotação",
                "32b55134-38dd-4c3f-bfe2-a8847f9ec37f": "Pode ter mais de uma"
            }
        }
    }

    response = client.delete("/disciplinas/historia")
    assert response.status_code == 200

    test_read_main()

def test_add_anotations_from_inexistent_discipline():
    response = client.put("/notas/japones")
    assert response.status_code == 404
    assert response.text == "Disciplina japones Inexistente"

def test_add_anotations_from_discipline_without_notes_and_delete():
    response = client.put(
        "/notas/ingles",
        params= {
            "id_nota": "9d752a00-2185-43c6-b6db-269f11b16029", 
            "nota": "Nota adicionada com sucesso!"
        }
    )
    assert response.status_code == 200
    assert response.json() == {
        "nome": "Ingles",
        "anotacoes": {
            "9d752a00-2185-43c6-b6db-269f11b16029": "Nota adicionada com sucesso!"
        }
    }

    response = client.delete("/notas/ingles/9d752a00-2185-43c6-b6db-269f11b16029")
    assert response.status_code == 200

def test_add_anotations_from_discipline_with_notes_and_delete():
    response = client.put(
        "/notas/matematica",
        params= {
            "id_nota": "9d752a00-2185-43c6-b6db-269f11b16027", 
            "nota": "Nota adicionada com sucesso!"
        }
    )
    assert response.status_code == 200
    assert response.json() == {
        "nome": "Matematica",
        "professor":"Angélica",
        "anotacoes": {
            "9470e1d7-bbbe-4037-9032-4b5e1c0ffddf": "Muito Legal!", 
            "f77fc0df-d9ac-4e70-a7c6-96d4bcf39484": "Gosto Muito", 
            "227ed50c-9cd9-4762-af8f-bc74954bdd9b": "Trabalhar Nisso",
            "9d752a00-2185-43c6-b6db-269f11b16027": "Nota adicionada com sucesso!"
        }
    }

    response = client.delete("/notas/matematica/9d752a00-2185-43c6-b6db-269f11b16027")
    assert response.status_code == 200

def test_modify_anotations_from_inexistent_discipline():
    response = client.patch(
        "/notas/japones/9470e1d7-bbbe-4037-9032-4b5e1c0ffddf"
    )
    assert response.status_code == 404
    assert response.text == "Disciplina japones Inexistente"

def test_modify_anotations_from_discipline_without_notes():
    response = client.patch(
        "/notas/portugues/9470e1d7-bbbe-4037-9032-4b5e1c0ffddf"
    )
    assert response.status_code == 404
    assert response.text == "Não há anotações nesta disciplina"

def test_modify_anotations_from_discipline():
    response = client.patch(
        "/notas/matematica/f77fc0df-d9ac-4e70-a7c6-96d4bcf39484",
        params= {
            "nota": "Nota modificada com sucesso!"
        }
    )
    assert response.status_code == 200
    assert response.json() == {
        "nome": "Matematica",
        "professor":"Angélica",
        "anotacoes": {
            "9470e1d7-bbbe-4037-9032-4b5e1c0ffddf": "Muito Legal!", 
            "f77fc0df-d9ac-4e70-a7c6-96d4bcf39484": "Nota modificada com sucesso!", 
            "227ed50c-9cd9-4762-af8f-bc74954bdd9b": "Trabalhar Nisso"
        }
    }

def test_modify_an_inexistent_discipline():
    response = client.patch("/disciplinas/japones")
    assert response.status_code == 404
    assert response.text == "Disciplina japones Inexistente"

def test_modify_discipline_name():
    response = client.patch(
        "/disciplinas/matematica",
        json ={
            "nome": "Matemática",
        }
    )
    assert response.status_code == 200
    assert response.json() == {
        "nome": "Matemática",
        "professor":"Angélica",
        "anotacoes": {
            "9470e1d7-bbbe-4037-9032-4b5e1c0ffddf": "Muito Legal!", 
            "f77fc0df-d9ac-4e70-a7c6-96d4bcf39484": "Nota modificada com sucesso!", 
            "227ed50c-9cd9-4762-af8f-bc74954bdd9b": "Trabalhar Nisso"
        }
    }

def test_modify_discipline_name_and_professor():
    response = client.patch(
        "/disciplinas/matemática",
        json ={
            "nome": "Matematic",
            "professor":"Paulo",
        }
    )
    assert response.status_code == 200
    assert response.json() == {
        "nome": "Matematic",
        "professor":"Paulo",
        "anotacoes": {
            "9470e1d7-bbbe-4037-9032-4b5e1c0ffddf": "Muito Legal!", 
            "f77fc0df-d9ac-4e70-a7c6-96d4bcf39484": "Nota modificada com sucesso!", 
            "227ed50c-9cd9-4762-af8f-bc74954bdd9b": "Trabalhar Nisso"
        }
    }

def test_try_to_modify_discipline_note():
    response = client.patch(
        "/disciplinas/matematic",
        json ={
            "nome": "Matematica",
            "professor":"Paulo",
            "anotacoes": {
                "9470e1d7-bbbe-4037-9032-4b5e1c0ffddf": "Teste1", 
                "f77fc0df-d9ac-4e70-a7c6-96d4bcf39484": "Teste2", 
                "227ed50c-9cd9-4762-af8f-bc74954bdd9b": "Teste3"
            }
        }
    )
    assert response.status_code == 200
    assert response.json() == {
        "nome": "Matematica",
        "professor":"Paulo",
        "anotacoes": {
            "9470e1d7-bbbe-4037-9032-4b5e1c0ffddf": "Muito Legal!", 
            "f77fc0df-d9ac-4e70-a7c6-96d4bcf39484": "Nota modificada com sucesso!", 
            "227ed50c-9cd9-4762-af8f-bc74954bdd9b": "Trabalhar Nisso"
        }
    }

def test_modify_discipline_adding_professor_and_notes():
    response = client.patch(
        "/disciplinas/quimica",
        json ={
            "nome": "Química",
            "professor":"Rogério",
            "anotacoes": {
                "9470e1d7-bbbe-4037-9032-4b5e1c0ffddf": "Teste1", 
                "f77fc0df-d9ac-4e70-a7c6-96d4bcf39484": "Teste2", 
                "227ed50c-9cd9-4762-af8f-bc74954bdd9b": "Teste3"
            }
        }
    )
    assert response.status_code == 200
    assert response.json() == {
        "nome": "Química",
        "professor":"Rogério",
        "anotacoes": {
            "9d752a00-2185-43c6-b6db-269f11b16029": "Meh"
        }
    }

def test_delete_inexistent_discipline():
    response = client.delete("/disciplinas/japones")
    assert response.status_code == 404
    assert response.text == "Disciplina japones Inexistente"

def test_delete_note_with_inexistent_discipline():
    response = client.delete("/notas/japones/9470e1d7-bbbe-4037-9032-4b5e1c0ffddf")
    assert response.status_code == 404
    assert response.text == "Disciplina japones Inexistente"

def test_delete_inexistent_note():
    response = client.delete("/notas/química/ac0c3a10-f338-44eb-8f76-92e7c1983681")
    assert response.status_code == 404
    assert response.text == "Anotação Inexistente"