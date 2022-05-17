from distutils.util import execute
from sqlalchemy.orm import Session 
from db.models.statistics import Delegaciones,DelegationsVehicles, Vehicles
import geopy
import pandas as pd
import requests

def delete_all_delegacion(db:Session):
    db.query(DelegationsVehicles).delete()
    db.query(Delegaciones).delete()
    db.commit()
    db.execute(
        """ SELECT SETVAL('public."delegaciones_id_seq"', COALESCE(MAX(id), 1)) FROM delegaciones""")
    db.execute(
        """ SELECT SETVAL('public."delegaciones_vehicles_id_seq"', COALESCE(MAX(id), 1)) FROM delegaciones_vehicles""")

def insert_delegacion(datos,db:Session):
    delete_all_delegacion(db)
    for i in datos:
        new_delegacion = Delegaciones(delegacion=i["delegacion"],titulo="alcalde",nombre=i["alcalde"],codigo_postal_inicial=i["codigo_inicial"],codigo_postal_final=i["codigo_final"])
        db.add(new_delegacion)
        db.commit()
        db.refresh(new_delegacion)
    insert_relacion_delegaciones(db)

    
def obtener_todas_delegaciones(db:Session):
    delegaciones = db.query(Delegaciones).all()
    return delegaciones


def get_zipcode(df, geolocator, lat_field, lon_field,ids):
	location = geolocator.reverse((df[lat_field], df[lon_field]))
	if "postcode" in list(location.raw["address"].keys()):
		return (df[ids],location.raw["address"]["postcode"])
	else:
		place_id = location.raw["place_id"]
		response = requests.get(f"https://nominatim.openstreetmap.org/details.php?place_id={place_id}&addressdetails=1&hierarchy=0&group_hierarchy=1&polygon_geojson=1&format=json")
		postcode = response.json()["calculated_postcode"]
		return (df[ids],postcode)


def execute_calculus_postal_codes(array_vehicles,array_delegations):
	array_ids = [record[0]for record in array_vehicles]
	array_lats =[record[1] for record in array_vehicles ] 
	array_longs = [record[2] for record in array_vehicles]

	geolocator = geopy.Nominatim(user_agent='api_postalcodes')

	df = pd.DataFrame({
	'Lat': array_lats,
	'Lon': array_longs,
	'id':array_ids
	})
	zipcodes = df.apply(get_zipcode, axis=1, geolocator=geolocator, lat_field='Lat', lon_field='Lon', ids='id')
	results_relations_delegations = []
	for k , v in zipcodes.iteritems():
		vehicle_id = int(v[0])
		post_code = int(v[1])
		
		for delegation in array_delegations:
			code_init, code_end = int(delegation[1]),int(delegation[2])
			if post_code >= code_init and post_code <=code_end:
				results_relations_delegations.append((vehicle_id, delegation[0], delegation[3]))
	return results_relations_delegations


def insert_relacion_delegaciones(db:Session):
    total_vehicles = db.query(Vehicles).all()
    total_delegations = db.query(Delegaciones).all()
    total_vehicles = [(record.vehicle_id,record.position_latitude,record.position_longitude) for record in total_vehicles]
    total_delegations = [(record.delegacion,record.codigo_postal_inicial,record.codigo_postal_final,record.id)for record in total_delegations]
    relations_data = execute_calculus_postal_codes(total_vehicles,total_delegations )
    db.query(DelegationsVehicles).delete()
    db.commit()
    for record in relations_data:
        data = DelegationsVehicles(
            vehicle_id = record[0],
            delegation_name = record[1],
            delegation_id =   record[2],
        )
        db.add(data)
        db.commit()
        db.refresh(data)
   
