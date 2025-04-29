import sys
import sqlite3
import pandas as pd
from PyQt6.QtWidgets import QApplication, QMessageBox, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QPushButton, QHBoxLayout, QLabel, QListWidget, QSplitter, QInputDialog, QLineEdit, QMessageBox, QDialog, QTextEdit
from PyQt6.QtCore import Qt
from datetime import datetime

class TicketDialog(QDialog):
    def __init__(self, ticket_text, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Ticket de Venta")
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()

            # Área de texto para el ticket
        self.ticket_display = QTextEdit()
        self.ticket_display.setReadOnly(True)
        self.ticket_display.setPlainText(ticket_text)
        layout.addWidget(self.ticket_display)

            # Botón para cerrar la ventana
        self.btn_cerrar = QPushButton("Cerrar")
        self.btn_cerrar.clicked.connect(self.accept)
        self.btn_cerrar.setStyleSheet("background-color: #3498DB; color: white; font-weight: bold; border-radius: 5px; padding: 5px;")
        layout.addWidget(self.btn_cerrar)

        self.setLayout(layout)


class PuntoDeVenta(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Punto de Venta")
        self.setGeometry(100, 100, 1000, 500)

        self.layout = QHBoxLayout()
        self.splitter = QSplitter(Qt.Orientation.Horizontal)

        # Panel izquierdo de búsqueda y tabla de productos
        self.panel_izquierdo = QVBoxLayout()

        # Campo de búsqueda con PLU
        self.busqueda_layout = QHBoxLayout()
        self.input_plu = QLineEdit()
        self.input_plu.setPlaceholderText("Escanee o ingrese PLU (12 dígitos)")
        self.input_plu.returnPressed.connect(self.buscar_por_plu)  # Procesar al presionar Enter
        self.input_plu.setFocus() 
        self.busqueda_layout.addWidget(self.input_plu)

        self.btn_buscar = QPushButton("Buscar")
        self.btn_buscar.clicked.connect(self.buscar_por_plu)  
        self.busqueda_layout.addWidget(self.btn_buscar)
        self.btn_buscar.setStyleSheet("background-color: #3498DB; color: white; font-weight: bold; border-radius: 5px; padding: 5px;")

        self.panel_izquierdo.addLayout(self.busqueda_layout)

        # Tabla de productos
        self.tabla_productos = QTableWidget()
        self.tabla_productos.setColumnCount(5)
        self.tabla_productos.setHorizontalHeaderLabels(["PLU", "Nombre", "Precio", "Stock", "Acción"])
        self.tabla_productos.setMinimumWidth(600)
        self.panel_izquierdo.addWidget(self.tabla_productos)
        self.cargar_productos()

        panel_izquierdo_widget = QWidget()
        panel_izquierdo_widget.setLayout(self.panel_izquierdo)
        self.splitter.addWidget(panel_izquierdo_widget)

        # Panel derecho con carrito y botones
        self.panel_derecho = QVBoxLayout()

        # Carrito de compras
        self.carrito = []
        self.lista_carrito = QListWidget()
        self.lista_carrito.setMinimumWidth(300)
        self.panel_derecho.addWidget(self.lista_carrito)

        # Botón para procesar venta
        self.btn_procesar = QPushButton("Procesar Venta")
        self.btn_procesar.clicked.connect(self.procesar_venta)
        self.panel_derecho.addWidget(self.btn_procesar)
        self.btn_procesar.setStyleSheet("background-color: #2E86C1; color: white; font-weight: bold; border-radius: 10px; padding: 5px;")

        # Botón para eliminar del carrito
        self.btn_eliminar_carrito = QPushButton("Eliminar seleccionado")
        self.btn_eliminar_carrito.clicked.connect(self.eliminar_del_carrito)
        self.panel_derecho.addWidget(self.btn_eliminar_carrito)
        self.btn_eliminar_carrito.setStyleSheet("background-color: #CD5C5C; color: white; font-weight: bold; border-radius: 10px; padding: 5px;")

        # Botón para restock
        self.btn_restock = QPushButton("Restock de Productos")
        self.btn_restock.clicked.connect(self.restock_producto)
        self.panel_derecho.addWidget(self.btn_restock)
        self.btn_restock.setStyleSheet("background-color: #F39C12; color: white; font-weight: bold; border-radius: 10px; padding: 5px;")

        # Botón para agregar nuevos productos
        self.btn_agregar_producto = QPushButton("Agregar Producto Nuevo")
        self.btn_agregar_producto.clicked.connect(self.agregar_producto)
        self.panel_derecho.addWidget(self.btn_agregar_producto)
        self.btn_agregar_producto.setStyleSheet("background-color: #ADD8E6; color: white; font-weight: bold; border-radius: 10px; padding: 5px;")

        # Botón para exportar ventas a Excel
        self.btn_exportar = QPushButton("Exportar Ventas a Excel")
        self.btn_exportar.clicked.connect(self.exportar_ventas_excel)
        self.panel_derecho.addWidget(self.btn_exportar)
        self.btn_exportar.setStyleSheet("background-color: #27AE60; color: white; font-weight: bold; border-radius: 10px; padding: 5px;")

        # Botón para eliminar producto
        self.btn_eliminar_producto = QPushButton("Eliminar producto")
        self.btn_eliminar_producto.clicked.connect(self.eliminar_producto)
        self.panel_derecho.addWidget(self.btn_eliminar_producto)
        self.btn_eliminar_producto.setStyleSheet("background-color: #B03A2E; color: white; font-weight: bold; border-radius: 10px; padding: 5px;")

        # Botón para limpiar el caché (eliminar ventas)
        self.btn_limpiar_cache = QPushButton("Limpiar Caché")
        self.btn_limpiar_cache.clicked.connect(self.limpiar_cache)
        self.panel_derecho.addWidget(self.btn_limpiar_cache)
        self.btn_limpiar_cache.setStyleSheet("background-color: grey; color: white; font-weight: bold; border-radius: 10px; padding: 5px;")

        # Total
        self.total_label = QLabel("Total: $0.00")
        self.panel_derecho.addWidget(self.total_label)

        panel_derecho_widget = QWidget()
        panel_derecho_widget.setLayout(self.panel_derecho)
        self.splitter.addWidget(panel_derecho_widget)

        self.layout.addWidget(self.splitter)
        contenedor = QWidget()
        contenedor.setLayout(self.layout)
        self.setCentralWidget(contenedor)

    def limpiar_cache(self):
        """Función para limpiar el caché y eliminar todas las ventas registradas."""
        conexion = sqlite3.connect("pos.db")
        cursor = conexion.cursor()

        # Eliminar todas las ventas y el detalle de ventas
        cursor.execute("DELETE FROM detalle_ventas")
        cursor.execute("DELETE FROM ventas")

        conexion.commit()
        conexion.close()

        QMessageBox.information(self, "Caché limpiado", "Todas las ventas han sido eliminadas.")
        self.actualizar_tabla()

    def agregar_producto(self):
        plu, ok = QInputDialog.getText(self, "Agregar Producto", "PLU del producto:")
        if not ok or not plu.strip():
            return

        nombre, ok = QInputDialog.getText(self, "Agregar Producto", "Nombre del producto:")
        if not ok or not nombre.strip():
            return

        precio, ok = QInputDialog.getDouble(self, "Agregar Producto", "Precio del producto:", decimals=2)
        if not ok:
            return

        stock, ok = QInputDialog.getInt(self, "Agregar Producto", "Cantidad en stock:", 1, 1, 1000)
        if not ok:
            return

        conexion = sqlite3.connect("pos.db")
        cursor = conexion.cursor()
        cursor.execute("INSERT INTO productos (plu, nombre, precio, stock) VALUES (?, ?, ?, ?)", (plu.strip(), nombre.strip(), precio, stock))
        conexion.commit()
        conexion.close()

        self.actualizar_tabla()
        print(f"Producto '{nombre}' agregado correctamente con PLU {plu}.")


    def buscar_por_plu(self):
            plu = self.input_plu.text().strip()
            print(f"PLU recibido: '{plu}'")  
            if len(plu) == 12 and plu.isdigit():  # Validar 12 numeros
                conexion = sqlite3.connect("pos.db")
                cursor = conexion.cursor()
                cursor.execute("SELECT id, plu, nombre, precio, stock FROM productos WHERE plu = ?", (plu,))
                producto = cursor.fetchone()
                conexion.close()
                if producto:
                    self.agregar_al_carrito(producto)
                    self.input_plu.clear()  # Limpia barra de busqueda y deja abierto al proximo escaneo
                    self.input_plu.setFocus()  
                else:
                    QMessageBox.warning(self, "Búsqueda", f"No se encontró un producto con PLU: {plu}")
            else:
                QMessageBox.warning(self, "Error", "El PLU debe tener exactamente 12 dígitos numéricos.")
            self.cargar_productos()  


    def cargar_productos(self, plu=None):
        conexion = sqlite3.connect("pos.db")
        cursor = conexion.cursor()
        if plu:
            cursor.execute("SELECT id, plu, nombre, precio, stock FROM productos WHERE plu = ?", (plu,))
        else:
            cursor.execute("SELECT id, plu, nombre, precio, stock FROM productos")
        productos = cursor.fetchall()
        conexion.close()

        self.tabla_productos.setRowCount(len(productos))

        for fila, producto in enumerate(productos):
            id_producto, plu, nombre, precio, stock = producto
            self.tabla_productos.setItem(fila, 0, QTableWidgetItem(plu))
            self.tabla_productos.setItem(fila, 1, QTableWidgetItem(nombre))
            self.tabla_productos.setItem(fila, 2, QTableWidgetItem(str(precio)))
            self.tabla_productos.setItem(fila, 3, QTableWidgetItem(str(stock)))

            boton_agregar = QPushButton("Agregar")
            boton_agregar.clicked.connect(lambda _, p=producto: self.agregar_al_carrito(p))
            self.tabla_productos.setCellWidget(fila, 4, boton_agregar)

    def actualizar_tabla(self):
        """Refresca la tabla de productos después de una venta o restock."""
        self.tabla_productos.clearContents()
        self.cargar_productos()

    def agregar_al_carrito(self, producto):
        id_producto, plu, nombre, precio, _ = producto  # ignoramos el stock anterior

        # Contar cuántas veces está ya en el carrito
        cantidad_en_carrito = sum(1 for p in self.carrito if p[0] == id_producto)

        # Consultar stock actual en base de datos
        conexion = sqlite3.connect("pos.db")
        cursor = conexion.cursor()
        cursor.execute("SELECT stock FROM productos WHERE id = ?", (id_producto,))
        resultado = cursor.fetchone()
        conexion.close()

        if resultado:
            stock_disponible = resultado[0]
            if cantidad_en_carrito < stock_disponible:
                self.carrito.append((id_producto, nombre, precio))
                self.lista_carrito.addItem(f"{nombre} - ${precio}")
                self.actualizar_total()
            else:
                QMessageBox.critical(self, "Stock insuficiente", f"No puedes agregar más unidades de '{nombre}'.\nStock disponible: {stock_disponible}")
        else:
            QMessageBox.critical(self, "Error", "Producto no encontrado en la base de datos.")

    def eliminar_del_carrito(self):
        selected_item = self.lista_carrito.currentRow()
        if selected_item >= 0:
            self.carrito.pop(selected_item)
            self.lista_carrito.takeItem(selected_item)
            self.actualizar_total()
        else:
            QMessageBox.warning(self, "Error", "Seleccione un producto del carrito para eliminar.")

    def actualizar_total(self):
        total = sum(precio for _, _, precio in self.carrito)
        self.total_label.setText(f"Total: ${total:.2f}")


    def procesar_venta(self):
        if not self.carrito:
            QMessageBox.warning(self, "Carrito vacío", "No hay productos en el carrito.")
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

        # Generar el ticket
        cursor.execute("SELECT n.nombre, dv.cantidad, dv.subtotal FROM detalle_ventas dv JOIN productos n ON dv.producto_id = n.id WHERE dv.venta_id=?", (venta_id,))
        articulos = cursor.fetchall()

        cursor.execute("SELECT total FROM ventas WHERE id=?", (venta_id,))
        total = cursor.fetchone()[0]

        ticket_text = "\n"
        ticket_text += "-------------- Ticket de Venta -------------\n"
        ticket_text += f"Id de la venta: {venta_id}\n"
        ticket_text += "------------------------------------------\n"
        ticket_text += f"{'Nombre':<20}{'Cantidad':<10}{'Subtotal':<10}\n"
        for nombre, cantidad, subtotal in articulos:
            ticket_text += f"{nombre:<20}{cantidad:<12}{subtotal:<10.2f}\n"
        ticket_text += "------------------------------------------\n"
        ticket_text += f"{'El total es: ':<30}${total:.2f}\n"
        ticket_text += "------------------------------------------\n"
        ticket_text += "\n"

        conexion.close()

        # Mostrar el ticket 
        ticket_dialog = TicketDialog(ticket_text, self)
        ticket_dialog.exec()

        self.carrito.clear()
        self.lista_carrito.clear()
        self.actualizar_total()
        self.actualizar_tabla()


    def restock_producto(self):
        """Permite al usuario seleccionar un producto y agregar stock."""
        conexion = sqlite3.connect("pos.db")
        cursor = conexion.cursor()
        cursor.execute("SELECT id, nombre FROM productos")
        productos = cursor.fetchall()
        conexion.close()

        if not productos:
            QMessageBox.warning(self, "Sin productos", "No hay productos disponibles.")
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
                QMessageBox.information(self, "Restock", "Stock actualizado correctamente.")

    def eliminar_producto(self):
        conexion = sqlite3.connect("pos.db")
        cursor = conexion.cursor()
        cursor.execute("SELECT id, nombre FROM productos")
        productos = cursor.fetchall()
        conexion.close()

        if not productos:
            QMessageBox.warning(self, "Sin productos", "No hay productos disponibles.")
            return

        # Mostrar cuadro de diálogo para seleccionar producto
        items = [f"{p[0]} - {p[1]}" for p in productos]
        item, ok = QInputDialog.getItem(self, "Eliminar artículo", "Selecciona un producto:", items, 0, False)

        if ok and item:
            id_producto = int(item.split(" - ")[0])  # Obtener el ID del producto
            codigo, ok = QInputDialog.getInt(self, "Código", "Ingrese el código:")

            if ok and codigo == 123:
                conexion = sqlite3.connect("pos.db")
                cursor = conexion.cursor()
                cursor.execute("DELETE FROM productos WHERE id=?", (id_producto,))
                conexion.commit()
                conexion.close()

                self.actualizar_tabla()
                QMessageBox.information(self, "Eliminado", "Artículo eliminado correctamente.")
            else:
                QMessageBox.warning(self, "Error", "No se ha eliminado el artículo - Código incorrecto.")

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
            
            # Se obtiene la fecha
            fecha_actual = datetime.now().strftime("%Y-%m-%d")
            nombre_archivo = f"Ventas ({fecha_actual}).xlsx"

            # Exportar al archivo Excel con nombre basado en la fecha
            df.to_excel(nombre_archivo, index=False)
            print(f"Ventas exportadas a {nombre_archivo} con productos agrupados correctamente.")
        except Exception as e:
            print("Error al exportar:", e)
        finally:
            conexion.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = PuntoDeVenta()
    ventana.show()
    sys.exit(app.exec())
