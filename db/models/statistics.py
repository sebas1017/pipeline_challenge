from sqlalchemy import Column, Integer, String, ForeignKey, Boolean,Float
from db.base_class import Base
class StatisticsCountries(Base):
    id = Column(Integer,primary_key=True,index=True)
    total_time = Column(Float)
    mean_time = Column(Float)
    min_time = Column(Float)
    max_time = Column(Float)



class Vehicles(Base):
    id = Column(Integer,primary_key=True,index=True)
    vehicle_id = Column(Integer)
    vehicle_label=Column(Integer)
    position_latitude=Column(Float)
    position_longitude=Column(Float)
    position_speed=Column(Integer)
    position_odometer=Column(Integer)
    trip_schedule_relationship=Column(Integer)
    trip_id=Column(Float)
    trip_route_id=Column(Float)




class Delegaciones(Base):
    id = Column(Integer,primary_key=True,index=True)
    delegacion = Column(String)
    nombre = Column(String)
    titulo = Column(String)
    codigo_postal_inicial = Column(String)
    codigo_postal_final = Column(String)