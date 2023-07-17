from fastapi import APIRouter
from models.request import confirmaEventoRequest, confirmaEventoUpdateRequest
from models.response import Response
from models.models import Confirma_Evento
from db.database import Database
from sqlalchemy import and_, desc

router = APIRouter(
    prefix="/confirma_eventos",
    tags=["confirma_evento"],
    responses={404: {"description": "Error de base de datos"}},
)

database = Database()
engine = database.get_db_connection()

@router.post("/add", response_description ="Confirma asistencia a evento")
async def add_user_id_evento(confirma_evento_req: confirmaEventoRequest):
    new_confirma_evento = Confirma_Evento()
    new_confirma_evento.evento_id = confirma_evento_req.evento_id
    new_confirma_evento.conformacion_id = confirma_evento_req.conformacion_id
    session = database.get_db_session(engine)
    session.add(new_confirma_evento)
    session.flush()
    session.refresh(new_confirma_evento, attribute_names=['id'])
    data = {"conformacion_id": new_confirma_evento.id}
    session.commit()
    session.close()
    return Response(data, 200, "Confirma_Evento registrado con exito...", False)

@router.put("/update")
async def update_user_id_evento(confirma_evento_update_req: confirmaEventoUpdateRequest):
    conformacion_id = confirma_evento_update_req.conformacion_id
    session = database.get_db_session(engine)
    try:
        is_confrimacion_evento_update = session.query(Confirma_Evento).filter(Confirma_Evento.id == conformacion_id).update({
            Confirma_Evento.evento_id: confirma_evento_update_req.evento_id,
            Confirma_Evento.user_id: confirma_evento_update_req.user_id,
        }, synchronize_session=False)
        session.flush()
        session.commit()
        response_msg = "Confirma_Evento actualizado con exito"
        response_code = 200
        error = False
        if is_confrimacion_evento_update == 1:
            data = session.query(Confirma_Evento).filter(
                Confirma_Evento.id == conformacion_id).one()
        elif is_confrimacion_evento_update == 0:
            response_msg = "Confirma_Evento no actualizado, Confirma_Evento con localizado id: " + srt(conformacion_id)
            error= True
            data = None
            return Response(data, response_code, response_msg, error)
    except Exception as ex:
        print("Error: ", ex)
        
@router.delete("/{evento_id}/delete")
async def delete_confirmacion_evento(evento_id: str):
    session = database.get_db_session(engine)
    try:
        is_confirmacion_charla_update = session.query(Evento).filter(and_(Evento.id == evento_id, Evento.deleted == False)).update({
            Evento.deleted: True}, synchronize_session=False)
        session.flush()
        session.commit()
        response_msg = "Evento eliminado corectamente"
        response_code = 200
        error = False
        data = {"evento_id": evento_id}
        if is_confirmacion_charla_update == 0:
            response_msg = "Evento no eliminado, no se localizo al usurio con id:  :" + \
                str(evento_id)
            error = True
            data = None
        return Response(data, response_code, response_msg, error)
    except Exception as ex:
        print("Error : ", ex)

@router.get("/{evento_id}")
async def read_confirmacion_evento(evento_id: str):
    session = database.get_db_session(engine)
    response_message = "Evento localizado"
    data = None
    try:
        data = session.query(Confirma_Evento).filter(
            and_(Confirma_Evento.id == evento_id)).one()
    except Exception as ex:
        print("Error", ex)
        response_message = "Evento no localizado"
    error = False
    return Response(data, 200, response_message, error)

@router.get("/")
async def read_all_Confirma_Eventos():
    session = database.get_db_session(engine)
    data = session.query(Confirma_Evento).all()
    return Response(data, 200, "Eventos localizados con exito", False)
        