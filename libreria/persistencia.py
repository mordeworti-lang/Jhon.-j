
# ============================================================================
# ARCHIVO 2: persistencia.py
# ============================================================================
# 
# PROPÓSITO: Este archivo maneja la PERSISTENCIA de datos, es decir,
# guardar y cargar información desde archivos JSON para que los datos
# NO SE PIERDAN cuando cerramos el programa.
#
# ¿QUÉ ES JSON?
# -------------
# JSON (JavaScript Object Notation) es un formato de texto que permite
# guardar datos estructurados de forma legible. Es como guardar un
# diccionario o lista de Python en un archivo de texto.
#
# Ejemplo de JSON:
# {
#     "nombre": "Juan",
#     "edad": 25,
#     "libros": ["Python", "JavaScript"]
# }
#
# ============================================================================

import json  # Módulo de Python para trabajar con archivos JSON
import os    # Módulo de Python para trabajar con archivos del sistema operativo

class GestorPersistencia:
    """
    EXPLICACIÓN DE CLASES:
    ----------------------
    Una CLASE es como un molde o plantilla que agrupa funciones relacionadas.
    En este caso, agrupa las funciones para guardar y cargar datos.
    
    ¿POR QUÉ USAR UNA CLASE?
    ------------------------
    - Organización: Todas las funciones relacionadas con persistencia están juntas
    - Reutilización: Podemos crear múltiples "gestores" si los necesitamos
    - Claridad: Es fácil saber que estas funciones manejan archivos
    
    MÉTODOS ESTÁTICOS:
    ------------------
    @staticmethod significa que el método NO necesita crear un objeto de la clase
    para usarse. Se puede llamar directamente:
    
    GestorPersistencia.cargar_datos("archivo.json", [])
    
    En lugar de:
    gestor = GestorPersistencia()
    gestor.cargar_datos("archivo.json", [])
    """
    
    @staticmethod
    def cargar_datos(archivo: str, default):
        """
        EXPLICACIÓN DETALLADA:
        ----------------------
        Esta función CARGA datos desde un archivo JSON.
        Si el archivo no existe, devuelve un valor por defecto.
        
        PARÁMETROS:
        -----------
        - archivo (str): Nombre del archivo JSON a cargar
        Ejemplo: "inventario.json", "clientes.json"
        
        - default: Valor que se devuelve si el archivo no existe
        Puede ser: [] (lista vacía), {} (diccionario vacío), etc.
        
        RETORNA:
        --------
        Los datos cargados desde el archivo, o el valor por defecto
        
        CÓMO FUNCIONA PASO A PASO:
        --------------------------
        """

        # PASO 1: Verificar si el archivo existe en el disco
        if os.path.exists(archivo):
        # os.path.exists() verifica si un archivo existe
        # Devuelve True si existe, False si no existe
            
            try:# Intentar cargar el archivo (puede fallar si está corrupto)
                
                # PASO 2: Abrir el archivo en modo lectura
                with open(archivo, "r", encoding = "utf-8") as f:
                    # 'r' = modo lectura (read)
                    # encoding='utf-8' = permite leer caracteres especiales (ñ, á, é, etc.)
                    # 'as f' = asigna el archivo a la variable 'f'
                    # 'with' = cierra automáticamente el archivo al terminar
                    
                    # PASO 3: Leer y convertir el contenido JSON a datos de Python
                    return json.load(f)
                    # json.load() lee el archivo y convierte el texto JSON
                    # en diccionarios, listas, etc. de Python
            
            except:  # Si hay algún error al leer el archivo
                # Puede fallar si el archivo está corrupto o vacío
                return default  # Devolver el valor por defecto
        
        # PASO 4: Si el archivo no existe, devolver el valor por defecto
        return default  
    @staticmethod
    def guardar_datos(archivo: str, datos):
        """
        EXPLICACIÓN DETALLADA:
        ----------------------
        Esta función GUARDA datos en un archivo JSON.
        Convierte los datos de Python (listas, diccionarios) a formato JSON
        y los escribe en un archivo.
        
        PARÁMETROS:
        -----------
        - archivo (str): Nombre del archivo donde guardar
          Ejemplo: "inventario.json", "clientes.json"
        
        - datos: Los datos a guardar (puede ser lista, diccionario, etc.)
          Ejemplo: [{"titulo": "Python", "precio": 25.99}]
        
        RETORNA:
        --------
        Nada (None). Solo guarda los datos en el archivo.
        
        CÓMO FUNCIONA PASO A PASO:
        --------------------------
        """
        # PASO 1: Abrir (o crear) el archivo en modo escritura
        with open(archivo, "w", encoding= "utf-8")as f:
            # 'w' = modo escritura (write)
            # Si el archivo no existe, lo crea
            # Si existe, lo sobrescribe (borra el contenido anterior)
            # encoding='utf-8' = permite escribir caracteres especiales
            
            # PASO 2: Convertir los datos de Python a formato JSON y escribirlos
            json.dump (datos, f, indent=4, ensure_ascii=False)
             # json.dump() convierte los datos a texto JSON y los escribe
            # 
            # Parámetros importantes:
            # - datos: Lo que queremos guardar
            # - f: El archivo donde escribir
            # - indent=4: Agrega sangría para que sea legible (4 espacios)
            # - ensure_ascii=False: Permite guardar caracteres especiales (ñ, á, etc.)
            #
            # Sin indent=4, el JSON quedaría en una sola línea:
            # {"nombre":"Juan","edad":25}
            #
            # Con indent=4, queda organizado:
            # {
            #     "nombre": "Juan",
            #     "edad": 25
            # }


# ============================================================================
# EJEMPLO DE USO DE ESTE MÓDULO:
# ============================================================================
#
# GUARDAR DATOS:
# --------------
# inventario = [
#     {"titulo": "Python Básico", "precio": 25.99, "cantidad": 10},
#     {"titulo": "JavaScript Pro", "precio": 30.50, "cantidad": 5}
# ]
# 
# GestorPersistencia.guardar_datos("inventario.json", inventario)
# # Esto crea el archivo "inventario.json" con los datos
#
# CARGAR DATOS:
# -------------
# inventario = GestorPersistencia.cargar_datos("inventario.json", [])
# # Si el archivo existe, carga los datos
# # Si no existe, devuelve [] (lista vacía)
#
# print(inventario)
# # [{"titulo": "Python Básico", "precio": 25.99, "cantidad": 10}, ...]
#
# ============================================================================


# ============================================================================
# RESUMEN DE ESTE ARCHIVO:
# ============================================================================
# 
# Este archivo contiene 1 clase con 2 métodos estáticos:
# 
# CLASE: GestorPersistencia
# -------------------------
# Agrupa las funciones para manejar archivos JSON
# 
# MÉTODO 1: cargar_datos(archivo, default)
# -----------------------------------------
# - Lee un archivo JSON y convierte su contenido a datos de Python
# - Si el archivo no existe, devuelve un valor por defecto
# - Maneja errores automáticamente
# 
# MÉTODO 2: guardar_datos(archivo, datos)
# ----------------------------------------
# - Convierte datos de Python a formato JSON
# - Guarda el JSON en un archivo
# - Crea el archivo si no existe, lo sobrescribe si existe
# 
# CONCEPTOS CLAVE:
# ----------------
# 1. JSON: Formato de texto para guardar datos estructurados
# 2. PERSISTENCIA: Guardar datos para que no se pierdan al cerrar el programa
# 3. CLASE: Agrupa funciones relacionadas
# 4. MÉTODO ESTÁTICO: Función que no necesita crear un objeto de la clase
# 
# VENTAJAS:
# ---------
# - Los datos se guardan automáticamente en archivos
# - Los datos persisten entre ejecuciones del programa
# - Fácil de usar: solo 2 funciones (cargar y guardar)
# - Manejo automático de errores
# 
# ============================================================================


            