from fastapi import FastAPI, Response, Depends
from psycopg2 import OperationalError
from bs4 import BeautifulSoup
from core.config import settings
from sqlalchemy.orm import Session
from db.session import get_db, engine 
from db.base import Base  
from db.models.statistics import StatisticsCountries
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
	
def insert_data(statistics, db):
	try:
		db_statistics = StatisticsCountries(
		total_time = statistics['Time [ms]'].sum() ,
		mean_time =  statistics['Time [ms]'].mean() ,
		min_time = statistics['Time [ms]'].min() ,
		max_time = statistics['Time [ms]'].max()
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
if __name__=="__main__":
	PORT = int(os.environ.get('PORT', 8000))
	uvicorn.run("main:app",host='0.0.0.0',port=PORT ,reload=True)