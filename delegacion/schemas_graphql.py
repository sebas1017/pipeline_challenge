import graphene
from graphene import String,Int
# from models import Post,User,Album
from db.models.statistics import Delegaciones
from graphene_sqlalchemy import SQLAlchemyObjectType
from graphene import relay

class DelegacionModel(SQLAlchemyObjectType):
    id = Int()
    class Meta:
        model = Delegaciones

