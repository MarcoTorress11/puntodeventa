import sqlite3

conexion = sqlite3.connect("pos.db")
cursor = conexion.cursor()
    
    # Crear tabla de productos
cursor.execute('''CREATE TABLE IF NOT EXISTS productos (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nombre TEXT NOT NULL,
                        precio REAL NOT NULL,
                        stock INTEGER NOT NULL)''')

    # Crear tabla de ventas
cursor.execute('''CREATE TABLE IF NOT EXISTS ventas (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        fecha TEXT NOT NULL,
                        total REAL NOT NULL)''')

    # Crear tabla de detalle de ventas
cursor.execute('''CREATE TABLE IF NOT EXISTS detalle_ventas (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        venta_id INTEGER NOT NULL,
                        producto_id INTEGER NOT NULL,
                        cantidad INTEGER NOT NULL,
                        subtotal REAL NOT NULL,
                        FOREIGN KEY (venta_id) REFERENCES ventas(id),
                        FOREIGN KEY (producto_id) REFERENCES productos(id))''')

conexion.commit()
conexion.close()
print("Base de datos creada correctamente.")

