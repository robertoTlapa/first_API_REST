from fastapi import APIRouter
from models.request import eventoRequest, eventoUpdateRequest
from models.response import Response
from models.models import Evento
from db.database import Database
from sqlalchemy import and_, desc, Date

router = APIRouter(
    prefix="/eventos",
    tags=["evento"],
    responses={404: {"description": "Error de base de datos"}},
)

database = Database()
engine = database.get_db_connection()

@router.post("/add", response_description ="Evento registrado en la base de datos")
async def add_evento(evento_request: eventoRequest):
    new_evento = Evento()
    new_evento.nombre = evento_request.nombre
    new_evento.fecha = evento_request.fecha
    session = database.get_db_session(engine)
    session.add(new_evento)
    session.flush()
    session.refresh(new_evento, attribute_names=['id'])
    data = {"evento_id": new_evento.id}
    session.commit()
    session.close()
    return Response(data, 200, "Evento registrado con exito", False)

@router.put("/update")
async def update_Evento(evento_update_req: eventoUpdateRequest):
    evento_id = evento_update_req.evento_id
    session = database.get_db_session(engine)
    try:
        is_evento_update = session.query(Evento).filter(Evento.id == evento_id).update({
            Evento.nombre: evento_update_req.nombre,
            Evento.fecha:evento_update_req.fecha,
        }, synchronize_session=False)
        session.flush()
        session.commit()
        response_msg = "Evento actualizado con exito"
        response_code = 200
        error = False
        if is_evento_update == 1:
            data = session.query(Evento).filter(
                Evento.id == evento_id).one()
        elif is_evento_update == 0:
            response_msg = "Evento no actualizado, Evento con localizado id: " + srt(evento_id)
            error= True
            data = None
            return Response(data, response_code, response_msg, error)
    except Exception as ex:
        print("Error: ", ex)
        
@router.delete("/{evento_id}/delete")
async def delete_evento(evento_id: str):
    session = database.get_db_session(engine)
    try:
        is_evento_update = session.query(Evento).filter(and_(Evento.id == evento_id, Evento.deleted == False)).update({
            Evento.deleted: True}, synchronize_session=False)
        session.flush()
        session.commit()
        response_msg = "Evento eliminado corectamente"
        response_code = 200
        error = False
        data = {"evento_id": evento_id}
        if is_evento_update == 0:
            response_msg = "Evento no eliminado, no se localizo al usurio con id:  :" + \
                str(evento_id)
            error = True
            data = None
        return Response(data, response_code, response_msg, error)
    except Exception as ex:
        print("Error : ", ex)
        
        
@router.get("/{evento_id}")
async def read_Evento(evento_id: str):
    session = database.get_db_session(engine)
    response_message = "Evento localizado"
    data = None
    try:
        data = session.query(Evento).filter(
            and_(Evento.id == evento_id)).one()
    except Exception as ex:
        print("Error", ex)
        response_message = "Evento no localizado"
    error = False
    return Response(data, 200, response_message, error)

@router.get("/")
async def read_all_Eventos():
    session = database.get_db_session(engine)
    data = session.query(Evento).all()
    return Response(data, 200, "Eventos localizados con exito", False)