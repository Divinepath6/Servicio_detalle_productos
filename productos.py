import pyodbc
from flask import jsonify
from config import cadena_conexion

def obtener_producto_db(id):
    
    conexion = None

    try:
        conexion = pyodbc.connect(cadena_conexion)
        cursor = conexion.cursor()

        query = """
            SELECT
            p.Id, p.Codigo, p.Nombre, p.Descripcion, Stock, 
            PrecioCompra, PrecioVenta, p.FechaRegistro, p.Estado,
            c.Id as Categoriaint, c.nombre as categoria,
            pr.id as Proveedorint, pr.Nombre as proveedor, 
            u.id as UnidadMedidaint,u.Nombre as UnidadMedida
            FROM Productos as p 
            LEFT JOIN categorias c ON p.categoria = c.Id LEFT JOIN proveedores pr ON p.proveedor = pr.Id LEFT JOIN UnidadMedida u ON p.UnidadMedida = u.Id 
            WHERE p.Id = ?
        """
        cursor.execute(query, (id,))

        fila = cursor.fetchone()

        if not fila:
            return jsonify({"mensaje": "Producto no encontrado"}), 404
        
        producto = tuple(fila)
  
        producto = {
            'id': fila.Id,
            'codigo': fila.Codigo,
            'nombre': fila.Nombre,
            'descripcion': fila.Descripcion, 
            'categoria_id': fila.Categoriaint,
            'categoria': fila.categoria,
            'proveedor_id': fila.Proveedorint, 
            'proveedor': fila.proveedor,
            'stock': fila.Stock,
            'precio_compra': fila.PrecioCompra,
            'precio_venta': fila.PrecioVenta,
            'medida_id': fila.UnidadMedidaint,
            'medida': fila.UnidadMedida, 
            'fecha_registro': fila.FechaRegistro,
            'estado': fila.Estado,
        }
   
        return jsonify({
            "producto": producto
        }), 200
    except pyodbc.Error as e:
        print("ERROR SQL:", e)

        return jsonify({
            "error": str(e)
        }), 500

    finally:
        if conexion:
            conexion.close()

