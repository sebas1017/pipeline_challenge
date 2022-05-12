from sqlalchemy.orm import Session 
from db.models.statistics import Delegaciones
from fastapi import HTTPException,status
import requests

def insert_delegacion(datos,db:Session):
    for i in datos:
        new_delegacion = Delegaciones(delegacion=i["delegacion"],titulo="alcalde",nombre=i["alcalde"],codigo_postal_inicial=i["codigo_inicial"],codigo_postal_final=i["codigo_final"])
        db.add(new_delegacion)
        db.commit()
        db.refresh(new_delegacion)