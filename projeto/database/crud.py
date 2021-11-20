from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from .. import schemas
from . import models


# Extra CRUDs
def get_one_note(db: Session, nome: str, id: int):
    return db.query(models.Anotacao).filter(models.Anotacao.nome_disciplina == nome, models.Anotacao.id == id).first()

# CRUD para as disciplinas
def get_all_discipline(db: Session):
    return db.query(models.Disciplina).all()

def get_discipline(db: Session, nome: str):
    return db.query(models.Disciplina).filter(models.Disciplina.nome == nome).first()

def get_all_discipline_names(db: Session):
    names = []
    model_name = models.Disciplina.nome
    for name in db.query(model_name).all():
        names.append(name[model_name])
    return names

def create_discipline(db: Session, disciplina: schemas.DisciplinaCreate):
    db_discipline = models.Disciplina(**disciplina.dict())
    db.add(db_discipline)
    db.commit()
    db.refresh(db_discipline)
    return db_discipline

def modify_discipline(db: Session, nome: str, disciplina: schemas.Disciplina):
    discip = get_discipline(db, nome)
    disc_json = jsonable_encoder(discip)
    discip_model = schemas.Disciplina(**disc_json)

    new_disc = disciplina.dict(exclude_unset=True)
    updated_disc = jsonable_encoder(discip_model.copy(update=new_disc))
    
    db.query(models.Disciplina).filter(models.Disciplina.nome == nome).update(updated_disc)
    db.commit()

    return updated_disc

def delete_discipline(db: Session, nome: str):
    db.query(models.Disciplina).filter(models.Disciplina.nome == nome).delete()
    db.commit()


# CRUD para as anotações
def get_discipline_notes(db: Session, nome: str):
    notas = []
    nome_notas = models.Anotacao.nome_disciplina
    for anotacao in db.query(models.Anotacao).filter(nome_notas == nome).all():
        notas.append(anotacao.nota)
    return notas
    # return db.query(models.Anotacao).filter(models.Anotacao.nome_disciplina == nome).all()

def add_discipline_note(db: Session, nota: schemas.AnotacaoCreate, nome: str):
    db_anotacao = models.Anotacao(**nota.dict(), nome_disciplina = nome)
    db.add(db_anotacao)
    db.commit()
    db.refresh(db_anotacao)
    return db_anotacao

def modify_note(db: Session, id: int, nota: schemas.Anotacao):
    note = get_one_note(db, nota.nome_disciplina, id)
    note_json = jsonable_encoder(note)
    note_model = schemas.Anotacao(**note_json)

    new_note = nota.dict(exclude_unset=True)
    update_note = jsonable_encoder(note_model.copy(update = new_note))

    db.query(models.Anotacao).filter(models.Anotacao.nome_disciplina == nota.nome_disciplina, models.Anotacao.id == id).update(update_note)
    db.commit()

    return update_note

def delete_discipline_note(db: Session, nome: str, id: int):
    db.query(models.Anotacao).filter(models.Anotacao.nome_disciplina == nome, models.Anotacao.id == id).delete()
    db.commit()