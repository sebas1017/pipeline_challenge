from fastapi import APIRouter, Depends, Response
from db.models import *
from sqlalchemy.orm import Session
from db.models.statistics import Vehicles,DelegationsVehicles
from functions.function import * 
from psycopg2 import OperationalError

from db.session import get_db 

router = APIRouter(
    prefix='/api/v1',
    tags=['Vehiculos']
)


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


@router.get("/insert_vehicles")
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
		return {"message":"insercion de vehiculos exitosa"}

	else:
		response.status_code = 500
		return {"message":"Error en API externa de datos de metrobus recargar nuevamente"}

				
@router.get("/get_all_vehicles")
async def vehicles_delegations(response:Response, db: Session = Depends(get_db)):
	vehicles_total = db.query(Vehicles).filter(Vehicles.vehicle_current_status==1).all()
	if len(vehicles_total) == 0:
		return {"message":"No existen vehiculos creados , favor ejecutar el endpoint insert_vehicles primer"}
	else:
		return vehicles_total


@router.get("/get_relation_vehicles_delegations")
async def get_relation_vehicles_delegations(response:Response, db: Session = Depends(get_db)):
	final_relation = {}
	relations  = db.query(DelegationsVehicles).all()
	if len( relations ) == 0:
		return {"message" : "no existen datos de delegaciones"}
	else:
		for delegation in relations:
			if delegation.delegation_name in final_relation:
				final_relation[delegation.delegation_name]["vehicles_ids"].append(delegation.vehicle_id)
			else:
				final_relation[delegation.delegation_name] ={"vehicles_ids": [delegation.vehicle_id]}
		return final_relation
		
		




@router.get("/vehicles/{id}")
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