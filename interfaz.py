import sys
import sqlite3
import pandas as pd
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QPushButton, QHBoxLayout, QLabel, QListWidget, QSplitter, QInputDialog
from PyQt6.QtCore import Qt

class PuntoDeVenta(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Punto de Venta")
        self.setGeometry(100, 100, 1000, 500)

        self.layout = QHBoxLayout()
        self.splitter = QSplitter(Qt.Orientation.Horizontal)

        # Tabla de productos
        self.tabla_productos = QTableWidget()
        self.tabla_productos.setColumnCount(4)
        self.tabla_productos.setHorizontalHeaderLabels(["Nombre", "Precio", "Stock", "Acción"])
        self.tabla_productos.setMinimumWidth(600)
        self.splitter.addWidget(self.tabla_productos)
        self.cargar_productos()

        # Panel derecho con carrito y botones
        self.panel_derecho = QVBoxLayout()

        # Carrito de compras
        self.carrito = []
        self.lista_carrito = QListWidget()
        self.lista_carrito.setMinimumWidth(300)
        self.panel_derecho.addWidget(self.lista_carrito)

        # Botón para eliminar del carrito
        self.btn_eliminar = QPushButton("Eliminar seleccionado")
        self.btn_eliminar.clicked.connect(self.eliminar_del_carrito)
        self.panel_derecho.addWidget(self.btn_eliminar)

        # Botón para procesar venta
        self.btn_procesar = QPushButton("Procesar Venta")
        self.btn_procesar.clicked.connect(self.procesar_venta)
        self.panel_derecho.addWidget(self.btn_procesar)

        # Botón para restock
        self.btn_restock = QPushButton("Restock de Productos")
        self.btn_restock.clicked.connect(self.restock_producto)
        self.panel_derecho.addWidget(self.btn_restock)

        # Botón para exportar ventas a Excel
        self.btn_exportar = QPushButton("Exportar Ventas a Excel")
        self.btn_exportar.clicked.connect(self.exportar_ventas_excel)
        self.panel_derecho.addWidget(self.btn_exportar)

        # Botón para limpiar el cache (eliminar ventas)
        self.btn_limpiar_cache = QPushButton("Limpiar Cache")
        self.btn_limpiar_cache.clicked.connect(self.limpiar_cache)
        self.panel_derecho.addWidget(self.btn_limpiar_cache)

        # Total
        self.total_label = QLabel("Total: $0.00")
        self.panel_derecho.addWidget(self.total_label)

        panel_widget = QWidget()
        panel_widget.setLayout(self.panel_derecho)
        self.splitter.addWidget(panel_widget)
        
        self.layout.addWidget(self.splitter)
        contenedor = QWidget()
        contenedor.setLayout(self.layout)
        self.setCentralWidget(contenedor)

    def limpiar_cache(self):
        """Función para limpiar el cache y eliminar todas las ventas registradas."""
        conexion = sqlite3.connect("pos.db")
        cursor = conexion.cursor()

        # Eliminar todas las ventas y el detalle de ventas
        cursor.execute("DELETE FROM detalle_ventas")
        cursor.execute("DELETE FROM ventas")

        conexion.commit()
        conexion.close()

        print("Todas las ventas han sido eliminadas.")

        # Refrescar la tabla de productos
        self.actualizar_tabla()

    def cargar_productos(self):
        conexion = sqlite3.connect("pos.db")
        cursor = conexion.cursor()
        cursor.execute("SELECT id, nombre, precio, stock FROM productos")
        productos = cursor.fetchall()
        conexion.close()

        self.tabla_productos.setRowCount(len(productos))

        for fila, producto in enumerate(productos):
            id_producto, nombre, precio, stock = producto
            self.tabla_productos.setItem(fila, 0, QTableWidgetItem(nombre))
            self.tabla_productos.setItem(fila, 1, QTableWidgetItem(str(precio)))
            self.tabla_productos.setItem(fila, 2, QTableWidgetItem(str(stock)))

            # Botón para agregar al carrito
            boton_agregar = QPushButton("Agregar")
            boton_agregar.clicked.connect(lambda _, p=producto: self.agregar_al_carrito(p))
            self.tabla_productos.setCellWidget(fila, 3, boton_agregar)

    def actualizar_tabla(self):
        """Refresca la tabla de productos después de una venta o restock."""
        self.tabla_productos.clearContents()
        self.cargar_productos()

    def agregar_al_carrito(self, producto):
        id_producto, nombre, precio, stock = producto
        if stock > 0:
            self.carrito.append((id_producto, nombre, precio))
            self.lista_carrito.addItem(f"{nombre} - ${precio}")
            self.actualizar_total()
        else:
            print("Producto sin stock")

    def eliminar_del_carrito(self):
        selected_item = self.lista_carrito.currentRow()
        if selected_item >= 0:
            self.carrito.pop(selected_item)
            self.lista_carrito.takeItem(selected_item)
            self.actualizar_total()

    def actualizar_total(self):
        total = sum(precio for _, _, precio in self.carrito)
        self.total_label.setText(f"Total: ${total:.2f}")

    def procesar_venta(self):
        if not self.carrito:
            print("No hay productos en el carrito")
            return

        conexion = sqlite3.connect("pos.db")
        cursor = conexion.cursor()

        # Insertar la venta en la tabla ventas
        total = sum(precio for _, _, precio in self.carrito)
        cursor.execute("INSERT INTO ventas (fecha, total) VALUES (datetime('now'), ?)", (total,))
        venta_id = cursor.lastrowid

        # Insertar los productos en detalle_ventas y actualizar stock
        for id_producto, _, precio in self.carrito:
            cursor.execute("INSERT INTO detalle_ventas (venta_id, producto_id, cantidad, subtotal) VALUES (?, ?, 1, ?)",
                           (venta_id, id_producto, precio))
            cursor.execute("UPDATE productos SET stock = stock - 1 WHERE id = ?", (id_producto,))

        conexion.commit()
        conexion.close()

        # Limpiar carrito y actualizar la tabla
        self.carrito.clear()
        self.lista_carrito.clear()
        self.actualizar_total()
        self.actualizar_tabla()
        print("Venta procesada correctamente")

    def restock_producto(self):
        """Permite al usuario seleccionar un producto y agregar stock."""
        conexion = sqlite3.connect("pos.db")
        cursor = conexion.cursor()
        cursor.execute("SELECT id, nombre FROM productos")
        productos = cursor.fetchall()
        conexion.close()

        if not productos:
            print("No hay productos disponibles.")
            return

        # Mostrar cuadro de diálogo para seleccionar producto
        items = [f"{p[0]} - {p[1]}" for p in productos]
        item, ok = QInputDialog.getItem(self, "Restock", "Selecciona un producto:", items, 0, False)

        if ok and item:
            id_producto = int(item.split(" - ")[0])  # Obtener el ID del producto
            cantidad, ok = QInputDialog.getInt(self, "Cantidad", "Ingrese la cantidad a añadir:", 1, 1, 100)

            if ok:
                conexion = sqlite3.connect("pos.db")
                cursor = conexion.cursor()
                cursor.execute("UPDATE productos SET stock = stock + ? WHERE id = ?", (cantidad, id_producto))
                conexion.commit()
                conexion.close()

                self.actualizar_tabla()
                print("Stock actualizado correctamente")

    def exportar_ventas_excel(self):
        conexion = sqlite3.connect("pos.db")

        try:
            query = """
            SELECT v.id AS Venta_ID, v.fecha AS Fecha, p.nombre AS Producto, 
                SUM(d.cantidad) AS Cantidad, SUM(d.subtotal) AS Subtotal
            FROM ventas v
            JOIN detalle_ventas d ON v.id = d.venta_id
            JOIN productos p ON d.producto_id = p.id
            GROUP BY v.id, p.id
            """
            df = pd.read_sql_query(query, conexion)

            if df.empty:
                print("No hay ventas para exportar.")
                return
            
            df.to_excel("ventas.xlsx", index=False)
            print("Ventas exportadas a ventas.xlsx con productos agrupados correctamente.")
        except Exception as e:
            print("Error al exportar:", e)
        finally:
            conexion.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = PuntoDeVenta()
    ventana.show()
    sys.exit(app.exec())