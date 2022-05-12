from argparse import _UNRECOGNIZED_ARGS_ATTR
from fastapi import FastAPI, Response, Depends
from psycopg2 import OperationalError
from bs4 import BeautifulSoup
from core.config import settings
from sqlalchemy.orm import Session
from db.session import get_db, engine 
from db.base import Base  
from db.models.statistics import StatisticsCountries, Vehicles
import json
import requests
import pandas as pd
import time
import random
import hashlib
import os
import uvicorn
from functions.function import *
def create_tables():           
	Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.PROJECT_NAME,version=settings.PROJECT_VERSION)
# app = FastAPI()
create_tables()      
	
def insert_data(db, data):
	try:
		for record in data:
			db_statistics = Vehicles(
			vehicle_id = record["vehicle_id"]
			)
			db.add(db_statistics)
			db.commit()
			db.refresh(db_statistics)
		return True
	except OperationalError:
		return "Por el momento nuestro servidor se encuentra abajo Espere por favor..."


@app.get("/")
async def index(response:Response):#, db: Session = Depends(get_db)):
	  return {"message":"hola mundo"}

@app.get("/ruta")
async def datos_delegaciones(response:Response):
	datos = obtener_datos_delegaciones()
	print(datos)
	return ""
async def index(response:Response, db: Session = Depends(get_db)):
	url = "https://datos.cdmx.gob.mx/api/3/action/datastore_search?resource_id=ad360a0e-b42f-482c-af12-1fd72140032e"	
	response = requests.get(url)
	units_final_availables = []
	if response.status_code == 200:
		units_availables =  response.json()["result"]["records"]
		for unit in units_availables:
			if unit["vehicle_current_status"] == 1:
				units_final_availables.append(unit)
		data = db.query(Vehicles).all()
		if len(data) < len(units_final_availables):
			units_final_availables = units_final_availables[len(data)-1 :]
			insert_data(db, units_final_availables)
		response.status_code == 200
		return {"message":"Proceso realizado correctamente"}
	else:
		response.status_code == 500
		return {"message":"Error en API externa de datos de metrobus recargar nuevamente"}

				





@app.get("/api/v1/vehicles/{id}")
async def index(id, response:Response, db: Session = Depends(get_db)):
	print(dir( db.query(Vehicles)))
	data_vehicles_filter = db.query(Vehicles).where(Vehicles.vehicle_id==id)
	print(data_vehicles_filter)
	
	return {"message":"Desde el 2 endpoint"}

if __name__=="__main__":
	PORT = int(os.environ.get('PORT', 8000))
	uvicorn.run("main:app",host='0.0.0.0',port=PORT ,reload=True)