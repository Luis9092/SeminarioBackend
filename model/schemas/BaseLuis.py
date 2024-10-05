from pydantic import BaseModel


class BaseProductos(BaseModel):
    idproducto: int
    nombre: str
    descripcion: str
    precio: float
    cantidad: int
    proveedorid: int
    fechaingreso: str
    imagen: str
    idcategoria: int
    precioventa: float


class BaseCategoria(BaseModel):
    id: int
    categoria: str


class BaseProveedores(BaseModel):
    id: int
    nombre: str
    telefono: str
    email: str