from fastapi import APIRouter, Response

api =APIRouter()


@api.get("/")
def root():
    return {"Iniciando": "Bienvenido"}