from fastapi import APIRouter, Depends, Response
from db.models import *
from sqlalchemy.orm import Session
from functions.function import * 
from delegacion.repository.delegacion import insert_delegacion,obtener_todas_delegaciones
from db.session import get_db 

router = APIRouter(
    prefix='/api/v1',
    tags=['Delegacion']
)

@router.get("/delegacion")
async def datos_delegaciones(response:Response,db: Session = Depends(get_db)):
	datos = obtener_datos_delegaciones()
	insert_delegacion(datos,db)
	return {"Respuesta":"Datos insertados satisfactoriamente!"}

@router.get("/obtener_delegaciones")
async def obtener_delegaciones(response:Response,db: Session = Depends(get_db)):
	datos = obtener_todas_delegaciones(db)
	return datos 
