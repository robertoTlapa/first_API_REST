from fastapi import APIRouter
from models.request import usuarioRequest, usuarioUpdateRequest
from models.response import Response
from models.models import Usuario
from db.database import Database
from sqlalchemy import and_, desc
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import json
from jose import jwt, JWTError
from typing import Optional
from pydantic import BaseModel, Field
import datetime
from mongoengine import Document, StringField, DateTimeField, IntField, BooleanField
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, Query, status


router = APIRouter(
    prefix="/usuarios",
    tags=["usuario"],
    responses={404: {"description": "Error de base de datos"}},
)
#Autenticación 
crypt_context = CryptContext(schemes=["sha256_crypt", "md5_crypt"])

def get_password_hash(password):
    return crypt_context.hash(password)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

database = Database()
engine = database.get_db_connection()



# run the following on terminal to generate a secret key
# openssl rand -hex 32
SECRET_KEY = "3e8a3f31aab886f8793176988f8298c9265f84b8388c9fef93635b08951f379b"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_password(plain_password, hashed_password):
    return crypt_context.verify(plain_password, hashed_password)


def authenticate(username, password):
    try:
        user = get_user(username)
        password_check = verify_password(password, user['password'])
        return password_check
    except User.DoesNotExist:
        return False

class Token(BaseModel):
    access_token: str
    token_type: str

@router.post("/token" , response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    username = form_data.username
    password = form_data.password
    if authenticate(username, password):
        access_token = create_access_token(
            data={"sub": username}, expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
        return {"access_token": access_token, "token_type": "bearer"}
    else:
        raise HTTPException(
            status_code=400, detail="Incorrect username or password")


class TokenData(BaseModel):
    username: Optional[str] = None


def get_user(username: str):
    try:
        user = json.loads(User.objects.get(username=username).to_json())
        return user
    except User.DoesNotExist:
        return None


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    usuario = get_user(username=token_data.username)
    if usuario is None:
        raise credentials_exception
    return usuario

@router.get("/detail")
async def user_detail(current_user: Usuario = Depends(get_current_user)):
    return {"name": "Danny", "email": "danny@tutorialsbuddy.com"}


##Fin autentiicación 
@router.post("/add", response_description ="Usuario registrado en base de datos")
async def add_usuario(usuario_req: usuarioRequest):
    new_usuario = Usuario()
    new_usuario.username = usuario_req.username
    new_usuario.password = get_password_hash(usuario_req.password)
    session = database.get_db_session(engine)
    session.add(new_usuario)
    session.flush()
    session.refresh(new_usuario, attribute_names=['id'])
    data = {"user_id": new_usuario.id}
    session.commit()
    session.close()
    return Response(data, 200, "Usuario registrado con exito...", False)

@router.put("/update")
async def update_usuario(usuario_update_req: usuarioUpdateRequest):
    user_id = usuario_update_req.user_id
    session = database.get_db_session(engine)
    try:
        is_usuario_updated = session.query(Usuario).filter(Usuario.id == user_id).update({
            Usuario.username: usuario_update_req.username,
            Usuario.password:usuario_update_req.password,
        }, synchronize_session=False)
        session.flush()
        session.commit()
        response_msg = "Usuario actualizado con exito"
        response_code = 200
        error = False
        if is_usuario_updated == 1:
            data = session.query(Usuario).filter(
                Usuario.id == user_id).one()
        elif is_usuario_updated == 0:
            response_msg = "Usuario no actualizado, usuario con localizado id: " + srt(user_id)
            error= True
            data = None
            return Response(data, response_code, response_msg, error)
    except Exception as ex:
        print("Error: ", ex)
        
@router.delete("/{user_id}/delete")
async def delete_ususario(user_id: str):
    session = database.get_db_session(engine)
    try:
        is_usuario_updated = session.query(Usuario).filter(and_(Usuario.id == user_id, Usuario.delete == False)).update({
            Usuario.deleted: True}, synchronize_session=False)
        session.flush()
        session.commit()
        response_msg = "Usuario eliminado corectamente"
        response_code = 200
        error = False
        data = {"user_id": user_id}
        if is_usuario_updated == 0:
            response_msg = "Usuario no eliminado, no se localizo al usurio con id:  :" + \
                str(user_id)
            error = True
            data = None
        return Response(data, response_code, response_msg, error)
    except Exception as ex:
        print("Error : ", ex)
        
        
@router.get("/{user_id}")
async def read_usuario(user_id: str):
    session = database.get_db_session(engine)
    response_message = "Usuario localizado"
    data = None
    try:
        data = session.query(Usuario).filter(
            and_(Usuario.id == user_id)).one()
    except Exception as ex:
        print("Error", ex)
        response_message = "Usuario no localizado"
    error = False
    return Response(data, 200, response_message, error)

@router.get("/")
async def read_all_usuarios():
    session = database.get_db_session(engine)
    data = session.query(Usuario).all()
    return Response(data, 200, "Usuarios localizados con exito", False)