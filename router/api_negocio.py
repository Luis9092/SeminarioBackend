from fastapi import APIRouter, Response
from typing import List
from database import conexiondb
api =APIRouter()


@api.get("/")
def root():
    seleccionar = conexiondb.conexion.cursor()
    resultado = seleccionar.execute("select * from role;")
    r = resultado.fetchall()
    print(r)

    return {"Iniciando": "Bienvenido"}

@api.post("/crearusuario")
def crearusuario():
    pass
    