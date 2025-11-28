# ============================================================================
# ARCHIVO 7: main.py (ARCHIVO PRINCIPAL)
# ============================================================================
# 
# PROPÓSITO: Este es el archivo PRINCIPAL que integra TODOS los módulos
# y ejecuta el sistema completo.
#
# ¿QUÉ HACE?
# ----------
# - Importa todos los módulos creados
# - Carga datos existentes desde archivos JSON
# - Crea los gestores (inventario, clientes, ventas, reportes)
# - Muestra el menú principal
# - Coordina entre todos los módulos
# - Guarda todos los datos al salir
#
# ESTE ES EL ÚNICO ARCHIVO QUE EJECUTAS
# --------------------------------------
# Para ejecutar el sistema completo, solo ejecutas:
# python main.py
#
# Los demás archivos son MÓDULOS que este archivo importa.
#
# ============================================================================


# ============================================================================
# PASO 1: IMPORTAR TODOS LOS MÓDULOS
# ============================================================================
# Importamos las clases y funciones de los archivos que creamos

from persistencia import GestorPersistencia
# Clase para guardar/cargar datos en JSON

from inventario import GestorInventario
# Clase para manejar el inventario de libros

from clientes import GestorClientes
# Clase para manejar clientes y sus compras

from ventas import GestorVentas
# Clase para manejar el sistema de ventas

from reportes import GestorReportes
# Clase para generar reportes y estadísticas

from validacion import pedir_int
# Función para pedir números enteros con validación


# ============================================================================
# PASO 2: CREAR LA CLASE PRINCIPAL DEL SISTEMA
# ============================================================================

class SistemaLibreria:
    """
    CLASE PRINCIPAL DEL SISTEMA:
    ----------------------------
    Esta clase es el "cerebro" del sistema. Coordina todos los demás módulos.
    
    RESPONSABILIDADES:
    ------------------
    1. Inicializar el sistema (cargar datos, crear gestores)
    2. Mostrar el menú principal
    3. Coordinar entre módulos
    4. Guardar datos al salir
    
    ARQUITECTURA DEL SISTEMA:
    -------------------------
    
    SistemaLibreria (main.py)
         |
         |--- GestorPersistencia (persistencia.py)
         |
         |--- GestorInventario (inventario.py)
         |         |
         |         |--- utilidades.py
         |
         |--- GestorClientes (clientes.py)
         |
         |--- GestorVentas (ventas.py)
         |         |
         |         |--- GestorInventario
         |         |--- GestorClientes
         |
         |--- GestorReportes (reportes.py)
                   |
                   |--- GestorClientes
                   |--- GestorVentas
    
    FLUJO DE DATOS:
    ---------------
    1. Al iniciar:
       JSON -> GestorPersistencia -> Gestores individuales
    
    2. Durante uso:
       Usuario -> Menús -> Gestores -> Modifican datos
    
    3. Al salir:
       Gestores -> GestorPersistencia -> JSON
    
    ATRIBUTOS DE LA CLASE:
    ----------------------
    - self.persistencia: Gestor para guardar/cargar archivos
    - self.gestor_inventario: Maneja inventario
    - self.gestor_clientes: Maneja clientes
    - self.gestor_ventas: Maneja ventas
    - self.gestor_reportes: Genera reportes
    """
    
    def __init__(self):
        """
        CONSTRUCTOR DEL SISTEMA:
        ------------------------
        Este método se ejecuta automáticamente al crear el sistema.
        Inicializa TODOS los componentes.
        
        PROCESO:
        --------
        1. Crear el gestor de persistencia
        2. Cargar datos desde archivos JSON
        3. Crear todos los gestores con los datos cargados
        4. Conectar los gestores entre sí
        
        ORDEN IMPORTANTE:
        -----------------
        El orden de inicialización es crucial:
        1. Persistencia (necesario para cargar datos)
        2. Cargar datos (necesarios para crear gestores)
        3. Inventario y Clientes (independientes)
        4. Ventas (necesita inventario y clientes)
        5. Reportes (necesita clientes y ventas)
        """
        
        # ===== PASO 1: Crear gestor de persistencia =====
        self.persistencia = GestorPersistencia()
        # Este objeto se usará para guardar y cargar todos los archivos
        
        # ===== PASO 2: Cargar datos desde archivos JSON =====
        # Si los archivos no existen, se crean automáticamente con valores por defecto
        
        inventario = self.persistencia.cargar_datos("inventario.json", [])
        # Si no existe: inventario = []
        # Si existe: inventario = [{"titulo": "...", ...}, ...]
        
        clientes = self.persistencia.cargar_datos("clientes.json", {})
        # Si no existe: clientes = {}
        # Si existe: clientes = {"1": {"nombre": "...", ...}, ...}
        
        ventas = self.persistencia.cargar_datos("ventas.json", [])
        # Si no existe: ventas = []
        # Si existe: ventas = [{"id_cliente": "1", ...}, ...]
        
        # ===== PASO 3: Crear gestores independientes =====
        # Estos gestores NO dependen de otros gestores
        
        self.gestor_inventario = GestorInventario(inventario, self.persistencia)
        # Crear gestor de inventario con:
        # - Los libros cargados desde JSON
        # - El gestor de persistencia para guardar cambios
        
        self.gestor_clientes = GestorClientes(clientes, self.persistencia)
        # Crear gestor de clientes con:
        # - Los clientes cargados desde JSON
        # - El gestor de persistencia para guardar cambios
        
        # ===== PASO 4: Crear gestores dependientes =====
        # Estos gestores NECESITAN otros gestores para funcionar
        
        self.gestor_ventas = GestorVentas(
            ventas,                    # Ventas cargadas desde JSON
            self.gestor_inventario,    # Necesita acceso al inventario
            self.gestor_clientes,      # Necesita acceso a clientes
            self.persistencia          # Necesita guardar datos
        )
        # El gestor de ventas COORDINA entre inventario y clientes
        
        self.gestor_reportes = GestorReportes(
            self.gestor_clientes,      # Necesita acceso a clientes
            self.gestor_ventas         # Necesita acceso a ventas
        )
        # El gestor de reportes CONSULTA datos de clientes y ventas
        
        # ===== SISTEMA INICIALIZADO Y LISTO PARA USAR =====
    
    
    def menu_principal(self):
        """
        MENÚ PRINCIPAL DEL SISTEMA:
        ---------------------------
        Este es el punto de entrada del usuario al sistema.
        Desde aquí puede acceder a todos los módulos.
        
        OPCIONES:
        ---------
        1. Gestión de Inventario -> self.gestor_inventario.menu()
        2. Ventas -> self.gestor_ventas.menu()
        3. Reportes -> self.gestor_reportes.menu()
        4. Salir -> guardar_todo_y_salir()
        
        BUCLE INFINITO:
        ---------------
        El menú se muestra en un bucle infinito (while True)
        que solo termina cuando el usuario selecciona "Salir".
        """
        while True:  # Bucle infinito
            # Mostrar el menú
            print("\n" + "="*50)
            print(" SISTEMA DE GESTIÓN DE LIBRERÍA")
            print("="*50)
            print("1. Gestión de Inventario")
            print("2. Ventas (Carrito de Compras)")
            print("3. Reportes y Estadísticas")
            print("4. Salir")
            
            # Pedir opción al usuario
            opcion = pedir_int("\nSelecciona una opción: ")
            
            # Ejecutar la opción seleccionada
            if opcion == 1:
                # GESTIÓN DE INVENTARIO
                self.gestor_inventario.menu()
                # Al salir del menú de inventario, vuelve aquí
                
            elif opcion == 2:
                # SISTEMA DE VENTAS
                self.gestor_ventas.menu()
                # Al salir del menú de ventas, vuelve aquí
                
            elif opcion == 3:
                # REPORTES Y ESTADÍSTICAS
                self.gestor_reportes.menu()
                # Al salir del menú de reportes, vuelve aquí
                
            elif opcion == 4:
                # SALIR DEL SISTEMA
                self.guardar_todo_y_salir()
                break  # Rompe el bucle while, termina el programa
                
            else:
                print(" Opción inválida")
    
    
    def guardar_todo_y_salir(self):
        """
        GUARDAR TODOS LOS DATOS Y SALIR:
        --------------------------------
        Esta función se ejecuta al salir del sistema.
        Garantiza que TODOS los datos se guarden correctamente.
        
        PROCESO:
        --------
        1. Guardar inventario en inventario.json
        2. Guardar clientes en clientes.json
        3. Guardar ventas en ventas.json
        4. Mostrar mensajes de confirmación
        5. Despedirse del usuario
        
        CONGRUENCIA DE DATOS:
        ---------------------
        Es crucial guardar todo antes de salir para mantener
        la congruencia entre los módulos.
        
        Si solo guardáramos el inventario pero no las ventas,
        habría inconsistencias: el inventario mostraría menos stock
        pero no habría registro de las ventas que causaron esa reducción.
        """
        # Guardar inventario
        self.gestor_inventario.guardar()
        # Esto ejecuta: GestorPersistencia.guardar_datos("inventario.json", inventario)
        
        # Guardar clientes
        self.gestor_clientes.guardar()
        # Esto ejecuta: GestorPersistencia.guardar_datos("clientes.json", clientes)
        
        # Guardar ventas
        self.persistencia.guardar_datos(
            "ventas.json",
            self.gestor_ventas.obtener_ventas()
        )
        
        # Confirmar y despedirse
        print("\n Datos guardados exitosamente")
        print(" ¡Hasta pronto!")


# ============================================================================
# PASO 3: PUNTO DE ENTRADA DEL PROGRAMA
# ============================================================================

if __name__ == "__main__":
    """
    PUNTO DE ENTRADA:
    -----------------
    Esta es una convención de Python.
    
    __name__ es una variable especial:
    - Si ejecutas este archivo directamente: __name__ == "__main__"
    - Si importas este archivo desde otro: __name__ == "main"
    
    Esto permite:
    - Ejecutar el código solo si es el archivo principal
    - Evitar que se ejecute al importarlo en otros archivos
    
    USO:
    ----
    Para ejecutar el sistema:
    $ python main.py
    
    Esto ejecutará todo el código dentro de este bloque if.
    """
    
    # PASO 1: Crear el sistema
    sistema = SistemaLibreria()
        # Al crear el objeto, se ejecuta __init__():
        # - Carga todos los datos
        # - Inicializa todos los gestores
        # - Conecta los módulos entre sí
        
        # PASO 2: Mostrar el menú principal
    sistema.menu_principal()
        # Esto muestra el menú y permite al usuario interactuar
        # con el sistema hasta que decida salir
        
        # PASO 3: Al salir, todos los datos ya fueron guardados
        # (esto se hace en guardar_todo_y_salir())


# ============================================================================
# RESUMEN COMPLETO DEL SISTEMA:
# ============================================================================
# 
# ESTRUCTURA DE ARCHIVOS:
# -----------------------
# 1. validacion.py      - Funciones de validación
# 2. persistencia.py    - Guardar/cargar JSON
# 3. inventario.py      - Gestión de libros
# 4. clientes.py        - Gestión de clientes
# 5. ventas.py          - Sistema de ventas
# 6. reportes.py        - Reportes y estadísticas
# 7. main.py (ESTE)     - Integración de todo
#
# ARCHIVOS JSON GENERADOS:
# ------------------------
# - inventario.json     - Todos los libros
# - clientes.json       - Todos los clientes
# - ventas.json         - Todas las ventas
#
# FLUJO COMPLETO DEL SISTEMA:
# ---------------------------
# 1. Ejecutar: python main.py
# 2. Sistema se inicializa:
#    - Carga datos de JSON
#    - Crea gestores
#    - Conecta módulos
# 3. Usuario ve menú principal
# 4. Usuario navega entre módulos:
#    - Inventario: agregar/actualizar/eliminar libros
#    - Ventas: procesar compras
#    - Reportes: ver estadísticas
# 5. Usuario sale del sistema
# 6. Sistema guarda todos los datos
# 7. Programa termina
#
# CONCEPTOS CLAVE APLICADOS:
# --------------------------
# 1. MODULARIZACIÓN: Código dividido en archivos lógicos
# 2. CLASES: Cada módulo es una clase con responsabilidades claras
# 3. COMPOSICIÓN: Clases que usan otras clases
# 4. PERSISTENCIA: Datos guardados en JSON
# 5. VALIDACIÓN: Todas las entradas validadas
# 6. CONGRUENCIA: Datos consistentes entre módulos
# 7. SEPARACIÓN DE RESPONSABILIDADES: Cada módulo hace UNA cosa bien
#
# VENTAJAS DE ESTA ARQUITECTURA:
# -------------------------------
#  MANTENIBLE: Fácil encontrar y modificar código
#  ESCALABLE: Fácil agregar nuevas funcionalidades
#  REUTILIZABLE: Módulos pueden usarse en otros proyectos
#  TESTEABLE: Cada módulo puede probarse independientemente
#  LEGIBLE: Código bien organizado y documentado
#  ROBUSTO: Validaciones y manejo de errores
#  PERSISTENTE: Datos no se pierden al cerrar
#  CONSISTENTE: Datos congruentes entre módulos
#
# CÓMO USAR EL SISTEMA:
# ---------------------
# 1. Asegúrate de tener todos los archivos .py en la misma carpeta
# 2. Ejecuta: python main.py
# 3. Navega por los menús usando números
# 4. Los datos se guardan automáticamente
# 5. Los archivos JSON se crean en la misma carpeta
#
# PARA MODIFICAR EL SISTEMA:
# --------------------------
# - Agregar validaciones: Edita validacion.py
# - Cambiar cómo se guardan datos: Edita persistencia.py
# - Modificar gestión de inventario: Edita inventario.py
# - Modificar gestión de clientes: Edita clientes.py
# - Modificar sistema de ventas: Edita ventas.py
# - Agregar reportes: Edita reportes.py
# - Cambiar menú principal: Edita main.py
#
# ============================================================================
#
# ¡SISTEMA COMPLETO Y LISTO PARA USAR!
#
# Para ejecutar:
# $ python main.py
#
# ============================================================================