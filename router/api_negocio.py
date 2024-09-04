from fastapi import APIRouter, Response
from typing import List
from database import conexiondb
from model.schemas import baseUsuario
from starlette.status import (
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
)
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from model.usuarios import Usuario

api = APIRouter()
user = Usuario()


@api.get("/")
def root():
    seleccionar = conexiondb.conexion.cursor()
    resultado = seleccionar.execute("select * from role;")
    r = resultado.fetchall()
    print(r)

    return {"Iniciando": "Bienvenido"}


@api.post("/crearUsuario")
def crearUsuario(listau: baseUsuario.baseUser):
    tiempo = datetime.now()
    horaActual = tiempo.strftime("%d/%m/%Y %H:%M:%S")
    contra = generate_password_hash(listau.password, "pbkdf2:sha256:30", 30)
    user.constructorUsuario(
        0, listau.nombres, listau.apellidos, listau.correo, contra, horaActual, 2
    )

    verificar = user.verificarSiexiste()
    if verificar != HTTP_200_OK:
        retorno = user.crearUsuario()
    else:
        retorno = HTTP_400_BAD_REQUEST

    return Response(status_code=retorno)


@api.get("/autenticarUsuario/<correo><pasw>", response_model=baseUsuario.baseUser)
def autenticarUsuario(correo: str, pasw: str):

    retorno1 = user.autenticarUsuario(correo, pasw)
    if retorno1 != HTTP_400_BAD_REQUEST:
        return retorno1
    else:
        return Response(status_code=HTTP_400_BAD_REQUEST)
