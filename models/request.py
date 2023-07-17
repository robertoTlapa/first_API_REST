from pydantic import BaseModel, EmailStr, Field
from typing import Optional
#Request Usuarios--------------------------------------------
class usuarioRequest(BaseModel):
    username: str = Field(
        None, title = "Nombre de usuario", max_length=100
    )
    password: str = Field(
        None, title = "Password del usuario", max_length = 100       
    )
    
class usuarioUpdateRequest(BaseModel):
    user_id: int
    username: str = Field(
        None, title = "Nombre de usuario", max_length=100
    )
    password: str = Field(
        None, title = "Password del usuario", max_length = 100       
    )
    
    
    #Request Eventos-------------------------------------------
class eventoRequest(BaseModel):
    nombre: str = Field(
        None, title = "Nombre de evento", max_length=100
    )
    fecha: str = Field(
        None, title = "Fecha del evento", max_length = 100       
    )
    
class eventoUpdateRequest(BaseModel):
    evento_id: int
    nombre: str = Field(
        None, title = "Nombre de evento", max_length=100
    )
    fecha: str = Field(
        None, title = "Fecha del evento", max_length = 100       
    )
    
    #Request Charlas---------------------------------
    
class charlaRequest(BaseModel):
    evento_id: int
    nombre_charla: str = Field(
        None, title = "Nombre de la Charla", max_length = 100       
    )
    
class charlaUpdateRequest(BaseModel):
    charla_id: int
    evento_id: int
    nombre_charla: str = Field(
        None, title = "Nombre de la charla", max_length=100
    )
    #Request Asistencia_charlas-------------------------
    
class confirmaCharlaRequest(BaseModel):
    charla_id: int
    confirmacion: int
    user_id: int 
    
class confirmaCharlaUpdateRequest(BaseModel):
    id_confirmacion: int
    charla_id: int
    confirmacion: int
    user_id: int 
    
    #Request Asistencia_eventos-------------------------
    
class confirmaEventoRequest(BaseModel):
    evento_id: int
    user_id: int
    
class confirmaEventoUpdateRequest(BaseModel):
    id_conformacion: int
    evento_id: int
    user_id: int