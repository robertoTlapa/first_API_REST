from fastapi import APIRouter
from models.request import charlaRequest, charlaUpdateRequest
from models.response import Response
from models.models import Charla
from db.database import Database
from sqlalchemy import and_, desc, Date

router = APIRouter(
    prefix="/charlas",
    tags=["charla"],
    responses={404: {"description": "Error de base de datos"}},
)

database = Database()
engine = database.get_db_connection()

@router.post("/add", response_description ="charla registrado en la base de datos")
async def add_charla(charla_request: charlaRequest):
    new_charla = Charla()
    new_charla.evento_id = charla_request.evento_id
    new_charla.nombre_charla = charla_request.nombre_charla
    session = database.get_db_session(engine)
    session.add(new_charla)
    session.flush()
    session.refresh(new_charla, attribute_names=['id'])
    data = {"charla_id": new_charla.id}
    session.commit()
    session.close()
    return Response(data, 200, "charla registrado con exito", False)

@router.put("/update")
async def update_charla(charla_update_req: charlaUpdateRequest):
    charla_id = charla_update_req.charla_id
    session = database.get_db_session(engine)
    try:
        is_charla_update = session.query(Charla).filter(Charla.id == charla_id).update({
            Charla.evento_id: charla_update_req.evento_id,
            Charla.nombre_charla:charla_update_req.nombre_charla,
        }, synchronize_session=False)
        session.flush()
        session.commit()
        response_msg = "charla actualizado con exito"
        response_code = 200
        error = False
        if is_charla_update == 1:
            data = session.query(Charla).filter(
                Charla.id == charla_id).one()
        elif is_charla_update == 0:
            response_msg = "charla no actualizado, charla con localizado id: " + str(charla_id)
            error= True
            data = None
            return Response(data, response_code, response_msg, error)
    except Exception as ex:
        print("Error: ", ex)
        
@router.delete("/{charla_id}/delete")
async def delete_charla(charla_id: str):
    session = database.get_db_session(engine)
    try:
        is_charla_update = session.query(Charla).filter(and_(Charla.id == charla_id, Charla.deleted == False)).update({
            charla.deleted: True}, synchronize_session=False)
        session.flush()
        session.commit()
        response_msg = "charla eliminado corectamente"
        response_code = 200
        error = False
        data = {"charla_id": charla_id}
        if is_charla_update == 0:
            response_msg = "charla no eliminado, no se localizo al usurio con id:  :" + \
                str(charla_id)
            error = True
            data = None
        return Response(data, response_code, response_msg, error)
    except Exception as ex:
        print("Error : ", ex)
        
        
@router.get("/{charla_id}")
async def read_charla(charla_id: str):
    session = database.get_db_session(engine)
    response_message = "charla localizado"
    data = None
    try:
        data = session.query(Charla).filter(
            and_(Charla.id == charla_id)).one()
    except Exception as ex:
        print("Error", ex)
        response_message = "charla no localizado"
    error = False
    return Response(data, 200, response_message, error)

@router.get("/")
async def read_all_charlas():
    session = database.get_db_session(engine)
    data = session.query(Charla).all()
    return Response(data, 200, "charlas localizados con exito", False)