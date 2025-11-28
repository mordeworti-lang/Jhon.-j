# ============================================================================
# ARCHIVO 4: clientes.py
# ============================================================================
# 
# PROPÓSITO: Este archivo maneja todo lo relacionado con los CLIENTES
# de la librería.
#
# ¿QUÉ HACE?
# ----------
# - Registrar nuevos clientes con ID único
# - Buscar clientes existentes
# - Evitar duplicar clientes (si ya existe, usa el mismo ID)
# - Guardar historial de compras de cada cliente
# - Calcular total gastado por cada cliente
# - Guardar/cargar datos de clientes en JSON
#
# ============================================================================

from datetime import datetime
# datetime es un módulo de Python para trabajar con fechas y horas
# Ejemplo: datetime.now() -> fecha y hora actual


class GestorClientes:
    """
    EXPLICACIÓN DE ESTA CLASE:
    --------------------------
    Esta clase maneja todo lo relacionado con clientes.
    
    FUNCIONALIDAD CLAVE:
    --------------------
    - CONTADOR DE IDs: Cada cliente nuevo obtiene un ID único (1, 2, 3, ...)
    - NO DUPLICADOS: Si un cliente ya existe, usa su ID anterior
    - HISTORIAL: Cada cliente tiene un historial de todas sus compras
    - PERSISTENCIA: Los datos se guardan en "clientes.json"
    
    ESTRUCTURA DE DATOS DE UN CLIENTE:
    -----------------------------------
    {
        "1": {  # ID del cliente (clave del diccionario)
            "nombre": "Juan Pérez",
            "fecha_registro": "2024-01-15 10:30:00",
            "compras": [  # Lista de todas sus compras
                {
                    "fecha": "2024-01-15 10:35:00",
                    "productos": [...],
                    "total": 45.99
                }
            ],
            "total_gastado": 45.99
        },
        "2": {  # Otro cliente
            "nombre": "María García",
            ...
        }
    }
    
    ATRIBUTOS DE LA CLASE:
    ----------------------
    - self.clientes: Diccionario con TODOS los clientes
    - self.persistencia: Objeto para guardar/cargar datos
    - self.archivo: Nombre del archivo JSON ("clientes.json")
    - self.contador: Contador para generar IDs únicos
    """
    
    def __init__(self, clientes: dict, persistencia):
        """
        CONSTRUCTOR DE LA CLASE:
        ------------------------
        Inicializa el gestor de clientes.
        
        PARÁMETROS:
        -----------
        - clientes (dict): Diccionario con los clientes existentes
        Puede estar vacío {} si no hay clientes aún
        
        - persistencia: Objeto GestorPersistencia para guardar datos
        
        ¿QUÉ HACE?
        ----------
        1. Guarda el diccionario de clientes
        2. Guarda el gestor de persistencia
        3. Define el nombre del archivo
        4. Calcula el próximo ID disponible
        """
        self.clientes = clientes
        self.persistencia = persistencia
        self.archivo = "clientes.json"
        
        # Calcular el próximo ID disponible
        # Si hay clientes: usar el ID más alto + 1
        # Si no hay clientes: empezar en 1
        self.contador = self._obtener_max_id() + 1
    
    
    def _obtener_max_id(self):
        """
        OBTENER EL ID MÁS ALTO:
        -----------------------
        Busca entre todos los clientes existentes y retorna el ID más alto.
        
        NOMBRE CON GUIÓN BAJO:
        ----------------------
        El _ al inicio (_obtener_max_id) indica que es un método PRIVADO.
        Esto es una CONVENCIÓN de Python que significa:
        "Este método es solo para uso interno de la clase,
        no lo llames desde fuera"
        
        RETORNA:
        --------
        - int: El ID más alto encontrado
        - 0: Si no hay clientes
        
        CÓMO FUNCIONA:
        --------------
        """
        # Si no hay clientes, retornar 0
        if not self.clientes:
            return 0
        
        # Si hay clientes, encontrar el ID más alto
        # self.clientes.keys() da todas las claves (IDs) del diccionario
        # Ejemplo: si clientes = {"1": {...}, "5": {...}, "3": {...}}
        #          entonces keys() = ["1", "5", "3"]
        
        # max() encuentra el valor máximo
        # int() convierte texto a número: "5" -> 5
        
        return max(int(id_cliente) for id_cliente in self.clientes.keys())
        # Esto es una COMPRENSIÓN DE LISTA (list comprehension)
        # Lee así: "Para cada id_cliente en las claves,
        #           conviértelo a int y dame el máximo"
    
    
    def obtener_o_crear_cliente(self, nombre: str) -> str:
        """
        FUNCIÓN CLAVE DEL SISTEMA:
        --------------------------
        Esta función es MUY IMPORTANTE porque:
        1. Busca si el cliente ya existe (por nombre)
        2. Si existe: retorna su ID (NO crea uno nuevo)
        3. Si NO existe: crea un nuevo cliente con ID único
        
        ESTO EVITA DUPLICADOS: Si "Juan Pérez" compra 3 veces,
        las 3 compras se registran con el MISMO ID.
        
        PARÁMETROS:
        -----------
        - nombre (str): Nombre del cliente
        
        RETORNA:
        --------
        - str: El ID del cliente (nuevo o existente)
        
        EJEMPLO:
        --------
        Primera vez: obtener_o_crear_cliente("Juan") -> "1" (nuevo)
        Segunda vez: obtener_o_crear_cliente("Juan") -> "1" (mismo ID)
        Tercera vez: obtener_o_crear_cliente("María") -> "2" (nuevo)
        """
        nombre_buscar = nombre.lower().strip()
        # Normalizar el nombre para comparar sin importar mayúsculas/espacios
        # "  JUAN  " -> "juan"
        # "Juan" -> "juan"
        # "JUAN" -> "juan"
        
        # PASO 1: Buscar si el cliente ya existe
        for id_cliente, datos in self.clientes.items():
            # .items() da pares (clave, valor)
            # Ejemplo: [("1", {...}), ("2", {...})]
            
            # Comparar nombres (ambos en minúsculas)
            if datos['nombre'].lower().strip() == nombre_buscar:
                # ¡Cliente encontrado!
                print(f" Cliente encontrado (ID: {id_cliente})")
                return id_cliente  # Retornar su ID existente
        
        # PASO 2: Si llegamos aquí, el cliente NO existe, crear uno nuevo
        nuevo_id = str(self.contador)  # Convertir el contador a texto
        # Ejemplo: contador = 5 -> nuevo_id = "5"
        
        # Crear el diccionario del nuevo cliente
        self.clientes[nuevo_id] = {
            "nombre": nombre,
            "fecha_registro": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            # datetime.now() -> fecha/hora actual
            # .strftime() -> formatea la fecha como texto
            # Ejemplo: "2024-01-15 14:30:00"
            
            "compras": [],  # Lista vacía, aún no ha comprado nada
            "total_gastado": 0  # Aún no ha gastado nada
        }
        
        # Incrementar el contador para el próximo cliente
        self.contador += 1
        
        print(f" Nuevo cliente registrado (ID: {nuevo_id})")
        return nuevo_id
    
    
    def registrar_compra(self, id_cliente: str, venta: dict):
        """
        REGISTRAR UNA COMPRA:
        ---------------------
        Agrega una compra al historial del cliente y actualiza su total gastado.
        
        PARÁMETROS:
        -----------
        - id_cliente (str): ID del cliente que hizo la compra
        - venta (dict): Diccionario con los detalles de la venta
          Estructura:
          {
              "fecha": "2024-01-15 14:30:00",
              "productos": [
                  {"titulo": "Python", "cantidad": 2, "subtotal": 50.00},
                  ...
              ],
              "total": 50.00
          }
        
        ¿QUÉ HACE?
        ----------
        1. Verifica que el cliente existe
        2. Agrega la venta a su lista de compras
        3. Suma el total de la venta a su total_gastado
        """
        # Verificar que el cliente existe
        if id_cliente in self.clientes:
            # Agregar la venta al historial
            self.clientes[id_cliente]['compras'].append(venta)
            
            # Actualizar el total gastado
            self.clientes[id_cliente]['total_gastado'] += venta['total']
            # += suma al valor actual
            # Si total_gastado era 100 y venta['total'] es 50
            # entonces total_gastado = 100 + 50 = 150
    
    
    def obtener_cliente(self, id_cliente: str):
        """
        OBTENER INFORMACIÓN DE UN CLIENTE:
        -----------------------------------
        Retorna el diccionario completo de un cliente.
        
        PARÁMETROS:
        -----------
        - id_cliente (str): ID del cliente
        
        RETORNA:
        --------
        - dict: Diccionario con toda la información del cliente
        - None: Si el cliente no existe
        """
        return self.clientes.get(id_cliente)
        # .get() retorna el valor si existe, None si no existe
    
    
    def buscar_cliente(self, termino: str):
        """
        BUSCAR UN CLIENTE:
        ------------------
        Busca un cliente por ID o por nombre.
        
        PARÁMETROS:
        -----------
        - termino (str): Puede ser el ID ("1") o el nombre ("Juan")
        
        RETORNA:
        --------
        - tupla: (id_cliente, datos_cliente) si se encuentra
        - tupla: (None, None) si no se encuentra
        
        ¿QUÉ ES UNA TUPLA?
        ------------------
        Una tupla es como una lista, pero INMUTABLE (no se puede modificar).
        Se escribe con paréntesis: (valor1, valor2)
        
        Ejemplo:
        resultado = buscar_cliente("1")
        id_encontrado = resultado[0]  # Primer elemento
        datos = resultado[1]  # Segundo elemento
        
        O usando desempaquetado:
        id_encontrado, datos = buscar_cliente("1")
        """
        termino_buscar = termino.lower().strip()
        
        # Recorrer todos los clientes
        for id_cliente, datos in self.clientes.items():
            # Comparar por ID o por nombre
            if id_cliente == termino or datos['nombre'].lower().strip() == termino_buscar:
                return id_cliente, datos  # Retornar tupla (id, datos)
        
        # No se encontró
        return None, None  # Retornar tupla (None, None)
    
    
    def guardar(self):
        """
        GUARDAR LOS CLIENTES:
        ---------------------
        Guarda todos los clientes en el archivo JSON.
        """
        self.persistencia.guardar_datos(self.archivo, self.clientes)


# ============================================================================
# RESUMEN DE ESTE ARCHIVO:
# ============================================================================
# 
# CLASE: GestorClientes
# ---------------------
# Maneja todo lo relacionado con clientes de la librería.
# 
# ATRIBUTOS:
# ----------
# - self.clientes: Diccionario con todos los clientes
# - self.persistencia: Gestor para guardar/cargar datos
# - self.archivo: Nombre del archivo JSON ("clientes.json")
# - self.contador: Contador para generar IDs únicos (1, 2, 3, ...)
# 
# MÉTODOS PRINCIPALES:
# --------------------
# - __init__(): Constructor que inicializa el gestor
# - obtener_o_crear_cliente(nombre): Busca cliente o crea uno nuevo (CLAVE)
# - registrar_compra(id, venta): Agrega una compra al historial del cliente
# - obtener_cliente(id): Retorna información de un cliente
# - buscar_cliente(termino): Busca por ID o nombre
# - guardar(): Guarda clientes en JSON
# 
# MÉTODOS PRIVADOS:
# -----------------
# - _obtener_max_id(): Calcula el ID más alto existente
# 
# CONCEPTOS CLAVE:
# ----------------
# 1. CONTADOR DE IDs: Sistema para generar IDs únicos (1, 2, 3, ...)
# 2. EVITAR DUPLICADOS: Busca antes de crear, reutiliza IDs
# 3. HISTORIAL: Cada cliente tiene lista de todas sus compras
# 4. TUPLAS: Estructura inmutable para retornar múltiples valores
# 5. MÉTODOS PRIVADOS: Convención con _ para métodos internos
# 6. DATETIME: Módulo para manejar fechas y horas
# 
# FLUJO DE TRABAJO:
# -----------------
# 1. Al iniciar: Cargar clientes existentes desde JSON
# 2. En cada venta: 
#    - Buscar/crear cliente con obtener_o_crear_cliente()
#    - Registrar la compra con registrar_compra()
# 3. Al salir: Guardar todos los clientes en JSON
# 
# VENTAJAS:
# ---------
# - IDs únicos garantizados
# - No se duplican clientes
# - Historial completo de compras
# - Total gastado calculado automáticamente
# - Persistencia de datos entre sesiones
# 
# ============================================================================