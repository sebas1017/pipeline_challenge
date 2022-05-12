from sqlalchemy.orm import Session 
from db.models.statistics import Delegaciones
from fastapi import HTTPException,status
import requests

def delete_all_delegacion(db:Session):
    db.query(Delegaciones).delete()
    db.commit()
def insert_delegacion(datos,db:Session):
    delete_all_delegacion(db)
    for i in datos:
        new_delegacion = Delegaciones(delegacion=i["delegacion"],titulo="alcalde",nombre=i["alcalde"],codigo_postal_inicial=i["codigo_inicial"],codigo_postal_final=i["codigo_final"])
        db.add(new_delegacion)
        db.commit()
        db.refresh(new_delegacion)