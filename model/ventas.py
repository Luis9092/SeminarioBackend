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
        self.detalles = []  # Inicializamos los detalles de la venta como una lista vacía

    def constructorVenta(self, cliente_id, fecha_venta, total, detalles):
        self.cliente_id = cliente_id
        self.fecha_venta = fecha_venta
        self.total = total
        self.detalles = detalles  # Asignamos los detalles al atributo de la clase

    def crearVenta(self):
        cn = conexion.cursor()
        
        # Inserción de la venta principal
        query = "INSERT INTO Ventas(ClienteID, FechaVenta, Total) OUTPUT INSERTED.VentaID VALUES (?, ?, ?)"
        cn.execute(query, (self.cliente_id, self.fecha_venta, self.total))
        
        # Obtener el ID de la venta recién creada
        venta_id = cn.fetchone()[0]
        
        # Insertar los detalles de la venta
        for detalle in self.detalles:
            query_detalle = "INSERT INTO DetallesVenta(VentaId, ProductoId, Cantidad, PrecioUnitario, EmpleadoId) VALUES (?, ?, ?, ?, ?)"
            cn.execute(
                query_detalle,
                (
                    venta_id,
                    detalle.ProductoId,  # Accedemos a los atributos del objeto detalle
                    detalle.Cantidad,
                    detalle.PrecioUnitario,
                    detalle.EmpleadoId,
                ),
            )
    
        conexion.commit()
        return venta_id  # Retorna el ID de la venta recién creada

    def obtenerVentaPorId(self, venta_id):
        cn = conexion.cursor()

        # Obtener la venta con el ID proporcionado
        query_venta = "SELECT VentaId, ClienteID, FechaVenta, Total FROM ventas WHERE VentaId = ?"
        cn.execute(query_venta, (venta_id,))
        venta = cn.fetchone()

        if not venta:
            return None  # Si no encuentra la venta, retorna None

        # Obtener los detalles de la venta
        query_detalles = """SELECT ProductoId, Cantidad, PrecioUnitario, EmpleadoId 
                            FROM DetallesVenta WHERE VentaId = ?"""
        cn.execute(query_detalles, (venta_id,))
        detalles = cn.fetchall()

        # Retornar la venta y sus detalles
        return {
            "VentaId": venta[0],
            "ClienteID": venta[1],
            "FechaVenta": venta[2],
            "Total": venta[3],
            "Detalles": [
                {
                    "ProductoId": detalle[0],
                    "Cantidad": detalle[1],
                    "PrecioUnitario": detalle[2],
                    "EmpleadoId": detalle[3]
                }
                for detalle in detalles
            ]
        }
    
    def eliminarVenta(self, venta_id):
        cn = conexion.cursor()

        try:
            # Eliminar los detalles de la venta primero
            query_detalle = "DELETE FROM DetallesVenta WHERE VentaId = ?"
            cn.execute(query_detalle, (venta_id,))
            
            # Luego eliminar la venta principal
            query_venta = "DELETE FROM Ventas WHERE VentaId = ?"
            cn.execute(query_venta, (venta_id,))
            
            conexion.commit()  # Hacemos commit de la transacción

            return {"message": "Venta y detalles eliminados con éxito", "VentaID": venta_id}

        except Exception as e:
            conexion.rollback()  # En caso de error, deshacer cambios
            return {"error": str(e), "message": "Error al eliminar la venta"}
        


    def actualizarVenta(self, venta_id, cliente_id, fecha_venta, total, detalles):
        cn = conexion.cursor()
        try:
            # Actualizar la venta principal
            query = "UPDATE Ventas SET ClienteID = ?, FechaVenta = ?, Total = ? WHERE VentaId = ?"
            cn.execute(query, (cliente_id, fecha_venta, total, venta_id))

            # Eliminar los detalles actuales de la venta
            query_eliminar_detalles = "DELETE FROM DetallesVenta WHERE VentaId = ?"
            cn.execute(query_eliminar_detalles, (venta_id,))

            # Insertar los nuevos detalles de la venta
            for detalle in detalles:
                query_insertar_detalle = """
                    INSERT INTO DetallesVenta (VentaId, ProductoId, Cantidad, PrecioUnitario, EmpleadoId) 
                    VALUES (?, ?, ?, ?, ?)
                """
                cn.execute(
                    query_insertar_detalle,
                    (
                        venta_id,
                        detalle['ProductoId'],
                        detalle['Cantidad'],
                        detalle['PrecioUnitario'],
                        detalle['EmpleadoId'],
                    ),
                )

            conexion.commit()
            return {"message": "Venta actualizada con éxito"}

        except Exception as e:
            conexion.rollback()  # Deshacer cambios en caso de error
            return {"message": f"Error al actualizar la venta: {str(e)}"}
