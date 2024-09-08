from database.conexiondb import conexion
from starlette.status import (
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
    HTTP_200_OK,
)
import pyodbc



class Venta:
    def __init__(self) -> None:
        pass
    def VentasConstructor():
        pass

    def VentasConstructor(self, IdCliente, FechaVenta,Total):
        self.IdCliente = IdCliente
        self.FechaVenta = FechaVenta
        self.Total = Total 

    def InsertVenta(self):
        try:    
            Connection = conexion.cursor()
            query = "INSERT INTO Ventas(ClienteId, FechaVenta, Total)\
                        VALUES(?,?,?)"
            Connection.execute(
                query,
                (
                    self.IdCliente,
                    self.FechaVenta,
                    self.Total,
                ),
            )
            Connection.commit()
        except pyodbc.Error as ex:
            sqlstate = ex.args[1]
            print(f"Error en la ejecución del query: {sqlstate}")

    def MaestroVentas():
        pass

    #prueba de git