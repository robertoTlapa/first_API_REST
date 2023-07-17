from fastapi import APIRouter
from models.request import confirmaCharlaRequest, confirmaCharlaUpdateRequest
from models.response import Response
from models.models import Confirma_Charla
from db.database import Database
from sqlalchemy import and_, desc

router = APIRouter(
    prefix="/confirma_charlas",
    tags=["confirma_charla"],
    responses={404: {"description": "Error de base de datos"}},
)

database = Database()
engine = database.get_db_connection()

@router.post("/add", response_description ="Confirmar asistencia a charla")
async def add_confirmacion_charla(confirma_charla_req: confirmaCharlaRequest):
    new_confirma_charla = Confirma_Charla()
    new_confirma_charla.charla_id = confirma_charla_req.charla_id
    new_confirma_charla.confirmacion = confirma_charla_req.confirmacion
    new_confirma_charla.user_id = confirma_charla_req.user_id
    session = database.get_db_session(engine)
    session.add(new_confirma_charla)
    session.flush()
    session.refresh(new_confirma_charla, attribute_names=['id'])
    data = {"user_id": new_confirma_charla.id}
    session.commit()
    session.close()
    return Response(data, 200, "Confirma_Charla registrado con exito...", False)

@router.put("/update")
async def update_confirmacion_evento(confirma_charla_Update_req: confirmaCharlaUpdateRequest):
    conformacion_id = confirma_charla_Update_req.conformacion_id
    session = database.get_db_session(engine)
    try:
        is_confirmacion_charla_update = session.query(Confirma_Charla).filter(Confirma_Charla.id == user_id).update({
            Confirma_Charla.charla_id: confirma_charla_Update_req.charla_id,
            Confirma_Charla.confirmacion: confirma_charla_Update_req.confirmacion,
            confirma_charla.user_id: confirma_charla_Update_req.user_id,
        }, synchronize_session=False)
        session.flush()
        session.commit()
        response_msg = "Confirma_Charla actualizado con exito"
        response_code = 200
        error = False
        if is_confirmacion_charla_update == 1:
            data = session.query(Confirma_Charla).filter(
                Confirma_Charla.id == conformacion_id).one()
        elif is_confirmacion_charla_update == 0:
            response_msg = "Confirma_Charla no actualizado, Confirma_Charla con localizado id: " + srt(user_id)
            error= True
            data = None
            return Response(data, response_code, response_msg, error)
    except Exception as ex:
        print("Error: ", ex)
        
@router.delete("/{charla_id}/delete")
async def delete_confirmacion_evento(charla_id: str):
    session = database.get_db_session(engine)
    try:
        is_confirmacion_charla_update = session.query(Evento).filter(and_(Evento.id == charla_id, Evento.deleted == False)).update({
            Evento.deleted: True}, synchronize_session=False)
        session.flush()
        session.commit()
        response_msg = "Evento eliminado corectamente"
        response_code = 200
        error = False
        data = {"charla_id": charla_id}
        if is_confirmacion_charla_update == 0:
            response_msg = "Evento no eliminado, no se localizo al usurio con id:  :" + \
                str(charla_id)
            error = True
            data = None
        return Response(data, response_code, response_msg, error)
    except Exception as ex:
        print("Error : ", ex)

@router.get("/{charla_id}")
async def read_confirmacion_evento(charla_id: str):
    session = database.get_db_session(engine)
    response_message = "Evento localizado"
    data = None
    try:
        data = session.query(Evento).filter(
            and_(Confirma_Charla.id == charla_id)).one()
    except Exception as ex:
        print("Error", ex)
        response_message = "Evento no localizado"
    error = False
    return Response(data, 200, response_message, error)

@router.get("/")
async def read_all_Confrima_Charlas():
    session = database.get_db_session(engine)
    data = session.query(Confirma_Charla).all()
    return Response(data, 200, "Eventos localizados con exito", False)