import sqlite3

conexion = sqlite3.connect("pos.db")
cursor = conexion.cursor()

#Una vez agregados los productos se pueden borrar de este código y si en un futuro es necesario agregar más solo se agrega el nuevo producto

productos = [
        ("Laptop HP", 15000.00, 5),
        ("Mouse Logitech", 500.00, 20),
        ("Teclado mecánico", 1200.00, 15),
        ("Monitor Samsung 24", 4000.00, 10),
        ("Auriculares Gamer", 2500.00, 8),
        ("Smartphone Samsung", 12000.00, 6),
        ("Impresora HP", 3000.00, 7),
        ("Tablet Lenovo", 7500.00, 5),
        ("Disco Duro 1TB", 2000.00, 12),
        ("Memoria USB 64GB", 300.00, 25),
        ("Camiseta Nike", 600.00, 30),
        ("Pantalón Levis", 1200.00, 20),
        ("Zapatillas Adidas", 1800.00, 15),
        ("Sudadera Puma", 1500.00, 18),
        ("Reloj Casio", 800.00, 10),
        ("Gorra New Era", 500.00, 25),
        ("Mochila Jansport", 1300.00, 10),
        ("Lentes de sol Ray-Ban", 2500.00, 7),
        ("Cinturón de cuero", 700.00, 12),
        ("Chaqueta de cuero", 3500.00, 5),
        ("Producto nuevo", 113500.00, 5000)
    ]

cursor.executemany("INSERT INTO productos (nombre, precio, stock) VALUES (?, ?, ?)", productos)
    
conexion.commit()
conexion.close()
print("Productos agregados correctamente.")
