from sqlalchemy import Column, INTEGER, String, Date, BOOLEAN, text
from sqlalchemy.ext.declarative import declarative_base



Base = declarative_base()

class Usuario(Base):
    __tablename__ = "usuarios"
    id = Column(INTEGER, primary_key= True)
    username = Column(String(50), nullable = False)
    password = Column(String(20), nullable = False)
    

    
class Evento(Base):
    __tablename__ = "eventos"
    id = Column(INTEGER, primary_key = True)
    nombre = Column(String(150), nullable = False)
    fecha = Column(String, nullable = True)
    
class Charla(Base):
    __tablename__ = "charlas"
    id = Column(INTEGER, primary_key = True)
    evento_id = Column(INTEGER, nullable = False)
    nombre_charla = Column(String(150), nullable = False)
    
class Confirma_Charla(Base):
    __tablename__ = "asistencia_charlas"
    id = Column(INTEGER, primary_key = True)
    charla_id = Column(INTEGER, nullable = False)
    confirmacion = Column(BOOLEAN, nullable = True)
    user_id = Column(INTEGER, nullable = False)
    
class Confirma_Evento(Base):
    __tablename__ = "asistencia_eventos"
    id = Column(INTEGER, primary_key = True)
    evento_id = Column(INTEGER, nullable = False)
    user_id = Column(INTEGER, nullable =False)
    