from pydantic import BaseModel

class BaseVenta(BaseModel):
    #Venta
    ClienteId: str
    FechaVenta: str
    Total: str

    #Detalle Venta
    DetalleId: str
    VentaId:str 
    ProductoId:str
    Cantidad:str
    PrecioUnitario:str
    EmpleadoId:str

