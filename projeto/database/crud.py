from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from .. import schemas
from . import models


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
    discip = db.query(models.Disciplina).filter(models.Disciplina.nome == nome).first()
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