from fastapi import APIRouter, Depends, Response, HTTPException, status
from db.models import *
from sqlalchemy.orm import Session
import requests
from functions.function import * 
from delegacion.repository.delegacion import insert_delegacion
from db.session import get_db, engine 

router = APIRouter(
    prefix='/delegacion',
    tags=['Delegacion']
)

@router.get("/")
async def datos_delegaciones(response:Response,db: Session = Depends(get_db)):
	datos = obtener_datos_delegaciones()
	insert_delegacion(datos,db)
	return {"Respuesta":"Insert de delegaciones creados satisfactoriamente!!"}