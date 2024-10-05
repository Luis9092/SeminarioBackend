from pydantic import BaseModel
from typing import List

class DetalleVenta(BaseModel):
    ProductoId: int
    Cantidad: int
    PrecioUnitario: float
    EmpleadoId: int

class Model_Venta(BaseModel):
    ClienteID: int
    FechaVenta: str  # Puedes usar datetime si deseas un formato más estricto
    Total: float
    Detalles: List[DetalleVenta]

