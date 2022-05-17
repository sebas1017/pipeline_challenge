from fastapi import FastAPI
from core.config import settings
from db.session import  engine 
from db.session import Base  
from delegacion.routers import delegacion, vehiculos
import os
import uvicorn
from starlette.graphql import GraphQLApp
import graphene
from delegacion.repository import graphql


def create_tables():           
	Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.PROJECT_NAME,version=settings.PROJECT_VERSION)

create_tables()      
		
app.include_router(delegacion.router)
app.include_router(vehiculos.router)
app.add_route(
    "/graphql",
    GraphQLApp(
        schema=graphene.Schema(
            query=graphql.Query),
        graphiql=True))


if __name__=="__main__":
	PORT = int(os.environ.get('PORT', 8000))
	uvicorn.run("main:app",host='0.0.0.0',port=PORT ,reload=True)