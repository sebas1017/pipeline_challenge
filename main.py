from fastapi import FastAPI, Response, Depends
from psycopg2 import OperationalError
from core.config import settings
from sqlalchemy.orm import Session
from db.session import get_db, engine 
from db.base import Base  
from db.models.statistics import Delegaciones, Vehicles
from delegacion.routers import delegacion
from functions.function import execute_calculus_postal_codes
import requests
import os
import uvicorn



def create_tables():           
	Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.PROJECT_NAME,version=settings.PROJECT_VERSION)

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



@app.get("/api/v1/all_vehicles")
async def all_vehicles(response:Response, db: Session = Depends(get_db)):
	url = "https://datos.cdmx.gob.mx/api/3/action/datastore_search?resource_id=ad360a0e-b42f-482c-af12-1fd72140032e"	
	response = requests.get(url)
	units_final_availables = []
	if response.status_code == 200:
		units_availables =  response.json()["result"]["records"]
		for unit in units_availables:
				data = {
				"vehicle_id":unit["vehicle_id"],
				"vehicle_label":unit["vehicle_label"],
				"vehicle_current_status":unit["vehicle_current_status"],
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
		db.execute(
        """ SELECT SETVAL('public."vehicles_id_seq"', COALESCE(MAX(id), 1)) FROM vehicles""")
		insert_data(db, units_final_availables)
		filter_units_availables=[ record for record in units_final_availables if record["vehicle_current_status"]==1]
		return filter_units_availables	

	else:
		response.status_code = 500
		return {"message":"Error en API externa de datos de metrobus recargar nuevamente"}

				


@app.get("/api/v1/vehicles_delegations")
async def vehicles_delegations(response:Response, db: Session = Depends(get_db)):
	total_vehicles = db.query(Vehicles).all()
	total_delegations = db.query(Delegaciones).all()
	total_vehicles = [(record.vehicle_id,record.position_latitude,record.position_longitude) for record in total_vehicles]
	total_delegations = [(record.delegacion,record.codigo_postal_inicial,record.codigo_postal_final)for record in total_delegations]
	execute_calculus_postal_codes(total_vehicles,total_delegations )
	return {"message":"ok"}




@app.get("/api/v1/vehicles/{id}")
async def filter_vehicles(id, response:Response, db: Session = Depends(get_db)):
	data_vehicles_filter = db.query(Vehicles).filter(Vehicles.vehicle_id==id).all()
	if len(data_vehicles_filter) == 0:
		response.status_code = 404
		return {"message":"El id ingresado no existe en la base de datos"}
	else:
		data_vehicles_filter = data_vehicles_filter[0]
		data = {
					"position_latitude":data_vehicles_filter.position_latitude,
					"position_longitude":data_vehicles_filter.position_longitude,
					}
		response.status_code = 200
		return data
	
app.include_router(delegacion.router)
if __name__=="__main__":
	PORT = int(os.environ.get('PORT', 8000))
	uvicorn.run("main:app",host='0.0.0.0',port=PORT ,reload=True)