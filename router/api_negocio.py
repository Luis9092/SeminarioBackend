from fastapi import APIRouter, Response, HTTPException
from pydantic import BaseModel
from typing import List
from database import conexiondb
from model.schemas import baseUsuario, BaseVentas
from starlette.status import (
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
    HTTP_422_UNPROCESSABLE_ENTITY
)
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from model.usuarios import Usuario
from model.ventas import Venta

api = APIRouter()
user = Usuario()
venta = Venta()

role_map = {
    1: "SuperAdmin",
    2: "Administrador",
    3: "Empleado",
    4: "Auditor"
}

reverse_role_map = {
    "SuperAdmin": 1,
    "Administrador": 2,
    "Empleado": 3,
    "Auditor": 4
}

class BaseUsuario(BaseModel):
    UsuarioID: int
    nombres: str
    fechacreacion: str
    rol: str

    class Config:
        orm_mode = True

class Rol(BaseModel):
    nombre: str
    
class RolUpdate(BaseModel):
    nuevo_rol: str

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
        0, listau.nombres, listau.apellidos, listau.correo, contra, horaActual, 3
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


# ------- SELLS SECTIONS IS BEING DEVELOPED HERE -start- ------- #

@api.post("/HacerVenta/<ClienteId><FechaVenta><Total>", response_model=BaseVentas.BaseVenta)
def InsertVenta(ClienteId:str, Total:str):
    Date = datetime.now()
    CurrentDate = Date.strftime("%d/%m/%Y %H:%M:%S")
    venta.VentasConstructor(ClienteId, CurrentDate, Total)
    venta.InsertVenta()

# ------- SELLS SECTIONS IS BEING DEVELOPED HERE -finish- ------- #

@api.get("/usuarios", response_model=List[BaseUsuario])
def obtener_usuarios():
    seleccionar = conexiondb.conexion.cursor()
    resultado = seleccionar.execute("SELECT UsuarioID, nombres, fechacreacion, rol FROM Login;")
    usuarios = resultado.fetchall()

    if usuarios:
        lista_usuarios = [
            {
                "UsuarioID": usuario[0],
                "nombres": usuario[1],
                "fechacreacion": usuario[2],
                "rol": role_map.get(usuario[3], "Desconocido")
            }
            for usuario in usuarios
        ]
        return lista_usuarios
    else:
        return Response(status_code=HTTP_204_NO_CONTENT)
    
# -------------------------------------------------------------------------# 

@api.get("/roles", response_model=List[dict])
async def obtener_roles():
    # Suponiendo que tus roles están en la base de datos
    roles = [
        {"id": 1, "nombre": "SuperAdmin"},
        {"id": 2, "nombre": "Administrador"},
        {"id": 3, "nombre": "Empleado"},
        {"id": 4, "nombre": "Auditor"}
    ]
    return roles
# -------------------------------------------------------------------------------------- #
    
@api.put("/usuarios/{usuario_id}/rol", response_model=BaseUsuario)
def actualizar_rol(usuario_id: int, rol_update: RolUpdate):
    nuevo_rol = rol_update.nuevo_rol  # Obtener el nuevo rol del cuerpo
    print(f"Rol recibido: {nuevo_rol}")  # Imprimir el rol recibido

    # Convertir el nuevo rol a su valor numérico
    rol_numero = reverse_role_map.get(nuevo_rol)
    if not rol_numero:
        raise HTTPException(status_code=HTTP_422_UNPROCESSABLE_ENTITY, detail="Rol inválido.")

    # Actualizar el rol en la base de datos
    actualizar = conexiondb.conexion.cursor()
    actualizar.execute("UPDATE Login SET rol = ? WHERE UsuarioID = ?", (rol_numero, usuario_id))
    conexiondb.conexion.commit()

    # Obtener los detalles actualizados del usuario
    resultado = actualizar.execute("SELECT UsuarioID, nombres, fechacreacion, rol FROM Login WHERE UsuarioID = ?", (usuario_id,))
    usuario_actualizado = resultado.fetchone()

    if usuario_actualizado:
        return {
            "UsuarioID": usuario_actualizado[0],
            "nombres": usuario_actualizado[1],
            "fechacreacion": usuario_actualizado[2],
            "rol": role_map.get(usuario_actualizado[3], "Desconocido")
        }
    else:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Usuario no encontrado.")


# -------------------------------------------------------------------------# 

@api.delete("/usuarios/{usuario_id}")
def eliminar_usuario(usuario_id: int):
    eliminar = conexiondb.conexion.cursor()
    eliminar.execute("DELETE FROM Login WHERE UsuarioID = ?", (usuario_id,))
    conexiondb.conexion.commit()

    return {"message": f"Usuario {usuario_id} eliminado correctamente"}


