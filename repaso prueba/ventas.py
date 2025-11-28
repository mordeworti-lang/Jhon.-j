# ============================================================================
# ARCHIVO 5: ventas.py
# ============================================================================
# 
# PROPÓSITO: Este archivo maneja TODO lo relacionado con el sistema de VENTAS
# (carrito de compras).
#
# ¿QUÉ HACE?
# ----------
# - Gestionar el carrito de compras
# - Verificar disponibilidad de stock
# - Manejar casos donde no hay suficiente stock
# - Descontar productos del inventario
# - Registrar ventas en historial general
# - Registrar compras en historial del cliente
# - Coordinar entre inventario y clientes
# - Guardar datos de ventas en JSON
#
# IMPORTACIONES NECESARIAS:
# -------------------------
from datetime import datetime
from validacion import pedir_int, pedir_texto
# Importamos las funciones de validación y el módulo de fechas
#
# ============================================================================


class GestorVentas:
    """
    EXPLICACIÓN DE ESTA CLASE:
    --------------------------
    Esta clase es el CORAZÓN del sistema de ventas.
    Coordina entre el inventario y los clientes para procesar ventas.
    
    RESPONSABILIDADES:
    ------------------
    1. Crear carritos de compra
    2. Verificar stock disponible
    3. Manejar casos de stock insuficiente
    4. Descontar del inventario
    5. Registrar la venta en el historial general
    6. Registrar la compra en el historial del cliente
    7. Calcular totales
    8. Confirmar o cancelar ventas
    
    ATRIBUTOS DE LA CLASE:
    ----------------------
    - self.ventas: LISTA con todas las ventas realizadas
    - self.inventario: Referencia al gestor de inventario
    - self.clientes: Referencia al gestor de clientes
    - self.persistencia: Objeto para guardar datos
    - self.archivo: Nombre del archivo JSON
    
    ESTRUCTURA DE UNA VENTA:
    ------------------------
    {
        "id_cliente": "1",
        "nombre_cliente": "Juan Pérez",
        "fecha": "2024-01-15 14:30:00",
        "productos": [
            {
                "titulo": "Python Básico",
                "autor": "Juan López",
                "categoria": "Programación",
                "cantidad": 2,
                "precio_unitario": 25.99,
                "subtotal": 51.98
            }
        ],
        "total": 51.98
    }
    """
    
    def __init__(self, ventas: list, gestor_inventario, gestor_clientes, persistencia):
        """
        CONSTRUCTOR DE LA CLASE:
        ------------------------
        Inicializa el gestor de ventas.
        
        PARÁMETROS:
        -----------
        - ventas (list): Lista con las ventas existentes
        - gestor_inventario: Objeto GestorInventario (para acceder al inventario)
        - gestor_clientes: Objeto GestorClientes (para registrar clientes)
        - persistencia: Objeto GestorPersistencia (para guardar datos)
        
        NOTA IMPORTANTE:
        ----------------
        Esta clase NECESITA trabajar con otros dos gestores:
        - GestorInventario: Para verificar stock y descontar productos
        - GestorClientes: Para registrar/buscar clientes
        
        Esto se llama "COMPOSICIÓN" en programación orientada a objetos.
        """
        self.ventas = ventas
        self.inventario = gestor_inventario
        self.clientes = gestor_clientes
        self.persistencia = persistencia
        self.archivo = "ventas.json"
    
    
    def menu(self):
        """
        MENÚ DE VENTAS:
        ---------------
        Menú simple con opción de realizar venta o volver.
        """
        while True:
            print("\n" + "="*50)
            print(" SISTEMA DE VENTAS")
            print("="*50)
            print("1. Realizar nueva venta")
            print("2. Volver al menú principal")
            
            opcion = pedir_int("\nSelecciona una opción: ")
            
            if opcion == 1:
                self.realizar_venta()
            elif opcion == 2:
                self.guardar_todo()
                break
            else:
                print("Opción inválida")
    
    
    def realizar_venta(self):
        """
        PROCESO COMPLETO DE VENTA:
        --------------------------
        Esta es la función MÁS COMPLEJA del sistema.
        Maneja todo el proceso de una venta desde inicio a fin.
        
        PASOS DEL PROCESO:
        ------------------
        1. Identificar o registrar al cliente
        2. Crear carrito de compras (bucle)
           a. Buscar libro
           b. Verificar stock
           c. Manejar stock insuficiente
           d. Agregar al carrito
           e. Descontar del inventario (temporal)
        3. Mostrar resumen de compra
        4. Pedir confirmación
        5. Si confirma: Registrar venta definitiva
        6. Si cancela: Revertir cambios en inventario
        """
        print("\n--- Nueva Venta ---")
        
        # ===== PASO 1: IDENTIFICAR O REGISTRAR CLIENTE =====
        nombre = pedir_texto("Nombre del cliente: ")
        id_cliente = self.clientes.obtener_o_crear_cliente(nombre)
        # Esta función busca el cliente o lo crea si no existe
        # GARANTIZA que no se dupliquen clientes
        
        # ===== PASO 2: CREAR CARRITO DE COMPRAS =====
        carrito = []  # Lista vacía para los productos
        total = 0  # Total acumulado de la compra
        
        # Bucle para agregar productos
        while True:
            print("\n--- Agregar producto al carrito ---")
            titulo = pedir_texto("Título del libro (o 'fin' para terminar): ")
            
            # Verificar si el usuario quiere terminar
            if titulo == 'fin':
                break  # Salir del bucle
            
            # Buscar el libro en el inventario
            libro = self.inventario.obtener_libro_por_titulo(titulo)
            if not libro:
                print(" Libro no encontrado")
                continue  # Volver al inicio del bucle
            
            # Mostrar información del libro
            print(f"\nLibro: {libro['titulo']}")
            print(f"Autor: {libro['autor']}")
            print(f"Precio: ${libro['precio']:.2f}")
            print(f"Stock disponible: {libro['cantidad']} unidades")
            
            # Preguntar cuántas unidades quiere comprar
            cantidad_deseada = pedir_int("Cantidad a comprar: ")
            
            # Validar que la cantidad sea mayor a 0
            if cantidad_deseada <= 0:
                print(" La cantidad debe ser mayor a 0")
                continue
            
            # ===== VERIFICAR DISPONIBILIDAD DE STOCK =====
            # ESTE ES UN PUNTO CLAVE DEL SISTEMA
            if cantidad_deseada > libro['cantidad']:
                # NO HAY SUFICIENTE STOCK
                print(f"\n Lo sentimos, solo tenemos {libro['cantidad']} unidades disponibles")
                
                # Preguntar si quiere llevar lo que hay disponible
                respuesta = pedir_texto(
                    f"¿Deseas llevar las {libro['cantidad']} unidades disponibles? (s/n): "
                )
                
                # Verificar la respuesta
                if respuesta in ("s", "si", "yes", "y"):
                    # Cliente acepta llevar lo disponible
                    cantidad_deseada = libro['cantidad']
                else:
                    # Cliente cancela este producto
                    print(" Compra cancelada para este producto")
                    continue  # Volver al inicio del bucle
            
            # ===== AGREGAR AL CARRITO =====
            # Si llegamos aquí, significa que HAY STOCK SUFICIENTE
            
            # Calcular el subtotal de este producto
            subtotal = cantidad_deseada * libro['precio']
            
            # Crear diccionario con los detalles del producto
            item_carrito = {
                "titulo": libro['titulo'],
                "autor": libro['autor'],
                "categoria": libro['categoria'],
                "cantidad": cantidad_deseada,
                "precio_unitario": libro['precio'],
                "subtotal": subtotal
            }
            
            # Agregar al carrito
            carrito.append(item_carrito)
            
            # Acumular al total general
            total += subtotal
            
            # ===== DESCONTAR DEL INVENTARIO (TEMPORAL) =====
            # Restamos la cantidad del inventario temporalmente
            # Si el usuario cancela la compra, lo revertiremos
            self.inventario.actualizar_stock(libro['titulo'], -cantidad_deseada)
            # Nota: -cantidad_deseada es NEGATIVO para RESTAR
            
            print(f" {cantidad_deseada} unidad(es) agregada(s) al carrito")
        
        # ===== PASO 3: VERIFICAR QUE HAY PRODUCTOS =====
        if not carrito:
            # Si el carrito está vacío, no continuar
            print("\n No se agregaron productos al carrito")
            return  # Salir de la función
        
        # ===== PASO 4: MOSTRAR RESUMEN =====
        self._mostrar_resumen(id_cliente, carrito, total)
        
        # ===== PASO 5: PEDIR CONFIRMACIÓN =====
        confirmacion = pedir_texto("\n¿Confirmar venta? (s/n): ")
        
        # ===== PASO 6: CONFIRMAR O CANCELAR =====
        if confirmacion in ("s", "si", "yes", "y"):
            # Usuario CONFIRMA la venta
            self._confirmar_venta(id_cliente, carrito, total)
        else:
            # Usuario CANCELA la venta
            self._cancelar_venta(carrito)
    
    
    def _mostrar_resumen(self, id_cliente, carrito, total):
        """
        MOSTRAR RESUMEN DE COMPRA:
        --------------------------
        Muestra un resumen ordenado de la compra antes de confirmar.
        
        MÉTODO PRIVADO:
        ---------------
        El _ al inicio indica que es para uso interno de la clase.
        
        PARÁMETROS:
        -----------
        - id_cliente (str): ID del cliente
        - carrito (list): Lista de productos en el carrito
        - total (float): Total de la compra
        """
        # Obtener información del cliente
        cliente = self.clientes.obtener_cliente(id_cliente)
        
        # Mostrar resumen
        print("\n" + "="*50)
        print(" RESUMEN DE COMPRA")
        print("="*50)
        print(f"Cliente: {cliente['nombre']}")
        print(f"ID Cliente: {id_cliente}")
        print("\nProductos:")
        
        # Mostrar cada producto del carrito
        for item in carrito:
            print(f"  - {item['titulo']} x{item['cantidad']} = ${item['subtotal']:.2f}")
            # :.2f formatea el número a 2 decimales
            # Ejemplo: 25.9 -> "25.90"
        
        print(f"\nTOTAL: ${total:.2f}")
    
    
    def _confirmar_venta(self, id_cliente, carrito, total):
        """
        CONFIRMAR VENTA:
        ----------------
        Registra la venta de forma definitiva.
        
        ¿QUÉ HACE?
        ----------
        1. Crea el diccionario de la venta
        2. Agrega la venta al historial general
        3. Agrega la compra al historial del cliente
        4. Muestra mensaje de éxito
        
        NOTA: Los cambios en el inventario ya se hicieron en realizar_venta(),
        así que aquí NO tocamos el inventario.
        """
        # Crear diccionario de la venta
        venta = {
            "id_cliente": id_cliente,
            "nombre_cliente": self.clientes.obtener_cliente(id_cliente)['nombre'],
            "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "productos": carrito,
            "total": total
        }
        
        # Agregar al historial general de ventas
        self.ventas.append(venta)
        
        # Agregar al historial del cliente
        self.clientes.registrar_compra(id_cliente, venta)
        
        # Mostrar mensaje de éxito
        print("\n Venta realizada exitosamente")
        print(f"Total: ${total:.2f}")
    
    
    def _cancelar_venta(self, carrito):
        """
        CANCELAR VENTA:
        ---------------
        Revierte los cambios en el inventario si el usuario cancela.
        
        IMPORTANTE:
        -----------
        Cuando agregamos productos al carrito, RESTAMOS del inventario.
        Si el usuario cancela, debemos DEVOLVER esas cantidades.
        
        PARÁMETROS:
        -----------
        - carrito (list): Lista de productos que se iban a vender
        """
        # Recorrer cada producto del carrito
        for item in carrito:
            # DEVOLVER la cantidad al inventario
            self.inventario.actualizar_stock(item['titulo'], item['cantidad'])
            # Nota: item['cantidad'] es POSITIVO para SUMAR de vuelta
        
        print("\n Venta cancelada")
    
    
    def obtener_ventas(self):
        """
        OBTENER TODAS LAS VENTAS:
        -------------------------
        Retorna la lista completa de ventas.
        Usado por el módulo de reportes para generar estadísticas.
        
        RETORNA:
        --------
        - list: Lista con todas las ventas realizadas
        """
        return self.ventas
    
    
    def guardar_todo(self):
        """
        GUARDAR TODOS LOS DATOS:
        ------------------------
        Guarda inventario, clientes y ventas antes de salir.
        
        IMPORTANTE:
        -----------
        Esta función coordina el guardado de TRES archivos:
        1. inventario.json (a través del gestor de inventario)
        2. clientes.json (a través del gestor de clientes)
        3. ventas.json (directamente)
        
        Esto garantiza la CONGRUENCIA de datos entre módulos.
        """
        self.inventario.guardar()
        self.clientes.guardar()
        self.persistencia.guardar_datos(self.archivo, self.ventas)
        print(" Datos guardados correctamente")


# ============================================================================
# RESUMEN DE ESTE ARCHIVO:
# ============================================================================
# 
# CLASE: GestorVentas
# -------------------
# Maneja todo el sistema de ventas (carrito de compras).
# 
# ATRIBUTOS:
# ----------
# - self.ventas: Lista con todas las ventas
# - self.inventario: Referencia al gestor de inventario
# - self.clientes: Referencia al gestor de clientes
# - self.persistencia: Gestor de archivos
# - self.archivo: "ventas.json"
# 
# MÉTODOS PRINCIPALES:
# --------------------
# - menu(): Menú de ventas
# - realizar_venta(): Proceso completo de venta (MÉTODO COMPLEJO)
# - obtener_ventas(): Retorna lista de ventas (para reportes)
# - guardar_todo(): Guarda inventario, clientes y ventas
# 
# MÉTODOS PRIVADOS:
# -----------------
# - _mostrar_resumen(): Muestra resumen antes de confirmar
# - _confirmar_venta(): Registra venta definitivamente
# - _cancelar_venta(): Revierte cambios si se cancela
# 
# CONCEPTOS CLAVE:
# ----------------
# 1. CARRITO DE COMPRAS: Lista temporal de productos
# 2. VERIFICACIÓN DE STOCK: Validar disponibilidad antes de vender
# 3. STOCK INSUFICIENTE: Ofrecer cantidad disponible al cliente
# 4. DESCUENTO TEMPORAL: Restar del inventario durante la compra
# 5. REVERSIÓN: Devolver al inventario si se cancela
# 6. CONFIRMACIÓN: Registrar definitivamente si se confirma
# 7. COMPOSICIÓN: Coordinar con otros gestores
# 8. CONGRUENCIA: Mantener datos consistentes entre módulos
# 
# FLUJO DE TRABAJO:
# -----------------
# 1. Identificar cliente (buscar o crear)
# 2. Agregar productos al carrito (bucle):
#    - Buscar libro
#    - Verificar stock
#    - Si no hay suficiente: ofrecer lo disponible
#    - Agregar al carrito
#    - Descontar temporalmente del inventario
# 3. Mostrar resumen
# 4. Pedir confirmación
# 5. Si confirma:
#    - Registrar en historial general
#    - Registrar en historial del cliente
#    - Mantener descuento del inventario
# 6. Si cancela:
#    - Revertir descuento del inventario
# 
# VENTAJAS DEL DISEÑO:
# --------------------
# - Manejo inteligente de stock insuficiente
# - No se venden más unidades de las disponibles
# - Opción de cancelar sin perder datos
# - Congruencia entre inventario, clientes y ventas
# - Historial completo de todas las transacciones
# 
# ============================================================================