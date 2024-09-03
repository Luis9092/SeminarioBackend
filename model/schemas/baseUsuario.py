from pydantic import BaseModel

class baseUsuario():
    id: int
    nombres: str
    apellidos : str
    correo: str
    password:str
    fecha: str
    idrol: int
    menu: str
    
    