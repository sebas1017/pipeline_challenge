from sqlalchemy import Column, Integer, String, ForeignKey,Float
# from db.base_class import Base
from db.session import Base 

from sqlalchemy.orm import relationship

class DelegationsVehicles(Base):
    __tablename__ = 'delegaciones_vehicles'
    id = Column(Integer,primary_key=True,index=True)
    vehicle_id = Column(Integer)
    delegation_name = Column(String)
    delegation_id =   Column(Integer, ForeignKey("delegaciones.id",ondelete="CASCADE"))

class Vehicles(Base):
    __tablename__ = 'vehicles'
    id = Column(Integer,primary_key=True,index=True)
    vehicle_id = Column(Integer)
    vehicle_label=Column(Integer)
    vehicle_current_status=Column(Integer)
    position_latitude=Column(Float)
    position_longitude=Column(Float)
    position_speed=Column(Integer)
    position_odometer=Column(Integer)
    trip_schedule_relationship=Column(Integer)
    trip_id=Column(Float)
    trip_route_id=Column(Float)


class Delegaciones(Base):
    __tablename__ = 'delegaciones'
    id = Column(Integer,primary_key=True,index=True)
    delegacion = Column(String)
    nombre = Column(String)
    titulo = Column(String)
    codigo_postal_inicial = Column(String)
    codigo_postal_final = Column(String)