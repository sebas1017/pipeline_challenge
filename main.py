from fastapi import FastAPI, Response, Depends
from psycopg2 import OperationalError
from core.config import settings
from sqlalchemy.orm import Session
from db.session import get_db, engine 
from db.base import Base  
from db.models.statistics import Vehicles



import json
import requests
import pandas as pd
import time
import random
import hashlib
import os
import uvicorn
# from functions.function import *
from delegacion.routers import delegacion
def create_tables():           
	Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.PROJECT_NAME,version=settings.PROJECT_VERSION)
# app = FastAPI()
create_tables()      
	
def insert_data(db, data):
	try:
		for record in data:
			db_statistics = Vehicles(
			 **record
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


@app.get("/api/v1/all_vehicles")
async def index(response:Response, db: Session = Depends(get_db)):
	url = "https://datos.cdmx.gob.mx/api/3/action/datastore_search?resource_id=ad360a0e-b42f-482c-af12-1fd72140032e"	
	response = requests.get(url)
	units_final_availables = []
	if response.status_code == 200:
		units_availables =  response.json()["result"]["records"]
		for unit in units_availables:
			if unit["vehicle_current_status"] == 1:
				data = {
				"vehicle_id":unit["vehicle_id"],
				"vehicle_label":unit["vehicle_label"],
				"position_latitude":unit["position_latitude"],
				"position_longitude":unit["position_longitude"],
				"position_speed":unit["position_speed"],
				"position_odometer":unit["position_odometer"],
				"trip_schedule_relationship":unit["trip_schedule_relationship"],
				"trip_id":unit["trip_id"],
				"trip_route_id":unit["trip_route_id"]
				}
				units_final_availables.append(data)
		db.query(Vehicles).delete()
		db.commit()
		insert_data(db, units_final_availables)
		return units_final_availables
		
			

	else:
		response.status_code == 500
		return {"message":"Error en API externa de datos de metrobus recargar nuevamente"}

				





@app.get("/api/v1/vehicles/{id}")
async def index(id, response:Response, db: Session = Depends(get_db)):
	data_vehicles_filter = db.query(Vehicles).filter(Vehicles.vehicle_id==id).all()
	if len(data_vehicles_filter) == 0:
		response.status_code == 404
		return {"message":"El id ingresado no existe en la base de datos"}
	else:
		data_vehicles_filter = data_vehicles_filter[0]
		data = {
					"vehicle_id":data_vehicles_filter.vehicle_id,
					"vehicle_label":data_vehicles_filter.vehicle_label,
					"position_latitude":data_vehicles_filter.position_latitude,
					"position_longitude":data_vehicles_filter.position_longitude,
					"position_speed":data_vehicles_filter.position_speed,
					"position_odometer":data_vehicles_filter.position_odometer,
					"trip_schedule_relationship":data_vehicles_filter.trip_schedule_relationship,
					"trip_id":data_vehicles_filter.trip_id,
					"trip_route_id":data_vehicles_filter.trip_route_id
					}
		response.status_code == 200
		return data
	
app.include_router(delegacion.router)
if __name__=="__main__":
	PORT = int(os.environ.get('PORT', 8000))
	uvicorn.run("main:app",host='0.0.0.0',port=PORT ,reload=True)