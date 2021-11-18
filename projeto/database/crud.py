from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import null
from . import models
from .. import schemas

# CRUD para as disciplinas
def get_discipline(db: Session, nome: str):
    return db.query(models.Disciplina).filter(models.Disciplina.nome == nome).first()

def get_all_discipline(db: Session):
    return db.query(models.Disciplina).all()

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

pass

def delete_discipline(db: Session, nome: str):
    db.query(models.Disciplina).filter(models.Disciplina.nome == nome).delete()
    db.commit()
